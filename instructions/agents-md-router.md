# Pointer line for a project's AGENTS.md

Add this near the top of a repo's root `AGENTS.md` (create the file if the repo has none) instead of restating
shared principles:

> Shared agent skills live in [lellimecnar/dotagents](https://github.com/lellimecnar/dotagents) (`skills/`).
> Every agent follows `use-existing-solutions-first`; coding, review and fixing follow `engineering-principles`.
> The rules in this file apply those skills to this project; where they conflict, raise it with the owner.

Hermes agents already have these skills installed from the dotagents tap. Other harnesses (Claude Code, Codex,
OpenCode) can load them from the repo's `skills/` folder.
