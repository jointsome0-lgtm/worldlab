import hashlib
import json
import random
import sqlite3

DIGEST_VERSION = 1
STATE_COLUMNS = ("id", "title", "status")


class World:
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def reset(self, seed: int):
        rng = random.Random(seed)
        cursor = self.conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS tickets")

        cursor.execute("""
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY,
            title TEXT,
            status TEXT
        )
        """)

        tickets = []

        for i in range(5):
            title = rng.choice(["Login broken", "Typo on page", "Some error", "Not a problem", "Maybe a problem"])
            status = rng.choice(["open", "in_progress"])
            tickets.append((i + 1, title, status))

        cursor.executemany("INSERT INTO tickets (id, title, status) VALUES (?, ?, ?)", tickets)

        self.conn.commit()

    def digest(self) -> str:
        cursor = self.conn.cursor()

        cursor.execute(f"SELECT {', '.join(STATE_COLUMNS)} FROM tickets ORDER BY id")
        rows = cursor.fetchall()
        rows = [dict(row) for row in rows]

        string = json.dumps(rows, sort_keys=True, separators=(",", ":"))
        string = f"v{DIGEST_VERSION}:" + string

        result = hashlib.sha256(string.encode()).hexdigest()

        return result
