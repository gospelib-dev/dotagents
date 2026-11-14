---
name: manuscript-book-build
description: Use when building or verifying DOCX/EPUB from chapters. Inspect real output.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Manuscript book build and verification

Build reader deliverables (DOCX, EPUB 3, later print PDF) from ordered chapter sources, or verify
someone else's build, without changing the text and without trusting converter defaults. Exit code 0
and a non-empty file prove nothing: open the containers and check their structure. Bounded ZIP/XML
recipes: `references/pandoc-structural-validation.md`. One-shot inspector: `scripts/inspect_book.py`.

## When to use

- Producing or regenerating a whole-book DOCX/EPUB from chapter files.
- Adding a repeatable build script, word count or format validator.
- Reviewing a PR or run that produces manuscript files (Pandoc script, an app's export, any tool).
- Building a reader artifact at a frozen revision for reader-knowledge checks (see
  `story-continuity-audit`).

Do not revise prose or canon here unless the task separately authorizes source edits.

## Build procedure

1. **Source contract.** Read the expected chapter count, filename pattern, order, title, subtitle,
   formats and validator. Fail before invoking the converter if the count differs or any expected file is
   missing (a missing chapter plus an extra file can preserve the total). Keep sources read-only; put all
   intermediates and outputs in an ignored build directory.
2. **One stripped intermediate.** Concatenate chapters in numeric order. Remove HTML comments (inline,
   multiline, same-line), `[//]: #` lines and the project's internal-note markers while preserving prose,
   headings, italics, code-like story text and scene breaks. An unterminated comment is an error (non-zero
   exit), never a silent deletion of the rest of the book. Derive every format and the word count from
   this same intermediate.
3. **Declare the converter version.** Check `pandoc --version` before writing any output. `--split-level`
   needs Pandoc 3+ (2.x used `--epub-chapter-level`); distro packages are often 2.x, so make install advice
   match the flags. A version guard must run before the first output, or 2.x writes a new DOCX and then
   fails on the EPUB, leaving a stale EPUB beside it. Never vendor the binary into the repo.
4. **Format-specific structure, deliberately.**
   - DOCX: a raw OpenXML page-break block before every chapter. Default heading styles have no
     `pageBreakBefore`; a single break after the title page leaves chapters running on.
   - EPUB 3: `--split-level=N` where N is the chapter-heading level, plus `--toc` and the intended
     `--toc-depth`. TOC depth controls navigation entries; it does not split spine documents.
   - Supply title, subtitle/series, language and other metadata explicitly.
5. **One reproducible word count.** Pandoc `-t plain` on the stripped intermediate, then count words;
   print exactly one labelled figure. Headings and scene-break glyphs are included; keep title metadata
   outside the intermediate if the declared count is prose-plus-headings.
6. **Test the wrapper before the real build.** Cover wrong count, missing-plus-extra file, comment
   stripping, unterminated comment, required flags, and the number of chapter page-break blocks. Put a
   fake `pandoc` first on `PATH` that rejects a missing `--split-level`, captures the intermediate and
   writes minimal fake artifacts. In Bash tests use `if cmd; then fail; fi` for negative assertions;
   `! cmd` is exempt from `set -e`.
7. **Real build, then inspect internals** (below).
8. **Deliver only the verified revision.** Report word count, Pandoc version, structural checks and the
   validator result. When replacing artifacts after review, upload the revised files and archive the old
   ones so the latest is unambiguous. Re-run cross-model review after any change to flags or structure.

## Verification procedure (also for reviewing someone else's build)

1. Get the diff without depending on a forge CLI: `git fetch origin`, `git log origin/main..origin/<b>`,
   `git diff origin/main...origin/<b>`; check out detached in your own worktree. Never review your own
   model family's work.
2. Get the tool locally, never committed: download the official Pandoc release tarball into a scratch dir
   and prepend its `bin` to `PATH` for the run only. Do not reuse another agent's scratch copy. Run
   `epubcheck` only if already installed (or installation was approved); otherwise report `not available`.
3. Run the checks the task names (`bash -n`, the test script, the build) and paste exact output.
4. Inspect: `python3 scripts/inspect_book.py <build_dir>/ <basename>` prints, for DOCX, the first paragraphs
   with styles and page breaks, every heading in order, style counts, the `w:type="page"` count, scene-break
   candidates and leaked markers; for EPUB, whether `mimetype` is first, the OPF package version, title and
   language, nav TOC entries, dangling hrefs, the size of every spine XHTML, and leaked markers.
5. Cross-check against the source: count the scene-break glyph and chapter headings in the chapter files;
   output counts must match.
6. Repo hygiene: `git diff --quiet origin/main -- <chapters dir>`, `git check-ignore -v build/ build/<file>`,
   clean `git status --short`; delete build outputs afterwards.
7. Before proposing a fix, test it: re-run the converter with the changed flag on the intermediate the
   script leaves behind and report the measured result.
8. Report findings first (each a class with file:line evidence and severity: should-fix or nit), then
   commands and results. Do not merge.

## Pitfalls (check every time)

- **EPUB split level vs heading level.** Pandoc splits at level 1 by default. With `##` chapters the whole
  book becomes one huge XHTML; the TOC still "works" through anchors, so naive acceptance passes while
  e-readers struggle. Always record spine-item sizes.
- **No H1 means a synthetic TOC entry.** Pandoc adds an unnumbered H1 named after the title: the nav has
  N+1 entries. Count entries against chapters. With `--toc-depth` below the chapter-title heading level,
  the nav shows only "CHAPTER N" without titles.
- **The synthetic title section survives obvious flags.** With `--split-level=2` it becomes a near-empty
  file (~550 B, a blank page in readers); neither `--shift-heading-level-by=-1` nor removing raw blocks
  removes it. Report as a nit; do not promise a flag fix.
- **Raw format blocks are dropped from other outputs.** An `{=openxml}` block silently vanishes from EPUB;
  check it did not leak into XHTML as text.
- **Front matter shifts reader positions.** Title and contents pages precede chapter 1 in some builds,
  shifting spine indices. Never assume a chapter mapping after a rebuild; confirm the returned title.
- Never equate a TOC with healthy packaging, headings with DOCX pagination, or file existence/size with a
  valid package.

## Project specifics

The project's own skill supplies: the chapter directory and filename pattern, chapter count and heading
level, scene-break glyph, internal-marker conventions, title/series metadata, the build script and output
names, where the canonical reader artifact lives and who may write it, its revision-stamp file, and the
chapter mapping of the current build.
