# Agent guide

worldlab is the code side of a preparation for a research engineer role in
agentic training environments. The plan, the current position and the gate
checklist live next door in `../learn-storybuilding-rl`; this repository holds
code, tests and nothing else.

## Who writes what

The goal is that Agniv understands the code and can apply it without help.
Design decisions are talked through before any code. Code that carries a
decision, Agniv writes: contracts, invariants, tests for them, the loop.
Boilerplate the agent may write after the design is agreed, and it explains
it. Test: if Agniv could not rewrite a piece from memory in ten minutes, it is
his to write.

## Three sources of truth, one each

- The past: git. Every commit says why, not just what. A commit without a
  reason does not merge. There is no decision log; `git log` is the log.
- The present: the code. There is no design document. If the code and a text
  disagree, the text is wrong.
- The future: `GOALS.md`. Direction, invariants, base state. Every line names
  its test; a line without a test does not enter.

Read in this order: `GOALS.md`, the map in `README.md`, the issue or PR you
are on, then code and tests. Before changing a thing, `git log -S<term>`: the
reason it is the way it is lives there, not in a file.

## Limiters (numbers checked in CI, not conventions)

All of them live in one script, `scripts/limits.py`, run by
`.github/workflows/limits.yml` on every PR.

- Budget: the whole repository fits in 100k tokens (bytes ÷ 4), counting
  every tracked file except `LICENSE` and lock files. There are no generated
  or vendored files; the first one that appears is excluded in the same PR,
  with its reason in the commit. A PR that crosses the budget fails. The
  number is never raised in the PR that needs it; when a subsystem cannot
  fit, it becomes its own repository with an executable contract.
- Map: one line per directory, at most 250 characters, in `README.md`. The
  script fails on a directory without a line or a line without a directory.
  Hidden directories are outside the map.
- Every goal line names its test file and every test file is named by a goal
  line. Adding a test file means adding a goal line, and the PR says why an
  existing test could not be strengthened instead.
- Tests reach the system only through the public API and the fake provider's
  recording: the only `worldlab` import allowed in `tests/` is
  `worldlab.testing`.
- Zero comments and zero docstrings in Python, including inline ones. Only
  machine markers (`# noqa`, `# type: ignore`, shebang) are exempt. A
  function that needs a paragraph needs a better name, a split, or a test.
- No process artifacts in the repository: the only Markdown files are
  `GOALS.md`, `AGENTS.md`, `README.md`, `CLAUDE.md`; any other `.md` fails.
  Scope lives in the issue, findings in the PR, reasons in the commit.

## Code boundaries

- `agent_core/` is how the model sees the task: provider, messages, tools,
  loop, context.
- `episode_runtime/` is how it runs reliably: lifecycle, runner, retries,
  idempotency, cancellation, provenance.
- `eval/` holds tasks, scorers, traces, analysis.
- Never build two overlapping runtimes. The append-only event log exists from
  the first commit that has a world.
- The world is generated from an explicit grammar with a seed.

## Rules that carried over

- `uv`, `ruff`, Python 3.12+, SQLite. No Docker without explicit approval.
- No live provider calls from tests.
- Secrets live outside the repository and outside the sandbox. Deny-by-default
  egress for agents.
- One experiment costs at most $60 until month 6. Anything above that needs a
  commit in the journal repository before launch. Ask before spending money,
  publishing anything, or deleting data.
- Money is integer microdollars, and every figure is labeled estimate or
  reported.
- Never commit `.env`, credentials, or raw prompts and responses. Own traces
  go public only after sanitization.
- Git worktrees only in `.worktrees/<name>`; the primary checkout stays on a
  clean `main`. One coherent slice per PR.
- Merge process, the only review gate: push; the Codex bot reviews every push
  to a PR that is ready for review; a 👍 means merge, findings mean fix, push,
  and wait again (the `watch` skill runs this loop).

## Writing

Everything is in English. Commit messages, issues and PR descriptions are the
only prose this project keeps, so they run through `unslop` before they are
posted. A commit says the decision and its reason, short. An issue says what
is wanted and how anyone will know it is done. A PR says what changed, why,
and how it was verified. No filler, no restating the diff.
