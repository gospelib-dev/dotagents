# Delivery specs: ACX/Audible and broadcast loudness

Read 2026-11 from the official ACX help page (it needs JS to render):
https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements — re-check before
citing; retailer rules change.

## ACX / Audible requirements (paraphrased tightly)

| Area | Requirement | How to measure |
|---|---|---|
| Levels | −23 to −18 dB **RMS** per file | RMS over the file (ACX Check / Audacity); integrated LUFS is a different measure — do not substitute |
| Peak | ≤ −3 dB | true-peak meter (4× oversampled, BS.1770 Annex 2); sample peak under-reads |
| Noise floor | ≤ −60 dB RMS | RMS of room-tone gaps; digital-zero gaps are not room tone |
| Room tone | "We recommend between 1 and 5 seconds… at the beginning and end of each file"; "must not exceed 5 seconds" | measure leading/trailing non-speech |
| Encoding | MP3, **CBR**, ≥ 192 kbps, **44.1 kHz** (256/320 allowed, negligible gain) | ffprobe `bit_rate`, `sample_rate` |
| Channels | all mono or all stereo, never mixed | ffprobe `channels` across files |
| Files | one chapter/section per file with its spoken header; each ≤ 120 min (split with "Chapter N continued"); opening and closing credits as separate files; US-alphanumeric file names | file list |
| Credits | opening: title, author(s), narrator(s) matching metadata/cover; closing indicates finality ("You have been listening to… The End") | listen |
| Retail sample | ≤ 5 min, from the audiobook, no explicit material; ACX asks for the first five minutes (Apple Books always uses the first five) | file |
| Consistency | levels, tone, noise, spacing, pronunciation consistent; no plosives, clicks, mouth noise, outtakes | listen |
| Narration | "Unauthorized use of text-to-speech, AI, or automated recordings in ACX titles is prohibited." Audible says it is "working to accept third-party TTS content" (no date) | owner decision — block the card, do not guess |

Amazon's separate KDP "virtual voice" beta generates its own computer voice from an eligible eBook
(kdp.amazon.com help topic G3QRL9HQNF273Q2H); it does not accept third-party renders. So any
"publish to Audible" task for a TTS pipeline needs an owner decision first.

History: an older rule (archived 2022, and quoted in ACX QA emails) asked for 0.5–1 s head and 1–5 s
tail room tone; a practitioner blog (academyvoices.com) dates the head change to Oct 2026.

## Broadcast / general loudness

- **ITU-R BS.1770-5**: integrated loudness is K-weighted and gated (−70 LKFS absolute, −10 LU
  relative, 400 ms blocks), so it ignores silences RMS counts. True peak (dBTP) per Annex 2 estimates
  inter-sample peaks by 4× oversampling.
- **EBU R 128 / Tech 3343**: production maximum −1 dBTP (−2 dBTP before lossy codecs such as MPEG-1
  L2 or AC-3).
- **ATSC A/85**: also specifies 4× oversampled true peak.
- Lossy encoding can raise peaks: leave margin under a −3 dB ceiling. Practitioners use about
  −3.5 dBTP limiting for ACX (unverified rule of thumb).

## Recipe: ACX-conformant files from a 24 kHz mono TTS master

1. Stitch with a room-tone bed (not digital zero), 1–5 s head and tail.
2. Resample to 44.1 kHz (`-ar 44100`), keep every file mono.
3. Level to about −20 dB RMS, true-peak limit at about −3.5 dBTP, then re-measure RMS, peak and noise
   floor on the *encoded* MP3.
4. Encode `-c:a libmp3lame -b:a 192k -ar 44100 -ac 1` (FFmpeg uses CBR via `lame_set_brate` unless
   `-abr 1`).
5. Assert in tests with ffprobe: `bit_rate >= 192000`, `sample_rate == 44100`, the same `channels`
   for every file.

Not verified: the exact LUFS-to-RMS offset for speech (content-dependent; measure, don't convert).
