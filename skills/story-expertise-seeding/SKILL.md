---
name: story-expertise-seeding
description: Use when a book-team agent must build cited story and field expertise.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Story and field expertise seeding

How an agent on a book project (author, editor, continuity keeper, reviewer, production lead,
engineer) becomes (1) an expert in *this* story through the lens of its role and (2) a subject-matter
expert in its field, before doing real work. Everything stored must be **true, cited and useful for the
job**. Memory you cannot cite is worse than no memory.

## When to use

Onboarding a new role agent, re-seeding after major canon changes, or reviewing another agent's seeded
knowledge.

## Where knowledge goes (never mix them)

| What | Where |
|---|---|
| Role-lens synthesis of the story (durable, shared, reviewable) | a dossier file in the project repo, on its own branch, reviewed like code |
| Working memory: the facts needed most often | a "Key facts" list at the top of that dossier |
| Field expertise (craft, science, linguistics, engineering) | a craft skill for the role (generic method in shared skills, project application in a local skill) |

Do not copy canon wholesale into memory: canon already lives in the story files and their search mirror;
search it. Never write conclusions about the owner while seeding, and never write directly to the canon
mirror; canon changes only through merged story files.

## Part 1: story expertise

1. **Read the files, not summaries**, in a throwaway detached checkout so your own branch is untouched.
   If several workers may run at once, give the checkout a unique path and never remove another worker's.
   Read the binding plan and decided no-ops first: they bind everything. Use
   `markdown-section-extraction` for big files.
2. **Write the dossier** (roughly 200–450 lines) in your role's lens:
   - every claim carries a source (`path §heading` or `chNN:line`);
   - lists, tables and per-character / per-chapter maps beat prose;
   - a **Contradictions and open questions** section: real inconsistencies between files, each with both
     sources. Do not fix them here; they become owner triage work.
   - end with a **Self-test**: about 12 hard questions a newcomer would get wrong, each with answer and source.
3. **Key facts:** at the top, a numbered list of the 50–90 facts and rules you will need most often, each
   self-contained and cited. These reach shared memory through review and merge, not by direct writes.
4. **Check retrieval:** answer a few self-test questions using the canon search mirror plus your dossier;
   any fact canon search could not answer must be in Key facts.
5. **Commit** only the dossier on its knowledge branch and push; leave PR bundling to the coordinator.
   Report: lines, key-fact count, branch, the full contradictions list, anything unfinished.

## Part 2: field expertise (the craft skill)

1. **Research with source ranking:** primary and authoritative works first (published craft books and
   their authors' own writing, peer-reviewed papers, standards bodies, official docs), then reputable
   practitioners; never forums or AI-generated pages as sole support. Every non-obvious claim gets
   author, title and URL or publication. If you cannot verify something, leave it out or mark it
   "unverified". Never invent a citation; use a citation checker if available.
2. **Write the skill:** what an expert in the role checks, in order; the diagnostic tests and thresholds
   you will actually apply; common failure modes and fixes; how each applies to this book (genre,
   audience, characters, chapters, languages). Keep SKILL.md short; put frameworks, worked examples,
   terminology and the sources list in `references/`. Generic method belongs in a shared skill; book facts
   stay in the project skill.
3. **Apply it once:** run the checklist on one chapter and report about five concrete findings
   (`chNN:line`, what, why, fix), so the skill is proven on real text.

## Part 3: cross-family review of dossiers

For each dossier: verify about 15 random claims plus every claim in Contradictions against the cited
file, and spot-check about 10 key facts. List wrong or unsupported claims with the correct text and
source. For each agent with errors, open one fix task assigned to that agent with every correction.
Report `wrong/checked` per role. Reviewers come from a different model family than the author.

## Pitfalls

- Summaries of summaries: always cite the primary file and line.
- "Fixing" contradictions inside the dossier: they belong to the owner.
- Memory writes that bypass review.
- Uncited key facts; self-tests with easy questions.
- Field claims resting on one secondary source.

## Project specifics

The project's own skill supplies: the dossier path and branch naming, reading lists per role, the canon
mirror and its tools, which memory writes are allowed when, the craft-skill naming convention, review
assignment and task conventions.
