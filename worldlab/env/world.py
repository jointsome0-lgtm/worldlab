import hashlib
import json
import random
import sqlite3

DIGEST_VERSION = 1
EVENT_VERSION = 1
STATE_COLUMNS = ("id", "title", "status")
EVENT_KINDS = ("read", "mutation", "rejection", "replay", "termination")

SCHEMA = f"""
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS events;
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    title TEXT,
    status TEXT
);
CREATE TABLE events (
    seq INTEGER PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ({", ".join(repr(k) for k in EVENT_KINDS)})),
    tool TEXT NOT NULL,
    args TEXT NOT NULL,
    result TEXT NOT NULL,
    prev_hash TEXT NOT NULL,
    hash TEXT NOT NULL
);
CREATE TRIGGER events_no_update BEFORE UPDATE ON events
BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
CREATE TRIGGER events_no_delete BEFORE DELETE ON events
BEGIN SELECT RAISE(ABORT, 'events are append-only'); END;
"""


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


class World:
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA recursive_triggers = ON")

    def reset(self, seed: int):
        rng = random.Random(seed)
        self.conn.executescript(SCHEMA)

        tickets = []
        for i in range(5):
            title = rng.choice(["Login broken", "Typo on page", "Some error", "Not a problem", "Maybe a problem"])
            status = rng.choice(["open", "in_progress"])
            tickets.append((i + 1, title, status))

        self.conn.executemany("INSERT INTO tickets (id, title, status) VALUES (?, ?, ?)", tickets)
        self.conn.commit()

    def digest(self) -> str:
        rows = self.conn.execute(f"SELECT {', '.join(STATE_COLUMNS)} FROM tickets ORDER BY id").fetchall()
        string = f"v{DIGEST_VERSION}:" + canonical([dict(row) for row in rows])
        return hashlib.sha256(string.encode()).hexdigest()

    def head(self) -> str:
        row = self.conn.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
        return row["hash"] if row else ""

    def record(self, kind: str, tool: str, args, result) -> str:
        prev_hash = self.head()
        seq = self.conn.execute("SELECT COALESCE(MAX(seq), 0) + 1 FROM events").fetchone()[0]
        body = {"seq": seq, "kind": kind, "tool": tool, "args": args, "result": result, "prev_hash": prev_hash}
        digest = hashlib.sha256(f"v{EVENT_VERSION}:{canonical(body)}".encode()).hexdigest()
        self.conn.execute(
            "INSERT INTO events (seq, kind, tool, args, result, prev_hash, hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (seq, kind, tool, canonical(args), canonical(result), prev_hash, digest),
        )
        return digest
