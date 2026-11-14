---
name: markdown-section-extraction
description: Use when pulling sections from big markdown files by heading. Script.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Markdown section extraction

Read only the part of a large markdown document you need (a story bible, outline, style guide, long
report) instead of loading the whole file. `scripts/extract.py` (standard library only) extracts one or
more sections by heading text, pattern or CSS-like hierarchical selector, and returns them with line
numbers plus short summaries of the parent, previous and next sections so you can follow up precisely.
It can also list or tree-view every heading across many files.

## When to use

- A file is too large to read whole, or you need a few named sections from many files.
- You need the heading structure of a document or folder before deciding what to read.
- You need a section plus the sections it links to internally.

## Usage

```bash
python3 scripts/extract.py <path|dir|glob> [pattern] [options]
```

| Pattern | Example | Behaviour |
|---|---|---|
| Single term | `"Scene 3"` | any heading containing "Scene 3" |
| Literal (contains a colon) | `"Chapter 2: The Long Road"` | one exact literal pattern |
| Soft match (spaces) | `"Act II Scene 3"` | terms match independently: Act II sections and Scene 3 sections |
| Multiple queries | `"Chapter 8; Chapter 9"` | each `;`-separated query runs separately |
| Regex | `"Scene [0-9]+"` | standard regex |
| Key-value | `"Target Length"` | matches `**Target Length**: ...` lines as nodes |

Hierarchical selectors: `A > B` direct child; `A >> B` any descendant; `A + B` adjacent sibling;
`A ~ B` any following sibling; `## A > ### B` explicit levels.

| Option | Effect |
|---|---|
| `-r, --recursive` | search directories recursively for `.md` |
| `--level N` | only headings at level N (1–6; 7 = key-values) |
| `--context` / `--no-context` | include (default) or omit surrounding-section summaries |
| `--related` | also extract sections linked via internal markdown links |
| `--format json` | JSON output |
| `--list` / `--tree` | flat list or indented tree of headings with line ranges |
| `--summary` | brief summaries with `--list`/`--tree` |
| `-p, --pattern` | filter headings in list/tree mode |

Examples:

```bash
python3 scripts/extract.py BIBLE.md --tree --summary            # map first
python3 scripts/extract.py BIBLE.md "## Main Characters > Mara"   # one entry
python3 scripts/extract.py ./chapters/ -r --list --level 2        # all chapter headings
python3 scripts/extract.py "docs/**/*.md" "Timeline" --related     # section plus linked sections
python3 scripts/extract.py BIBLE.md "Act I >> Setting" --format json
```

Multi-file search treats each file as a level above `#`.

## Method

1. Map: `--tree` (optionally `--summary`) to see the structure and line ranges.
2. Extract the narrowest selector that answers the question; use `--related` when sections cross-link.
3. Follow up with the line ranges in the context summaries rather than re-reading the whole file.
4. Cite `file:line` from the output when the content becomes evidence.

## Pitfalls

- A colon makes the pattern literal; use spaces for soft matching across terms.
- Soft matching is broad: `"Act II Scene 3"` returns both sets. Use `>` / `>>` to scope.
- `#` lines inside fenced code blocks are parsed as headings (they split sections); setext-style
  headings are not recognized. Check `--tree` on files with code samples.
- Extraction is for reading, not authority: cite the source file, not the extraction.

## Project specifics

The project's own skill supplies where the script is installed and which large files (story bible,
outlines, style guides) are worth mapping first.
