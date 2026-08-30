from worldlab.testing import World


def test_same_seed_same_digest():
    a, b = World(), World()
    a.reset(7), b.reset(7)
    assert a.digest() == b.digest()


def test_digest_ignores_storage_layout():
    a, b = World(), World()
    a.reset(7), b.reset(7)

    rows = b.conn.execute("""
        SELECT id, title, status
        FROM tickets ORDER BY id DESC
    """).fetchall()
    b.conn.execute("DELETE FROM tickets")
    b.conn.executemany("INSERT INTO tickets (id, title, status) VALUES (?, ?, ?)", rows)
    b.conn.commit()
    b.conn.execute("VACUUM")

    assert a.digest() == b.digest()


def test_different_seed_different_digest():
    a, b = World(), World()
    a.reset(7), b.reset(8)
    assert a.digest() != b.digest()
