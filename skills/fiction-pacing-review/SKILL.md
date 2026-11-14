---
name: fiction-pacing-review
description: Use when reviewing fiction pacing, structure, tension or hooks. Diagnostics.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Fiction pacing and structure review

How a pacing specialist diagnoses rhythm in a chapter or sequence: map beats before judging, test
structure with several lenses without forcing a template, audit scene engines and try–fail cycles, draw
the tension wave, check mode balance, openings, transitions and endings, and report complete finding
classes with causal fixes. This skill diagnoses; it does not authorize prose edits. Sources `[S#]`
resolve in `references/sources.md`; depth in `references/frameworks.md` and
`references/tension-hooks-audience.md`.

## When to use

Chapter pacing, structure, tension, release, scene balance and hook reviews, alone or as a specialist
contribution to an editorial or readiness assessment.

## Inputs, in order

1. Pin the source revision. Read the chapter in full, its outline/notes, the previous chapter's ending
   and the next chapter's opening.
2. Read the project's binding constraints. An exact-text lock, completed decision, withheld-lore rule or
   do-not-touch span defeats a pacing preference. If a protected span is the apparent cause, cite the lock
   and return no finding.
3. Read any role dossier or chapter map for context, never as a substitute for prose.
4. Style guides and avoid-lists are secondary evidence, not pacing verdicts.

## Method

### 1. Map before judging

For each typographic scene and each functional beat record:
`lines | POV | time/place | goal/question | pressure | turn | outcome | dominant mode | tension 0–10`.
A functional beat can turn inside an unbroken scene; white space is not structure. Write the causal chain
in verbs: **because X, the character tries Y; therefore Z changes**. "And then" chains are suspect in
quest plotting [S19].

### 2. Test macro structure without forcing a template

- Beginning–middle–end wholeness and necessary/probable causation (Aristotle) [S1].
- Three-act setup/confrontation/resolution as a diagnostic (Field) [S3], not page percentages.
- Freytag's rise/climax/fall only when its dramatic wave fits [S2].
- Promise, visible progress, payoff (Sanderson) [S7]. Relationship or knowledge shifts count as progress.
- Reject any framework that makes the actual story worse; structures are tools [S8].

### 3. Audit scene engines and try–fail cycles

Action units: **goal → conflict → outcome/setback**. Processing units: **reaction → options/dilemma →
decision** (Swain, Bickham, Ingermanson) [S4][S5][S6]. Units may be compressed, interleaved, summarized
or omitted when trivial. For each attempt ask: is it an intelligent response to what the character
knows? Does the obstacle fail it for a distinct reason? Does the result change plan, cost, knowledge,
relationship, capability or time? Does the next attempt adapt? "No, and" / "yes, but" helps only when
consequence and adaptation are real [S8]. There is no required number of failures.

### 4. Draw the tension wave

Score each beat 0–10 (relative within the chapter only) and annotate the source: stakes, imminence,
instability, agency, uncertainty, knowledge gap, emotional investment. Tension comes from anticipated
emotionally significant outcomes (Lehne & Koelsch) [S9], not sentence length; suspense survives known
outcomes (Hoeken & van Vliet) [S11]. After a peak, look for release that lets consequence register
through body, thought, relationship, choice or tactic. Release may keep danger; it is not filler. Two
peaks may touch when continuous emergency is the point.

### 5. Test mode balance

- **Action:** choices and consequences legible; action changes state.
- **Dialogue:** each exchange changes leverage, knowledge, relationship or decision.
- **Reflection:** processes a specific change and ends in altered understanding or choice.
- **Description/worldbuilding:** sharpens orientation, threat, wonder, motive or tactics.

Do not seek equal percentages. Flag a mode only when its function stalls or crowds out the one the beat needs.

### 6. Opening, transitions, ending

- Opening: a live change, desire, pressure or orienting question early; no replay of the previous
  chapter before the new one starts (Kress, Edgerton) [S13][S14].
- Transition: preserve cause, emotional residue, time/place clarity, escalation or release.
- Ending: complete or sharply turn the local beat, then create pull through consequence, decision,
  revelation, image or danger. Cliffhangers are optional: experiments found they raise desire for the
  next installment, not suspense or enjoyment (Schibler et al.) [S12]. Vary hook types across chapters.

### 7. Audience and genre lens

Calibrate for the readership (for YA, YALSA's 12–18 range [S16]): clear causal orientation without
flattening moral or emotional complexity [S17][S18]. Attach lore to a present want, danger, wonder or
decision; SF exposition that halts action is a known failure [S19]. No universal chapter length exists:
use the chapter's job, its local baseline and the book's rhythm. Market length is a separate risk from
chapter pace; never use it to demand uniform cuts.

## Triage triggers (inspection thresholds, not craft laws)

| Trigger | Inspect for |
|---|---|
| No live chapter question after first 10% or ~500 words | delayed entry / recap opening |
| One unchanged beat function > ~900 words or 20% | sag or missing turn |
| Promised main reversal begins after ~55% | front-loaded setup |
| One functional scene > ~35% with no internal turn/release | reader fatigue |
| Third beat with the same function and outcome | repetition class |
| 10+ dialogue turns or ~300 words without new leverage, action, interiority or decision | static dialogue |
| ~250 expository words without changed tactic, threat, relationship or question | exposition shelf |
| Hook lands ~300+ words before the end and the runway changes nothing | second ending |
| Adjacent chapters share entry or exit construction | repetitive macro rhythm |

Report raw word counts and line ranges from a script; never estimate. Thresholds select passages for
rereading. They prove nothing by themselves.

## Finding classes and completeness

Classes: sag/unchanged state; rushed setup, turn, consequence or processing; repeated information,
proof, opening, hook or scene engine; action without character consequence; static dialogue; exposition
shelf; unearned escalation or climax reset; duplicate resolution/second ending.

Each finding gives: (1) class and severity (`required` only when publish-readiness fails, else
`suggestion`); (2) **every** instance as `file:line-line`, or "Other instances in scope: none"; (3) beat
function and reader effect, not "feels slow"; (4) a fix at the class root: what to cut, compress, move,
split or expand, and what must remain; (5) guardrail check.

Fix order: delete duplicate → compress to summary → move information under pressure → split for release
→ add missing consequence/decision → rewrite the sequence. Never add action merely to make prose "faster".

## Common bad reviews

- "Short sentences make pace fast." They change texture; stakes, causality and anticipation make pace.
- "Slow scenes drag." Processing can be the payoff; test change and duration.
- "Every chapter needs a cliffhanger." Consequence and decision hooks work too [S12].
- "Alternate scene and sequel mechanically." Compress or interleave to fit the story [S4][S5].
- "Hit act percentages." Field's page marks describe a screenplay model [S3].
- "One example proves the problem." List the full class.
- "Cut the protected passage." The lock wins; find a safe boundary or return no finding.

## Output skeleton

```markdown
# Pacing review — <chapter>
**Source:** <sha>  **Words:** <count>  **Verdict:** good | needs work | major
## Beat map
| Lines | Goal/question | Pressure | Turn/outcome | Mode | Tension |
## Rhythm summary
## Findings (ranked; every instance of each class)
## Strengths to preserve
## Metrics and calibration notes
```

## Project specifics

The project's own skill supplies: binding constraints and protected spans, the chapter map and known
repetition classes, beats and endings that must be preserved, arc progressions to protect, local length
baselines and market positioning, and worked applications on the book.
