import hashlib
import json
import sqlite3

import pytest

from worldlab.testing import World

SET_STATUS = {"ticket_id": 1, "status": "done"}


def expected_hash(seq, kind, tool, args, result, prev_hash):
    body = {"seq": seq, "kind": kind, "tool": tool, "args": args, "result": result, "prev_hash": prev_hash}
    string = "v1:" + json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(string.encode()).hexdigest()


def rows(world):
    return [tuple(row) for row in world.conn.execute("SELECT * FROM events ORDER BY seq").fetchall()]


def fresh():
    world = World()
    world.reset(7)
    return world


def test_written_row_survives_update_delete_and_replace():
    world = fresh()
    world.record("mutation", "set_status", SET_STATUS, {"ok": True})
    before = rows(world)

    for sql in (
        "UPDATE events SET result = '{}' WHERE seq = 1",
        "DELETE FROM events WHERE seq = 1",
        "INSERT OR REPLACE INTO events VALUES (1, 'read', 'x', '{}', '{}', '', '')",
    ):
        with pytest.raises(sqlite3.IntegrityError):
            world.conn.execute(sql)

    assert rows(world) == before


def test_each_row_hashes_the_one_before():
    world = fresh()
    first = world.record("read", "read_tickets", {}, [{"id": 1}])
    second = world.record("mutation", "set_status", SET_STATUS, {"ok": True})

    assert first == expected_hash(1, "read", "read_tickets", {}, [{"id": 1}], "")
    assert second == expected_hash(2, "mutation", "set_status", SET_STATUS, {"ok": True}, first)
    assert world.head() == second


def test_unknown_kind_is_rejected():
    world = fresh()
    with pytest.raises(sqlite3.IntegrityError):
        world.record("guess", "read_tickets", {}, {})
    assert rows(world) == []


def test_reset_starts_an_empty_log():
    world = fresh()
    world.record("mutation", "set_status", SET_STATUS, {"ok": True})
    world.reset(7)
    assert world.head() == ""
    assert rows(world) == []
