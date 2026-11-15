---
name: initiative-inventory-mapping
description: Use when mapping an in-flight initiative into proposed tracker tasks.
metadata:
  version: "0.1.0"
  status: draft
  owner: maintainer
---

# Initiative inventory mapping

Produce a read-only **inventory map** of an in-progress initiative (a directory of plans, ledgers,
decisions and open PRs) that proposes the tracker goal, lasting work products ("cases") and owed
tasks *before* anyone creates them. The map is reviewed and approved first; another role turns it
into tracker objects. You create nothing except the map document.

## When to use

- A task asks what it takes to move an initiative into the tracker, or for a map to review before
  objects are created.
- Not for creating the objects (that is a plans-to-tasks conversion after approval).

## Principles

- **The repo docs are the source of truth.** A case *links* to a file and never copies it.
- **Every row cites its source**: `path#heading` (a real anchor), a PR number, or the exact command
  whose output proves it. When a row rests on the owner's words, quote them verbatim and say whether
  the record marks them owner-verbatim or second-hand.
- **Drop nothing.** Anything owed becomes a task. Anything that looks obsolete goes under gaps for
  the owner to decide, never into a quiet omission.
- **Make the owner's steps visible.** Merges, picks, judgements and rulings get the owner as
  assignee: the owner's review time is the serial resource.
- **Say exactly what you changed** ("only this map document was saved"), not "nothing changed".

## Procedure

1. **Read-only worktree** at the integration tip, detached; no branch, no PR; remove it at the end.
2. **Read selectively.** README and its read-in-order table; the status file (it holds the claims to
   verify); the "still yours to answer" part of the open-questions file; headings of the big ledgers
   (`grep -n '^#'`), then only the sections the task names. Count words first; ledgers can be huge.
3. **Run the initiative's own checker**, quoting its last line and exit code.
4. **Live PRs.** For each: immutable head SHA, base (a base other than the integration branch means
   stacked), review verdicts with full bodies (their findings become the fix task's "done means").
   Fetch PR trees into remote-tracking refs (`git fetch origin pull/N/head:refs/remotes/pr/N`) rather
   than local branches that may be checked out elsewhere, and read with `git show`; `git grep` over
   trees with large fixtures can hang. Delete the refs at the end.
5. **Tracker state.** Goals, projects, agents; search for every PR number and initiative keyword.
   Map existing items to steps instead of proposing duplicates; note items pinned to an old PR head
   (they cannot cover a new one) and projects with no goal.
6. **Verify the docs against git and the forge**: branches the docs say to delete still exist?
   PRs called open still open? Claims that something landed? Resolve relative links in *generated*
   files from the generated file's own directory.
7. **Write the map**, save it as the task's document, read it back, then hand off for review.

## Map shape

1. **Goal.** One goal, in the owner's own words for the outcome (their definition of done), with the
   parent goal named.
2. **Cases.** Lasting work products only: ledgers, session logs, tooling, option documents,
   measurements, spikes, and one review case per PR **head** (key it `pr-<N>@<head8>`). Not one per
   decision or row. A small case-type vocabulary in a table; stable keys; exact lifecycle status
   values with rationale in a separate note column. A case whose doneness is an open gap is "in
   review". Attach cases to the project, not to an invented container case.
3. **Tasks.** Every owed step in order, grouped into tracks:
   `title | assignee | done means | blocked by | existing item | source`.
   - A re-review at a new head is a new task; never reuse a review pinned to an old head.
   - Include owed work nothing owns yet: commitments the owner's answers created with no plan,
     file or item behind them.
   - Do not invent blockers. Where docs set no order, say so and list the ordering as an owner
     decision under gaps.
4. **Gaps and conflicts**: doc claims contradicted by git/forge; stale status lines; owner state
   stored outside the repo; stacked PRs the review sweep misses; duplicate or dead items; live
   defects the record mentions; work with no tracker home; sequencing only the owner can set. Each
   gap names who acts.

## Review-proofing (lessons from rejected maps)

- **Citations on every row**, cases and gaps included. Bare filenames, dates, "same as above", "as
  T10", prose pointers ("row N", "the review report") and bare commands are rejected; commands come
  after the citation as corroboration. Long paths get an alias legend at the top. Use full repo
  paths in case links.
- **Check anchors and quotes by script before saving**: slug each heading GitHub-style
  (`re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-')`, skipping code fences) from `git show
  <ref>:<path>` and fail on any miss; compare every quoted string with the source after normalising
  whitespace and `**`; check every table row has a citation.
- **Generate task tables from a script** (keys → numbers, dependencies → ID ranges) and check
  topological order (no row blocked by a later row) and role/"done means" coverage on every row.
- **Blockers are task IDs or PRs only**, never "track D" or "owner sequencing". Model owner
  deferrals as owner tasks ("sequence or transfer, never drop") and block affected rows on them.
- **Review and baseline tasks are blocked by every build task they verify**; the final close is
  blocked by every other task. A transferred obligation counts only when its receiving task exists.
- **Owed work is the whole chain**: "re-plan X" means plan → review → run → cross-model review →
  owner accepts, plus any later spike named. "Ships before launch" means design options → owner
  picks → build, review, QA.
- **"Agent drafts, owner approves"** is two tasks; later gates depend on the owner task. Add an owner
  gate only where an owner ruling requires it, and quote the ruling.
- **"Done" never allows "or states why it can't".** Give an unfinishable row a named blocking task.
- **Long implementation tasks** get startable slices plus a final completion gate blocked on every
  slice and on the closed scope list.
- **Read residue sentences** inside long register entries ("also found… not built", "open item",
  "owed", "left open on the owner's instruction"): each is a task row.
- **Never collapse a plan's roster into one row.** Build a crosswalk: each batch, the files it names,
  and their live state. For migrations, an import is not completion: expand each batch's globs and
  scan surviving files for imports of predecessors the plan deletes; hits make "finish" tasks, every
  other batch gets a "verify" task, never "done". Files no batch owns go to the owner as gaps.
- **List every unresolved measured row**, partial as well as blocked, with counts from the latest
  stacked head. Don't hard-code counts an earlier task will change ("every choice", not "122").
- **Grep each hand-off a task executes for hook bypasses** (`--no-verify`) or other project-rule
  violations; if found, add a gap and a prerequisite task to fix the procedure.

## Pitfalls

- "Merged" is not "approved": contracts and plans can be merged and still be proposals.
- Generated docs lag their sources; check dates against the ledgers' ruling lines before quoting a
  summary line.
- When a promised deliverable has no artifact, grep the data files too, not only the prose.
- When you cannot re-run a check, say so and cite who ran it; don't present it as verified.
- Count branch-only docs per directory with `git ls-tree`; don't count docs on other branches.

## Verification

Anchor, quote, citation-per-row, topological-order and role/done-coverage scripts all pass; the map
was read back after saving; the hand-off states exactly what changed.

## Project specifics

The project's mapping skill or `AGENTS.md` supplies the initiative directory layout, its checker,
the tracker's object model, case-type vocabulary and status values, the project rules to grep for,
and who reviews and who creates the objects.
