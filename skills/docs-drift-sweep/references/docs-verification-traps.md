# Docs verification traps

Checks and rendering traps that let wrong prose pass. Use them when writing a docs fix and when
reviewing a docs PR.

## Checkers that prove nothing

- **Changed-files mode.** Link/anchor checkers wired for lint-staged often default to "files passed
  as arguments"; with none, they print nothing and exit 0. Always run the full-scan flag and confirm
  the output reports a count of links and files.
- **Anchor checkers ignore links without an anchor.** A plain relative link (`[X](X.md)`) in a file
  that is *copied or generated elsewhere* can be broken in one location and pass. Grep such files for
  relative links (`\]\([^h#)][^)]*\)`) and resolve each from every location the file lives. An
  absolute URL to the canonical branch is often the right fix, not `../`.
- **Prose pointers are invisible to link checkers.** When a heading is renamed, grep the page for
  plain-text references to the old heading ("see the backlog below").
- **`git diff --check` with no range** on a clean tree checks nothing; use `<base>...HEAD`.
- **Formatter "pass" is not "renders right"** (next section).

## Formatters can change rendered emphasis

When a markdown formatter reflows a paragraph containing a bare identifier with an underscore
(`node_type's`) next to `_emphasis_`, it can rewrite the text to something like
`node*type's \_own*`. The file still passes the formatter's check, but a different span now renders
in italics. Look for added lines matching `\\_` or `[a-z]\*[a-z]`. Confirm by rendering both
versions (for example `micromark(text)` or walking an mdast tree for `emphasis` nodes) and comparing
where `<em>` falls. Fix: put the identifier in a code span.

## Claims that must be re-verified

- **"X lives in file Y"** — grep Y for X. Authors often cite the main workflow or module for
  something in a sibling.
- **"Job X runs when Y changes"** — open that job's `if:`. Some jobs gate only on the base branch,
  not on path filters, and cover more than the prose says. Grep instruction files for sibling copies
  of any CI claim the PR rewrites.
- **Removed names** — when a job, setting or command is removed, grep the whole tree (including
  `.github/*.md`, instruction files, tool READMEs) for the old name, not just the docs root.
- **"Add a note wherever a page says Z"** — grep every docs root and instruction file for Z's wording
  and URLs. Authors fix the pages they had open and skip the siblings.
- **Dated status notes** ("not active yet because…", "returns error N") can go stale between the
  author's push and your review. Re-probe each stated cause against the provider now. A note whose
  conclusion still holds but whose stated *reason* is false is still wrong.
- **Environment-specific endpoint sweeps** cover the whole docs root, including verify steps and
  table rows, not just the operations section.

## Documented commands must run

For every new shell block that runs a repo script, grep the script for each environment variable
the doc exports, then run it with only the documented variables (against a bogus host if needed). A
wrong variable name passes every docs check and fails only when someone runs it.

## Decision and ruling docs

- Keep *current legacy behaviour* separate from the *ratified replacement*. Read the full decision,
  not the headline; decisions often have several parts, and surviving text that contradicts one part
  must be marked legacy.
- For every "remains required" or "tracked as open question <ID>" sentence, look up that ID and the
  decision it cites. A sweep that turns every gap into "required" can require the opposite of an
  answered ruling, or call an answered question open.
- When an intro labels only some sections historical, read the rest: acceptance summaries and
  "open items" sections often repeat the legacy plan as owed work.
- Unsigned deferrals reworded as "may choose" or "follow-up" are still descoping. Owed work reads as
  required, or goes to the owner as an option.
- Generated summaries can lag their sources; check dates and "answered" lists against the source
  ledger before quoting them.
