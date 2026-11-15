---
name: layered-chapter-drafting
description: Use when drafting a chapter from an outline. Brief, layered passes, gates.
metadata:
  version: "0.2.0"
  status: draft
  owner: Lance
---

# Layered chapter drafting

A production method for drafting (or fully redrafting) a novel chapter with agents: first assemble one
chapter brief from canon, then write in **layered passes**, each with one concern, a small context and
hard rules about what it may not touch, with verification gates between them. Building quality
incrementally beats asking one generation to do structure, accuracy, voice, atmosphere and polish at
once. Craft depth for each layer lives in `fiction-prose-craft`; this skill is the pipeline.

## When to use

- Writing a new chapter from an approved outline, or rewriting one from scratch.
- Revising a chapter after an assessment, by re-running only the affected passes.
- Not for small line edits (edit directly) or canon changes (continuity skill).

## Phase 0: the chapter brief

Assemble one brief per chapter (e.g. `<reports>/chapter-NN/brief.md`), regenerated whenever its sources
change. It is the drafting agents' single authority and states that it supersedes the outline where they
conflict. Contents:

- **Source priority** and **hard constraints** (locks, withheld lore, owner rulings).
- **Characters not present** (must never appear) and a **character–scene map** (who may appear where).
- **Critical numbers** (ages, counts, distances, percentages) and correct name forms.
- **Continuity state on entry only**: injuries, inventory, device states, locations, relationships, as
  they stand when the chapter opens; no mid-chapter or ending states.
- **Voices** for the characters in this chapter only, complete, not truncated.
- **Relationships** filtered to pairs involving a present character.
- **Spatial context** for each location (layout, light, sound, hazards).
- **Language references** for invented terms actually used here, not the whole grammar.
- **Previous chapter ending** plus a short voice sample (2–3 paragraphs) from it.
- **Chapter structure**: opening hook, closing hook, section plan with word targets, beat-by-beat outline
  with consequences, plants and payoffs.
- **Prose rules**: the avoid-list hits already present, house quotas, readability targets.

Verify before drafting: no placeholders ("see file", "TBD", "..."), real values for every state field,
every outline beat present. Extraction should be scripted and deterministic where possible.

## The passes

Each pass edits the chapter file in place, receives only the brief sections it needs, and returns a
one-line status. Orchestrators coordinate and do not load story files into their own context.

1. **Skeleton.** Turn each beat into 1–5 lines of plain, factual narrative in order, grouped by section.
   No metaphor, no sensory detail beyond the outline, no interpretation: "screenplay directions". Respect
   the character–scene map. Realize the opening and closing hooks. Ignore any existing draft.
   - **Gate A (structure):** every beat present; no absent character appears; map respected; hooks
     realized; section breaks present.
2. **Accuracy.** Cross-check every fact against the brief and canon (presence, numbers, objects, device
   states, relationships, spatial facts); fix in place; add nothing; mark anything unverifiable
   `[VERIFY: …]`.
   - **Gate B (facts):** no contradictions; no remaining hard-constraint violations; list `[VERIFY]` tags
     for the owner.
3. **Voice and emotion.** Make every speaker distinct per profile; subtext through what is not said;
   emotion through body and action, never labels; build to peaks rather than starting high; keep direct
   italic thought rare. Do not change facts, add events, or add atmosphere yet.
4. **Sensory and atmosphere.** Ground scenes physically: favour non-visual senses (sound, smell, touch)
   before sight; a few specific details per **scene**, not per paragraph; concrete nouns; environment
   reflects mood lightly; elevated language only at pivotal moments. Do not change dialogue, voice,
   emotional beats or facts; do not over-describe.
5. **Polish.** Enforce zero-tolerance patterns (banned AI tells and clichés, hedges like "began to",
   filter verbs, stock emotion clichés), per-chapter action quotas (smiled, nodded, sighed …), sentence
   rhythm (no long runs of same-length sentences or same openings; shorter in action, longer in
   reflection), readability targets and word-count target. If under target, do not pad: flag it.
   - **Gate C (compliance):** run the analyzer (`prose-text-analysis`), the avoid-list and quota checks,
     and invented-language validation if applicable.

## Multi-model variant

When several drafting models are available, the prose-generating work (a full draft from the brief, or the
voice and atmosphere passes 3-4) can fan out to them and be merged, following `multi-model-drafting`. The
merged text then goes back through Gate B (facts) before Polish: merging can introduce errors as well as
remove them.

## Gate failure protocol

On failure, re-run only the preceding pass with the gate's output appended: "Fix ONLY these issues; make
no other changes." Allow at most two retries per gate, then stop and report to the owner with the
remaining issues. Never weaken a gate to pass it.

## Revision mode

Load the assessment's required fixes, map each to the pass that owns it (structure → 1, facts → 2,
voice → 3, atmosphere → 4, mechanics → 5), re-run those passes on the existing text with the fix list,
then re-run the downstream gates. Record deliberate outline deviations in revision notes for the editor.

## Pitfalls

- Letting an early pass "improve" style: it creates work later passes must undo.
- Feeding every pass the whole brief: context bloat blurs the single concern.
- Writing on stale state: regenerate the brief after any canon or outline change.
- Treating gate counts as quality: gates catch violations; the editor still judges the chapter.

## Project specifics

The project's own skill supplies: where briefs and chapters live, the brief template and extraction
scripts, heading and scene-break formats, voice profiles and locked name forms, the prose-rules and
avoid-list files, quotas, readability and length targets, and which agents or models run each pass.
