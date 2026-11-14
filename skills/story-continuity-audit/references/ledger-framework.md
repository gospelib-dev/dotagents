# Continuity ledger framework

Sources `[S#]` refer to [sources.md](sources.md).

## 1. Authority stack

Use the narrowest authoritative evidence for each question:

1. Binding owner decisions and locked spans govern intent.
2. Current manuscript prose proves what occurs and what readers can see.
3. The story bible records the maintained interpretation and future constraints.
4. A search mirror of the story bible retrieves it; it is not a separate authority.
5. A reader-position tool retrieves only reader-visible prose at a checkpoint; it is not canon.
6. Outlines and plans describe intended beats until current prose disproves them.

Professional standards require scope control, accuracy checks, and preservation of intended meaning [S1]. Fiction
copyediting specifically tracks characters, places, events, and timelines, with complex questions returned to the
author [S2].

## 2. Event ledger

| Field | Rule |
|---|---|
| Event ID | Stable `chNN-scene-event` label. |
| Story time | Exact value only if stated; otherwise bounds (`Day 4 night–Day 5 dawn`). |
| Discourse position | Chapter and line range; keep distinct from story time [S12]. |
| POV / focalizer | Whose perception limits the scene. |
| Place | Named location plus sub-location and route from prior event. |
| Entities | Characters and plot-bearing objects present. |
| Cause / goal | Immediate causal predecessor and active character goal. |
| Entry state | Condition, inventory, knowledge, relationship, technology readiness. |
| Delta | Explicit action, transfer, wound, disclosure, inference, failure, or choice. |
| Exit state | Values after the delta; becomes the next scene's expected entry. |
| Evidence | Exact prose and canon citations. |

The dimensions follow narrative-comprehension research: readers monitor time, space, protagonist/entity,
causation, and motivation, and discontinuities raise processing cost [S10]. The ledger adds production fields
(custody, health, knowledge, technology) because fiction style sheets must track people, places, and timelines
[S2–S5].

## 3. State-machine schemas

### Character

`location | physical condition | injuries | clothing/visible identifiers | inventory | abilities | goals |
knowledge | beliefs | relationships | authority/status`

Store negative capabilities only when established (`cannot read sacred register`, `network command fails here`). A
new ability requires an acquisition event or earlier seed.

### Object custody

`object | holder | exact location | container | condition | visibility | last transfer event | next required use`

Transitions: `acquire → carry/store → transfer/confiscate/lose → recover/consume/destroy`. An object cannot be both
in inventory and abandoned unless a duplicate is explicit. “Not named in the search result” is not a loss event.

### Technology

`device | operator | components | input | preconditions | output | range | cost | failure mode | who understands it`

Separate mechanism from character interpretation. Separate visually similar channels (for example: device audio,
translated speech, telepathic contact, implant sync, network signals).

### Relationship

`A↔B | trust | obligation | fear | authority | intimacy | public/private status | last change event`

Do not update a relationship from dialogue alone if the following action repudiates it. Record action and stated
belief separately.

## 4. Timeline table

| Event | Earliest | Latest | Duration | Travel | Sleep | Light/weather | Injury clock | Simultaneous with | Source |
|---|---:|---:|---:|---:|---:|---|---|---|---|

Rules:

- Solve explicit arithmetic exactly. A source saying “about” keeps a range.
- Preserve relative references (“next morning”) if calendar anchors are absent.
- Separate narrated order from event order for flashbacks, memories, and summaries [S12].
- Treat distance/speed as a feasibility range, not a false precise estimate.
- Check wound consequences, food/water, battery, daylight, and rest against elapsed time.
- A timeline statement in a packet is a claim, not evidence, until traced to prose.

Schneider recommends recording fixed and relative references, weather, sun position, travel, time zones, scene
breaks, POV changes, parallel timelines, and flashbacks [S2]. CIEP likewise treats a timeline as essential,
especially for nonlinear fiction [S3].

## 5. Epistemic and reveal ledger

| Fact | Truth | Reader evidence | Character evidence | Belief | Confidence | Channel | Acquired | Shared | Payoff |
|---|---|---|---|---|---|---|---|---|---|

Use four values, not a Boolean: `unknown`, `suspected`, `known`, `false belief`. Also mark `withheld` when a
character knows but intentionally does not disclose.

### Reveal lanes

- **Truth lane:** what is canonically true, including gated facts never stated on-page.
- **Reader lane:** what the text has made available at the checkpoint.
- **POV lane:** what the focal character perceives or plausibly infers.
- **Private lane:** knowledge held by a subset of characters.
- **Public lane:** what has been disclosed to the relevant group.

Dramatic irony is the structural difference between audience and character understanding [S8]. Experimental work
shows that installation of information unavailable to a character changes audience processing of the exploitation
scene [S9]. Therefore record both installation and payoff, not just “reader knows.”

### Reveal tests

1. **Acquisition:** Is there a cited perception, statement, translation, memory, document, or inference?
2. **Channel access:** Could this character hear/see/translate/understand it?
3. **Confidence:** Was it framed as fact, hypothesis, dream, lie, or corrupted signal?
4. **Propagation:** Who witnessed the disclosure? Who was absent?
5. **Action fit:** Does later action match the belief held at that moment?
6. **Reader fit:** Has the reader seen enough to understand the intended irony without future knowledge?
7. **Payoff:** Does the later reveal answer the installed question rather than introduce it retroactively?

The curse-of-knowledge effect makes backward assessment unreliable; verify at the bounded chapter checkpoint
[S11].

## 6. NEW versus CORRECTION

### NEW

Use when a value changes in story time and the transition is supported:

`Ch4: relic = left in the wreck → Ch20: relic = recovered`, with an on-page recovery in Ch20.

Add an effective range and retain history. Never rewrite the old value as if it was always false.

### CORRECTION

Use when a record misstates what the authoritative source says:

`packet says the relic stayed in the hero's pocket; ch4 says it fell into the wreckage and was left`.

Correct the record and every dependent mirror; do not invent an in-story transfer.

## 7. Triage

- **Blocker:** binding plan/lock/protected-span/gated-lore violation or missing required beat.
- **Major:** impossible timeline, custody teleport, knowledge leak, contradictory character state, causal break.
- **Minor:** stale title, first-appearance label, scene count, or summary wording with no reader-facing effect.
- **Query:** evidence permits multiple intent-changing repairs.

Fix simple contradictions at the authoritative record; query complex story decisions [S2, S6].
