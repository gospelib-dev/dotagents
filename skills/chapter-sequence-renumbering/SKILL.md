---
name: chapter-sequence-renumbering
description: Use when chapters are added, removed, merged or split. Safe renames, refs.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Chapter sequence renumbering

After a structural change to a manuscript's chapter sequence, renumber chapter files and folders and
every cross-reference to them, without collisions and without leaving stale numbers in outlines,
continuity tables, character sheets or indexes. Plan first, execute in a safe order, then verify.

## When to use

- **Remove** chapter N: chapters > N decrement by 1.
- **Insert** at N: chapters ≥ N increment by 1.
- **Merge** N and N+1: N+1's content joins N; chapters > N+1 decrement by 1.
- **Split** N into N and N+1: chapters > N increment by 1.

## Method

### 1. Pin the change and the layout

Record the operation, the affected chapter(s), the zero-padding width (e.g. `chapter-07`), and every
place chapters live: prose files, per-chapter planning folders, act or part groupings. Decide whether a
change **cascades** across act/part boundaries (default: numbering is global) or stays inside one act,
which then needs manual boundary adjustment. Work on a branch; never on a dirty tree.

### 2. Generate a plan before touching anything

Produce (by script where possible) the old → new mapping, the rename commands in safe order, and every
file and line that references an affected number. Review the plan; do not execute blind.

### 3. Rename in collision-safe order

Always move a chapter into a slot that is already empty: when shifting **up**, start from the
**highest** number; when shifting **down**, start from the **lowest** number after the gap.
- **Decrement (remove/merge):** rename ascending after the gap: 11→10, 12→11, 13→12. The target slot is
  always free because the chapter that occupied it was just moved or deleted.
- **Increment (insert/split):** rename descending: 14→15, 13→14, … 10→11, then create the new chapter.

If unsure, rename everything to temporary names (`chapter-11.tmp`) first, then to final names. Use
`git mv` so history follows the files.

### 4. Update every reference class

Search with regexes and fix by mapping, never by blind global replace (a value can be both an old and a
new number):
- folder/file paths: `chapter-(\d{2})`, `chapter-(\d{2})\.md`
- prose and notes: `[Cc]hapter[\s-]?(\d{1,2})`, `[Cc]h[\s.-]?(\d{1,2})`, spelled-out numbers ("chapter eight")
- tables: `\|\s*(\d{1,2})\s*\|` in chapter, timeline, continuity and first-appearance tables
- navigation links (Previous/Next), cross-act relative links, frontmatter chapter numbers
- line-anchored citations (`ch3#L55`, `chapter-03.md#L237`): the number and possibly the line

Apply replacements from a mapping in one pass (or via placeholders) so 11→10 and 10→9 cannot chain.

### 5. Regenerate dependents

Rebuild indexes, search mirrors or knowledge graphs that ingest the story files, and any generated
artifacts (book builds) that embed chapter numbers.

## Verification

- Chapter folders and files are sequential: no gaps, no duplicates (`ls -d <dir>/chapter-*/ | sort -V`).
- Prose files match planning folders one to one.
- Act/part tables, prev/next links and first-appearance references updated.
- No broken links: `rg "\]\([^)]+chapter-" --type md` and a link checker.
- Frontmatter numbers match file names.
- `git diff --stat` shows only intended files; prose content of moved chapters is unchanged apart from
  numbering.

## Pitfalls

- Collisions from renaming in the wrong order.
- Chained replacements (11→10 then 10→9) from sequential global substitutions.
- Missed classes: spelled-out numbers, table cells, line-anchored citations, frontmatter.
- Act boundaries silently shifting when the change cascades.
- Contiguous one-chapter shifts left in canon tables later masquerade as many separate continuity errors;
  fix them as one range (see `story-continuity-audit`).

## Project specifics

The project's own skill supplies: the directory layout and act/part chapter ranges, the planning-folder
contents, the plan-generation script, which files carry chapter references, and which indexes must be
re-ingested afterwards.
