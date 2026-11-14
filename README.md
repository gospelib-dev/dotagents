# dotagents

Lance's shared, tool-neutral material for AI agents: skills, instruction snippets and decision logs.
Any agent harness (Hermes, Claude Code, Codex, others) loads it from a read-only checkout and keeps it
current with a scheduled pull.

| Path | What |
| --- | --- |
| `skills/<name>/SKILL.md` | Agent Skills (agentskills.io format). |
| `instructions/` | Tool-neutral snippets for project `AGENTS.md` files. |
| `decisions/` | Decision logs that span more than one skill. |

## Skills

| Skill | For | Use when |
| --- | --- | --- |
| `engineering-principles` | every agent that writes, reviews or fixes code | writing, reviewing or fixing code; includes the review and fix-the-class protocols |
| `fixing-a-wrong-memory` | every agent with long-term memory | someone corrects you, or a stored memory turns out wrong |

## How agents load it

- Hermes: each gateway host keeps a read-only checkout at `/opt/dotagents` (pulled every 15 minutes) and each
  profile lists `/opt/dotagents/skills` in `skills.external_dirs`. A profile that should not see a skill lists
  it in `skills.disabled`.
- Other harnesses: point their skills directory (or a symlink) at `skills/` in a read-only checkout.
- Project rules: add the router line from `instructions/agents-md-router.md` to a repo's `AGENTS.md`.

Rules for this repo: nothing private (no household or personal details), no credentials, no
harness-specific steps beyond short tool examples. Changes arrive by pull request; Lance merges.
