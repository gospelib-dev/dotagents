#!/usr/bin/env python3
"""Build a compact, reproducible ledger of report lines that mention one chapter."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports-root", type=Path, required=True)
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chapter = str(args.chapter)
    pattern = re.compile(
        rf"(?i)(\bchapter[- ]?0*{re.escape(chapter)}\b|"
        rf"\bch\.?\s*0*{re.escape(chapter)}\b|{re.escape(args.title)})"
    )

    entries: list[tuple[Path, list[tuple[int, str, str]]]] = []
    for path in sorted(args.reports_root.rglob("*.md")):
        heading = "(document start)"
        hits: list[tuple[int, str, str]] = []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("#"):
                heading = line
            if pattern.search(line):
                hits.append((number, heading, line))
        if hits:
            entries.append((path.relative_to(args.reports_root), hits))

    hit_count = sum(len(hits) for _, hits in entries)
    output = [
        "# Chapter report mention ledger",
        "",
        f"Chapter: {args.chapter:02d}",
        f"Title: {args.title}",
        f"Files: {len(entries)}",
        f"Exact matching lines: {hit_count}",
        "",
    ]
    for path, hits in entries:
        output.append(f"## {path} ({len(hits)} hits)")
        previous_heading = None
        for number, heading, line in hits:
            if heading != previous_heading:
                output.append(f"### Context: {heading}")
                previous_heading = heading
            output.append(f"{number}|{line}")
        output.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(output), encoding="utf-8")
    print(f"files={len(entries)} hits={hit_count} output={args.output}")


if __name__ == "__main__":
    main()
