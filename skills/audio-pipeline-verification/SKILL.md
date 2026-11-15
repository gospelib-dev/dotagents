---
name: audio-pipeline-verification
description: Use when building or reviewing TTS/audio render or export. Measure, don't echo.
metadata:
  version: "0.1.0"
  status: draft
  owner: maintainer
---

# Audio pipeline verification

Verify audio as data, not "a file exists". This is the method for engineers and reviewers working on
speech synthesis, audio processing, stitching, loudness and packaging (audiobooks, podcasts, voice
apps). It covers pipeline invariants, render caches, loudness and true peak, encoder settings,
packaging probes, delivery specs, and human listening tests.

## When to use

Any change to a TTS engine adapter, DSP transform, render cache, stitcher, loudness normaliser,
encoder/packager, or a card that targets a retailer or broadcast delivery spec.

## Principles

- **Measure the artifact, never echo the request.** A test that asserts "loudness == target" using
  the target it passed in proves nothing. Re-measure the bytes on disk, and measure the *encoded*
  file: lossy encoding changes peaks. [13]
- **Decide the delivery target first.** Loudness, peak, format and file layout depend on the target
  (private listening, a retailer such as ACX/Audible, broadcast R128). Don't invent a ceiling from a
  spec the owner never chose, and don't call output compliant with a spec nobody named.
- **Sample peak is not true peak.** ITU-R BS.1770 defines true peak by 4× oversampling and warns
  inter-sample peaks can exceed the largest sample. `max(abs(samples)) <= 1` is not a true-peak
  gate. [13]
- **RMS is not LUFS.** Integrated loudness (LUFS/LKFS) is K-weighted and gated; RMS is unweighted and
  counts silence. They differ by a content-dependent amount: measure what the spec names.
- **Never trust encoder defaults.** Set bitrate, sample rate and channels explicitly and assert them.
- **Objective metrics screen; ears decide.** Use human listening for timbre, affect, pronunciation,
  transitions and extreme DSP.

## Pipeline invariants (assert at every stage)

Engine adapter, pronunciation/prosody, guidance/voice conversion, cache, stitch, loudness, package:

- non-empty, finite samples (reject NaN/Inf) before caching;
- explicit dtype, channel layout and a positive declared sample rate (a common adapter contract:
  mono float32 plus sample rate);
- expected duration/sample-count bounds after every stitch or time transform; no silent truncation
  or unintended resampling; resample explicitly;
- preserve source audio until the last responsible transform;
- deterministic metadata and cache identity;
- failures leave the previous good artifact intact.

## Render cache correctness

A cache hit asserts that two renders are semantically identical. Keys include every byte-changing
input: normalised text and pronunciation/phoneme decisions; voice, engine, reference, model or
checkpoint; prosody controls (pace, pitch, energy, emotion, accent) and engine-native overrides;
guidance take identity and dials; quality tier; sample rate; pipeline/DSP version; language profile.
For each field: same input hits, changing only that field misses. Also test atomic manifest update,
stale/missing clip recovery, and concurrent renders of the same key.

## Transform tests

| Transform | Assert |
|---|---|
| Resample | requested output rate; duration tolerance; no NaN/Inf; anti-alias path used |
| Gain | monotonic RMS/energy; documented unity point; clip/true-peak policy |
| Time/rhythm | directional duration change; alignment still covers words; no zero/negative spans |
| Pitch/formant | requested direction; duration preserved within tolerance; restore byte-stable where promised |
| Stitch | order; exact gaps by boundary type; sample-rate reconciliation; head/tail policy; no cumulative drift |
| Loudness | target and tolerance; silence and unreachable targets surfaced; encoded true peak |
| Package | codec, rate, channels, bitrate, tags, artwork, chapter marks, continuity, duration |

## Packaging probes (ffprobe/decoder output, not filenames)

Codec; sample rate and channel layout; bitrate or quality mode; duration vs stitched source; title,
author, album/series, track tags; chapter count, titles, contiguous starts/ends with the last end near
stream duration; artwork disposition and size; full-file decode succeeds; integrated loudness and true
peak *after* lossy encoding. Keep a tiny generated fixture for deterministic package tests and one
complete-length smoke build for scale and continuity.

## Loudness and encoding facts

- FFmpeg `loudnorm` is an EBU R128 normaliser (defaults I −24, LRA 7, TP −2). Single pass is dynamic;
  two-pass with measured values and `linear=true` applies one gain but *falls back to dynamic* if
  that would breach TP or measured LRA exceeds the target — check `normalization_type` in pass 2.
  Dynamic mode upsamples to 192 kHz, so always set `-ar` on output. [12][14]
- pyloudnorm implements BS.1770 integrated loudness only; it neither limits nor measures true peak.
- FFmpeg's libmp3lame wrapper sets a bitrate only when `-b:a` is given. Without it LAME uses its
  compression-ratio default (11.025): `samplerate*16*channels/(1000*11.025)` rounded to a legal
  bitrate — 44.1 kHz stereo → 128 kbps, but 24 kHz mono → ~32 kbps. Always pass `-b:a -ar -ac`.
- Use a room-tone bed, not digital zero, where a spec measures noise floor or room tone.

Retailer and broadcast numbers (ACX/Audible levels, peaks, noise floor, room tone, MP3 format, file
layout, narration policy; EBU R128 and true-peak margins) and a recipe from a TTS master are in
[references/delivery-specs.md](references/delivery-specs.md).

## Listening evaluation

Objective checks catch regressions, not listener quality. MOS terminology is standardised
(ITU-T P.800.1), but the listening design and question must be reported. [15]

1. Freeze a prompt set: narration, dialogue, questions/exclamations, long sentences, scene breaks,
   numerals, invented or foreign terms and names.
2. Loudness-match clips; randomise and blind A/B order.
3. Score separate 1–5 dimensions: intelligibility, naturalness, pronunciation, voice identity and
   consistency, emotional fit, pacing, audible artifacts.
4. Record engine, model/checkpoint, seed, voice/reference and every override.
5. At least two listeners per main-voice change; a disagreement triggers a third (a reasonable
   operational minimum, not part of P.800.1).
6. Keep raw notes and aggregate by prompt category, never one global mean.

## Pitfalls

- Pronunciation pipelines with lexicon → accent → G2P precedence: don't "fix" deliberate literals
  (numbers spelled as words in the source text).
- A sample-peak limiter at −0.3 dBFS is not "clip-safe" after lossy encoding.
- Hardware-bound suites (Apple Silicon/Metal models) can't run in a Linux sandbox: label results
  "not executed" and hand verification to the supported host rather than implying a pass.

## Verification

Encoded files probed for codec/rate/channels/bitrate and decoded to the end; loudness and true peak
measured on the encoded file against a named target; cache-key pair tests for touched fields;
listening results reported with design and raw notes.

## Project specifics

The project's engineering skill or `AGENTS.md` supplies the chosen delivery target and tolerances,
working sample rate, engine list and adapters, cache key builder, pronunciation corpus, and which
host runs the hardware lane.

Sources: [references/sources.md](references/sources.md).
