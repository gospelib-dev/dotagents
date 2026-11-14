# dotagents

Lance's shared, tool-neutral material for AI agents: generalized skills that any agent of a given type can
use (any code reviewer, any fiction editor, any schedule planner...), instruction snippets and decision logs.
Project-specific facts stay in each project's own skills and `AGENTS.md`; those point back here for method.

| Path | What |
| --- | --- |
| `skills/<agent-type>/<name>/SKILL.md` | Agent Skills (agentskills.io format), grouped by agent type. |
| `instructions/` | Tool-neutral snippets for project `AGENTS.md` files. |
| `decisions/` | Decision logs that span more than one skill. |

## Skills by agent type

Each folder under `skills/` is one agent type. A profile loads the folders that match its job.

### `common/` — every agent (1)

| Skill | Use when |
| --- | --- |
| `fixing-a-wrong-memory` | you are corrected or find a stored memory is wrong. Delete every copy, save once |

### `engineering/` — agents that write, review, test or ship code (16)

| Skill | Use when |
| --- | --- |
| `audio-pipeline-verification` | building or reviewing TTS/audio render or export. Measure, don't echo |
| `backlog-grooming` | grooming a backlog: one state per item, verify claims, owner unblocks |
| `coding-task-intake` | taking a coding task end to end: intake, build, verify, PR, report |
| `credential-gated-runner` | building a sudo-gated runner that keeps secrets away from agents |
| `dependency-update-review` | triaging bot dependency PRs or lockfile changes. Reconcile, verdict |
| `docs-drift-sweep` | keeping project docs in step with merged code, or reviewing a docs PR |
| `engineering-principles` | writing, reviewing or fixing code. Principles plus review and fix-the-class protocols |
| `initiative-inventory-mapping` | mapping an in-flight initiative into proposed tracker tasks |
| `local-web-app-hardening` | building or reviewing a loopback/local web app. Boundaries, limits |
| `merge-queue-stewardship` | admitting approved PRs to a merge queue or checking trains flowed |
| `pull-request-review` | reviewing another agent's PR. Verify claims, pin head, one verdict |
| `qa-acceptance-evidence` | QA-accepting a change. Oracle, risk-ranked tests, evidence verdicts |
| `tech-debt-ranking` | producing a recurring ranked, deduped tech-debt backlog. No code edits |
| `test-lanes-and-coverage` | judging a test suite: lanes, branch-coverage ratchet, perf budgets |
| `web-accessibility-check` | building, reviewing or accepting UI. WCAG 2.2 AA checks and tools |
| `work-planning` | a plan or spec is requested, or uncertainty must be resolved before work |

### `ops/` — agents that triage alerts or inspect infrastructure (2)

| Skill | Use when |
| --- | --- |
| `alert-triage` | an alert webhook wakes you. Dedupe by fingerprint, diagnose read-only |
| `readonly-infrastructure-inspection` | inspecting servers, storage, backups or networks with read-only keys |

### `writing/` — fiction and book-production agents (16)

| Skill | Use when |
| --- | --- |
| `chapter-sequence-renumbering` | chapters are added, removed, merged or split. Safe renames, refs |
| `conlang-usage-review` | reviewing invented-language use in fiction. Form, meaning, gating |
| `dialogue-voice-review` | reviewing dialogue, character voice or relationship beats in fiction |
| `editorial-production-management` | planning a book's editing/publishing pipeline. Stages, gates, routes |
| `fiction-manuscript-editing` | editing fiction: developmental, line, copy. Staged passes, notes |
| `fiction-pacing-review` | reviewing fiction pacing, structure, tension or hooks. Diagnostics |
| `fiction-prose-craft` | drafting or revising fiction scenes. Outside-in craft tests, fixes |
| `layered-chapter-drafting` | drafting a chapter from an outline. Brief, layered passes, gates |
| `manuscript-book-build` | building or verifying DOCX/EPUB from chapters. Inspect real output |
| `manuscript-readiness-assessment` | judging if a chapter is publish-ready. Full rubric, ranked fixes |
| `markdown-section-extraction` | pulling sections from big markdown files by heading. Script |
| `originality-check` | checking a manuscript for copied text or derivative concepts |
| `prose-text-analysis` | measuring prose: readability, n-grams, overuse, avoid-list hits |
| `science-plausibility-review` | reviewing science/tech plausibility in fiction. Smallest fix |
| `story-continuity-audit` | checking story canon/continuity against prose. Cited ledgers |
| `story-expertise-seeding` | a book-team agent must build cited story and field expertise |

### `organizing/` — professional-organizer agents (6)

| Skill | Use when |
| --- | --- |
| `clutter-feelings-and-hoarding` | clutter work hits sentiment, guilt, family conflict or hoarding signs |
| `decluttering-method-guide` | choosing a decluttering method, room order, session plan or keep rule |
| `household-paper-flow` | setting up a home paper flow, record retention, scanning or shredding |
| `organizing-for-adhd-households` | designing organizing systems for ADHD, sensory or support-needs homes |
| `room-organizing-playbooks` | organizing a specific room or zone, or when storage safety is in play |
| `unwanted-item-routing` | deciding if an unwanted item is sold, donated, recycled or trashed |

### `planning/` — schedule-planner and task-manager agents (2)

| Skill | Use when |
| --- | --- |
| `capacity-first-scheduling` | building or repairing a week or day of time boxes, ADHD-aware |
| `task-triage-and-rating` | capturing, rating, ranking or breaking down tasks, incl. from email |

### `finance/` — household-finance agents (2)

| Skill | Use when |
| --- | --- |
| `household-money-guidance` | answering household money, bill, debt or cash-flow questions |
| `reconciled-spending-reports` | reporting household spending, income or balances to the exact cent |

### `assistant/` — personal-assistant agents (6)

| Skill | Use when |
| --- | --- |
| `daily-brief` | writing a person's morning brief or building today's plan for them |
| `evening-check-in` | running an evening check-in, a reflection or a goal review |
| `household-request-capture` | someone asks their assistant to track a chore, home item or project |
| `owned-calendar-stewardship` | an assistant owns a person's calendar and must plan, mirror or fix it |
| `person-profile-seeding` | building or refreshing a person's notes from their read-only accounts |
| `smart-home-request-handling` | relaying or doing a request to read or change smart-home devices |

### `lance-facing/` — any agent that talks with Lance directly (1)

| Skill | Use when |
| --- | --- |
| `i-have-adhd` | 'Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across  |

## How agents load it

- Hermes: each gateway host keeps a read-only checkout at `/opt/dotagents` (pulled every 15 minutes). Each
  profile lists the agent-type folders it needs in `skills.external_dirs`, always including
  `/opt/dotagents/skills/common`.
- Other harnesses: each `skills/<agent-type>/` folder is a flat, spec-compliant skills root
  (`<name>/SKILL.md`). Point the harness at the folders it needs. Don't use `skills/` itself as a single
  `~/.agents/skills`: the Agent Skills layout is flat, and most tools do not search nested folders.
- Project rules: add the router line from `instructions/agents-md-router.md` to a repo's `AGENTS.md`.

## Writing a skill here

- Generalize: the method or expertise any agent of that type needs. Project facts (people, repos, paths,
  accounts, story content, household details) go in the project's own skill, which starts with
  "Method: follow the shared `<skill>` skill".
- Principles with judgment, not rigid rules. Keep sources cited. Under ~12 KB per SKILL.md; depth in `references/`.
- Nothing private (no household or personal details), no credentials, no hostnames or internal addresses,
  no harness-specific steps beyond short tool examples. `lance-facing/` is the one exception by design.
- Changes arrive by pull request; Lance merges.
