---
name: dialogue-voice-review
description: Use when reviewing dialogue, character voice or relationship beats in fiction.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Dialogue and character-voice review

How a dialogue specialist reviews speech, internal monologue, action beats and relationship-earned
voice in any fiction: establish what each speaker wants, fingerprint each voice, test attribution
without tags, test idiolect against situation, subtext, tags and beats, age and non-human voice, then
sweep each defect class. Sources `[S#]` resolve in `references/sources.md`; depth in
`references/dialogue-diagnostics.md` and `references/age-and-nonhuman.md`.

## When to use

Specialist chapter reviews, editorial voice checks, revisions that alter dialogue or monologue, and
relationship-beat verification. Never use it to override canon or binding revision constraints.

## Inputs and authority

1. Load the project's guardrails and binding plan. Never flag an exact-text lock, protected span,
   withheld-lore constraint or decided no-op as a defect.
2. Read the chapter and its outline/notes, any role dossier and the avoid-list.
3. For **every speaking or thinking character**, retrieve the voice profile, current chapter state and
   relationship history from canon. If retrieval is thin, read the source files and disclose the fallback.
4. Authority order: binding plan → current canon → manuscript continuity → voice guides where they do
   not conflict → field craft.

## Method

### 1. Scene contract

Record POV, speakers, each speaker's immediate want, emotional state, knowledge, audience, power
position and relationship stage. Dialogue is verbal action (McKee): every consequential line should
pursue, resist, conceal, test, bond or decide, not merely transfer information [S2].

### 2. Voice fingerprint

Seven axes per character: lexical domains; sentence shape/length; contractions/grammar;
questions/interruptions/pauses; address forms; figurative habits; body or sensorium accompanying speech.
Add one "never" rule and two manuscript anchors. Distinct voice is distributed across lexical and
syntactic choices, not one catchphrase [S10].

### 3. Tagless cold read

Take five representative lines per major speaker (low pressure, conflict, intimacy, exposition,
decision) without names, tags or giveaway lore nouns. Attribute each and name the axis that supports the
guess. **House trigger:** fewer than 4/5 for a major recurring speaker. Below that, inspect context,
translation, deliberate masking and state shifts before flagging. It is a trigger, not proof.

### 4. Idiolect against situation

A voice may shift with audience, fear, injury, intimacy, authority, language or identity state. Ask
whether the shift keeps the fingerprint while changing register. Style shifts can foreground a different
persona; do not demand static tics [S11].

### 5. Subtext and relationship action

For each vulnerable or conflict line: `surface words | private want/fear | tactic | listener uptake |
changed action`. If surface and private meaning match, check for intentional confession, crisis
breakthrough, child directness, ritual or safety instruction before calling it on-the-nose. Indirect
affective meaning is socially salient to adolescents and context-dependent [S6]. A relationship beat is
earned when prior pattern, pressure, risk, reciprocal response and a changed choice are present, and the
change carries forward.

### 6. Tags, beats and silence

- New speaker, new paragraph; tags identify speech cleanly [S15].
- Prefer unobtrusive attribution; avoid redundant or impossible tags (a smile does not speak) [S13].
- Every action beat must orient, characterize, escalate, carry subtext or change blocking; cut filler [S14].
- Silence, interruption, ellipsis and fragments must belong to the speaker and the pressure.
- No universal "said percentage"; any house ratio is a prompt, not a quality law.

### 7. Age without infantilizing

- Teen voice is not slang. Test priorities, peer sensitivity, autonomy, humour, turn-taking, risk and
  audience adaptation [S3][S6][S9].
- Do not ban complex syntax or abstract thought; adolescent language keeps developing, with real
  individual variation [S5][S7].
- Child voice may be lexically simple while behaviour is burdened or perceptive. Separate vocabulary from
  maturity. Milestones are descriptive ranges affected by culture, language and neurodiversity [S8].
- Read aloud: true and character-specific, not a transcript or an adult performing slang [S4].

### 8. Non-human voice

Anchor the reader with a recognizable need, then keep at least one non-human constraint in sensorium,
embodiment, cognition, time scale, social structure or communication [S12]. Review translated words
**with** gesture, colour, optics, glyphs, motion, latency or translator limits. Do not make every alien
archaic, every robot emotionless, or every species homogeneous. Register shifts should reveal role or
identity, not random weirdness [S11].

### 9. Sweep the whole class

For every defect, search the complete chapter for the same class: nickname drift, neutralized syntax,
repeated tag, random beat, adult ventriloquism, over-explicit emotion, knowledge leak, non-human
flattening. Report all instances together.

## Operational triggers (house tests, not empirical laws)

| Test | Trigger |
|---|---|
| Tagless attribution | fewer than 4 of 5 representative lines attributable |
| Fingerprint | fewer than 3 active axes in a scene, unless deliberate masking/silence |
| Speech length | more than 3 uninterrupted sentences: verify tactic turn and listener pressure [S4] |
| Action beat | serves none of orientation/character/subtext/escalation/blocking |
| Subtext | surface = private meaning in a baseline indirect relationship scene |
| Age | slang is the primary age marker, or child vocabulary turns uniformly adult |
| Non-human | the English line works unchanged for any human and embodiment adds nothing |
| Relationship | claimed growth produces no reciprocal response or changed choice |

## Failure modes → fix

| Failure | Fix |
|---|---|
| Everyone sounds like the author | restore one motive-linked lexical domain and one syntax/rhythm marker per speaker |
| Tic substitution | remove the catchphrase; distribute identity across the seven axes |
| On-the-nose feeling | move one layer into task choice, evasion, body/sensor behaviour or listener uptake |
| Random beats | replace with a character-specific task, or cut |
| Purple tag | `said`/`asked`, a precise speech verb, or a separate action |
| Fake teen slang | durable peer dynamics, concrete stakes, teasing, world-specific idiom |
| Child as miniature adult | shorten abstraction; keep perceptiveness through concrete noticing and action |
| Robot monotone | keep architecture and literal precision; vary latency, diagnostics, embodiment, intent |
| Alien ornament | let biology and culture alter metaphor, turn-taking, address and what stays unsaid |
| Earned shift flagged as drift | cite prior pressure and reciprocal consequence; withdraw the finding |

## Output

Start with a one-line verdict and the speakers reviewed. Then actionable findings only:
`file:line — [class] Character — problem; why it breaks fingerprint/state/relationship; concrete
replacement strategy. Other instances: lines …`. Group each class; separate required fixes from polish;
cite canon and craft basis. End with strong beats worth protecting, canon-retrieval gaps and checks run.

## Project specifics

The project's own skill supplies: each character's voice profile and locked forms (nicknames, titles,
contraction rules), known canon conflicts not to auto-fix, the cultures and species and how their
translated speech is rendered, current knowledge states for names, and any house ratios.
