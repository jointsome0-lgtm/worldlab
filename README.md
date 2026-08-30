# worldlab

Agentic training environments: a seeded world with typed tools, an append-only
event log, tasks with checkable outcomes, and an agent loop that runs on it.

Where we are going: `GOALS.md`. Why things are this way: `git log`. Rules for
agents: `AGENTS.md`. The plan, the current position and the gate checklist
live in the journal repository, `../learn-storybuilding-rl`.

## Map

One line per directory. Hidden directories (`.claude/`, `.github/`) are harness
and CI config and stay out of the map.

- `scripts/`: `limits.py`, the one repository check: token budget, map, goals ↔ tests by name, four Markdown files only, test imports, zero comments.
- `worldlab/`: the package: `env/` now, later `tasks/`, `verifiers/`, `agent_core/`, `episode_runtime/`, `eval/`.
- `worldlab/env/`: the SQLite world, its tools and its digest.
- `tests/`: one file per line of `GOALS.md`; they see the system only through `worldlab.testing`.
