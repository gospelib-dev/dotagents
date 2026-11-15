---
name: originality-check
description: Use when checking a manuscript for copied text or derivative concepts.
metadata:
  version: "0.1.0"
  status: draft
  owner: maintainer
---

# Originality check for manuscripts

Check prose for verbatim or near-verbatim borrowing from published or online text, and check story
elements for unintended closeness to existing works, then triage what genuinely needs changing. This is
a screening method for agents with web search; it is **not** a substitute for a professional plagiarism
service, and an absence of matches proves only that nothing indexed was found.

## When to use

- Before submitting or publishing a chapter or book; after heavy revision or AI-assisted drafting.
- When a passage "sounds familiar", or a reviewer suspects a borrowed premise, character or set piece.

## Method

### 1. Phrase sampling and search

- Extract candidate passages: sentences and distinctive phrases of about 6–12 words. Skip dialogue tags,
  stock phrases and character/place names alone.
- Modes: **quick** (≈20 samples), **thorough** (≈50, or more for a whole book), **sentence** (complete
  sentences). Spread samples across the text; weight passages that are unusually polished or tonally
  different from their surroundings.
- Search each sample as an **exact quoted phrase**. Pace requests (≈1 s apart) to avoid rate limits.
- Record per match: phrase, location, source URL, match type (exact / near, i.e. reordered or lightly
  varied / common phrase). Compute an originality share as unmatched samples ÷ samples, and say it is a
  sample estimate.

| Share | Reading |
|---|---|
| 90–100% | highly original |
| 75–89% | mostly original |
| 50–74% | some borrowed content |
| 25–49% | significant copying |
| 0–24% | mostly copied |

### 2. Triage every match

- **Acceptable (do not flag):** idioms, common collocations, generic genre phrasing, the work's own
  earlier publication or excerpts, public-domain quotations the text deliberately cites.
- **Questionable (review):** a distinctive simile or image found once elsewhere; a near match with the
  same unusual word order; matches clustered in one passage.
- **Definite concern (must address):** a sentence or longer run matching a specific source verbatim or
  near-verbatim, or several distinctive matches to the same source.

### 3. Concept and media cross-check

Beyond text, compare the premise, character archetypes, set pieces and world elements with existing
media using targeted site searches: film/TV databases (IMDb, TMDB), franchise wikis (fandom sites),
Wikipedia, TV Tropes (to tell a common trope from a distinctive borrowing), and Goodreads (lists,
shelves and descriptions of comparable books in the same category). Build queries from the story's own
distinctive combinations, e.g. `site:tvtropes.org "mentor occultation"` or `site:goodreads.com/list "heist"
"fantasy"`. For genre fiction, check the major franchises of that genre for their signature elements
(their iconic devices, species, institutions and set pieces).

A shared **trope** is normal and not plagiarism. Flag only **specific expression** (names, scenes,
dialogue, distinctive designs) or a combination close enough that readers would name the source.

### 4. Unintentional influence

Check for style borrowing (distinctive sentence rhythms or metaphor patterns of a known author, voice
that echoes one writer too closely) and concept similarity (plot points or character dynamics that
mirror a familiar story). For each, recommend how to add an original spin or differentiate.

### 5. Edits

For each flagged passage give location, the matched source, why it matters, and a rewrite strategy:
re-imagine the image from the POV character's own sensorium and history; change structure, not just
synonyms; cut if the passage adds nothing. Then verify every rewrite still matches the character's voice
profile and the project's canon and style rules.

## Report

1. Summary: samples checked, matches, originality share (sample estimate), mode.
2. Matches found: phrase, location, source URL, type, triage verdict.
3. Top sources (most frequently matched sites).
4. Flagged passages in full context with recommended edits.
5. Concept/media similarities with a verdict (trope / close / concern) and differentiation ideas.

## Pitfalls

- Common phrases create false positives; fiction also matches quotes, tropes and similar stories.
- Web search only sees indexed text; paywalled books are largely invisible.
- Rate limiting truncates large runs silently; record how many searches actually completed.
- Never paste unpublished manuscript text into third-party services the owner has not approved.
- For local comparison against known reference files, a text-alignment tool (e.g. the `text-matcher`
  package) is more reliable than web search.

## Project specifics

The project's own skill supplies: any installed checker script and its dependencies, which comparable
works and franchises to prioritize, approval for sending text to external services, and the voice and
canon rules rewrites must respect.
