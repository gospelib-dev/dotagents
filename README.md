# dotagents

Lance's shared, tool-neutral material for AI agents: skills, instruction snippets and decision logs.
Any agent harness (Hermes, Claude Code, Codex, others) loads it from a read-only checkout and keeps it
current with a scheduled pull.

| Path | What |
| --- | --- |
| `skills/<name>/SKILL.md` | Agent Skills (agentskills.io format). First: `engineering-principles`. |
| `instructions/` | Tool-neutral snippets for project `AGENTS.md` files. |
| `decisions/` | Decision logs that span more than one skill. |

Rules for this repo: nothing private (no household or personal details), no credentials, no
harness-specific steps. Changes arrive by pull request; Lance merges.
