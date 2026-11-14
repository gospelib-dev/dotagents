# Linguistic audit reference

Use this after the occurrence ledger. Canon rules still outrank general typology.

## Phonology and phonotactics

1. **Inventory:** Compare graphemes and IPA separately. A romanization may use two letters for one segment or one letter plus a diacritic; verify the canon mapping rather than reading it as English [S1].
2. **Contrast:** Ask whether the sound is phonemic, allophonic, marginal, or merely a spelling artifact. PHOIBLE warns that source descriptions can disagree, so preserve the source analysis instead of inferring from database frequency [S3].
3. **Syllabification:** Mark nuclei first, then assign onsets/codas according to the language's template. Canonical templates such as `(C)V(C)` describe possibilities, not permission for every segment combination [S2].
4. **Clusters:** Check both length and membership. An allowed `CC` onset can still reject a particular pair; word-medial strings may span a syllable boundary [S2].
5. **Suprasegmentals:** Verify tone, stress, and length independently. A missing diacritic can change a lexical or grammatical contrast [S1].
6. **Names:** Run the same test. Accept an exception only when canon labels its source (loan, fossil, dialect, foreign name).

### Failure patterns

- A segment occurs in prose but not the inventory.
- Romanization and IPA imply different sounds.
- A word ends in an unlicensed coda.
- A cluster is structurally possible but violates the language's allowed sequence.
- Stress, tone, or vowel length is omitted or moved.
- Apostrophe alternates between glottal stop, ejective, and punctuation without a stated rule.

## Harmony

For any claimed vowel harmony, record:

| Field | Question |
|---|---|
| Feature | backness, rounding, height, ATR, or another property? |
| Trigger | root, dominant affix, first vowel, stressed vowel? |
| Targets | all vowels or a restricted class? |
| Direction | progressive, regressive, or bidirectional? |
| Domain | stem, word, compound, phrase? |
| Exceptions | neutral, transparent, opaque, disharmonic, loan? |

Harmony is agreement in a defined domain and can create allomorphic alternations when morphemes combine; neutral vowels may be transparent or opaque [S4]. Therefore, do not flag a mixed-vowel word until the domain and exception classes are known.

## Morphology

Build a parse table for each phrase:

| Surface | Lemma/root | Morphs | Features | Literal contribution | Source |
|---|---|---|---|---|---|

Then test:

1. **Segmentation:** Every boundary corresponds to an attested morph or licensed fusion. A morpheme is not required to equal one syllable [S7–S8].
2. **Order:** Compare each affix with its slot. Languages may strongly prefer prefixes or suffixes, mix them, or use nonconcatenative marking [S5–S6].
3. **Exponence:** One morph may realize several features, and one feature may be distributed; do not demand one-to-one glossing when canon specifies fusion [S5].
4. **Allomorphy:** Apply harmony, assimilation, or other conditioned alternation after selecting the grammatical features [S4–S5].
5. **Agreement:** Check person, number (including dual/collective), gender/class if any, and subject/object indexing.
6. **Polarity:** Confirm whether negation is a particle, affix, circumfix, tone, or multiple marking. Position alone does not establish correctness.
7. **TAM/evidentiality:** Check every category canon marks as obligatory; a semantically plausible English translation can hide missing morphology.
8. **Lemma vs form:** A dictionary headword is not automatically the form required in the clause [S8].

## Syntax and semantics

1. Identify predicate, arguments, adjuncts, clause type, and information structure.
2. Verify canonical order and any licensed alternation.
3. Check adpositions against noun phrases and direction.
4. For questions, verify both constituent order and any required particle/morphology.
5. Compose the literal meaning from the parse before reading the supplied English gloss.
6. Compare literal meaning, idiomatic meaning, and speech act.
7. Check lexical valency and semantic roles: healer/healed, giver/recipient, observer/observed.
8. Check pragmatic felicity: title, politeness, taboo, collective membership, ritual setting, and authority.

## Naturalistic design diagnostics

Natural languages vary along independent dimensions; labels such as “agglutinative” compress several variables and should not be treated as a single scale [S5]. A robust design therefore specifies each mechanism separately.

- Derive recurring irregularities from history. Grammaticalization treats forms as changing entities and foregrounds reanalysis and analogy [S9].
- Let sound change interact with morphology, producing conditioned allomorphy rather than random misspellings [S4, S9].
- Maintain paradigms, not only lists of roots. Rosenfelder warns that writing isolated text first and backfilling grammar creates incoherence [S11].
- Connect language to speakers and history. Tolkien's account joins language-making with mythology; Peterson treats invention as an evolving system, not a cipher [S10, S12].
- Use typological databases as possibility checks, not generators or universals. PHOIBLE is a convenience sample and records source disagreements [S3].

## Interlinear glossing

For canon examples use four levels where useful:

1. Original surface form.
2. Morpheme segmentation with aligned boundaries.
3. Morpheme-by-morpheme gloss; grammatical labels in small caps or stable abbreviations.
4. Idiomatic translation.

The Leipzig Glossing Rules standardize alignment, boundary marks, grammatical labels, and translation presentation, but explicitly allow purpose-dependent detail and do not decide the analysis [S7].
