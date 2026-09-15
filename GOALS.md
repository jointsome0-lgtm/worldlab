# worldlab

Long term: environments where an agent's trace can be replayed, scored and
trusted: a world generated from a grammar with a seed, tools the world
enforces, a log nothing can rewrite, verifiers that read final state and the
log, and a loop that survives timeouts, retries and cancellation.

Short term: a stateful SQLite world with two typed tools, twenty tasks with a
checkable outcome, a bare agent loop, and a baseline of two models on it.

Rules of this file:

- A line below exists only if it has a test. Growing this file costs a test.
- A test sees the system through the public API and the fake provider's
  recording, and reaches the raw connection only to play the adversary or to
  move storage. It knows nothing about modules or repositories.
- There are exactly as many test files as lines below. A new file needs a new
  line, and the PR says why an existing test could not be strengthened.

## Invariants of worldlab

1. Digest is canonical: two worlds in one state give one digest, whatever SQLite did with pages. `tests/test_digest.py`
2. Events are append-only within an episode: a written row survives UPDATE, DELETE and REPLACE unchanged, each row carries the hash of the one before, and reset starts an empty log. `tests/test_events.py`

## Non-goals

A framework. A second runtime next to the first. Hashing the SQLite file.
Training runs before the environment holds its invariants.
