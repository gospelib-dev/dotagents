# Sources (read 2026-11 unless dated)

## Audio standards and specs
- ACX (Audible). "ACX audio submission requirements". https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements (primary; renders with JS)
- ACX, archived 2022 version. https://web.archive.org/web/20221011103238/https:/www.acx.com/help/acx-audio-submission-requirements/201456300 (room-tone rule history)
- Academy Voices. "ACX's New Room Tone Rule: 1 to 5 Seconds at the Start". https://academyvoices.com/blog/acx-room-tone-requirement-change (practitioner; dates the change only)
- Amazon KDP. "Learn more about audiobooks with virtual voice". https://kdp.amazon.com/en_US/help/topic/G3QRL9HQNF273Q2H
- [13] ITU-R BS.1770-5 (11/2023), "Algorithms to measure audio programme loudness and true-peak audio level". https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf
- [14] EBU R 128, "Loudness normalisation and permitted maximum level of audio signals". https://tech.ebu.ch/publications/r128 ; EBU Tech 3343-2023. https://tech.ebu.ch/docs/tech/tech3343.pdf
- ATSC A/85:2026-07, "Techniques for Maintaining Audio Loudness". https://www.atsc.org/wp-content/uploads/2026/07/A85-2026-07.pdf
- [15] ITU-T P.800.1 (2016), "Mean Opinion Score (MOS) terminology". https://www.itu.int/epublications/en/publication/itu-t-p-800-1-2016-07-mean-opinion-score-mos-terminology

## Tools
- [12] FFmpeg Filters documentation, `loudnorm`. https://ffmpeg.org/ffmpeg-filters.html#loudnorm
- FFmpeg source, `libavcodec/libmp3lame.c` (bitrate set only inside `if (avctx->bit_rate)`). https://github.com/FFmpeg/FFmpeg/blob/master/libavcodec/libmp3lame.c
- LAME source (mirror), `libmp3lame/lame.c`, `lame_init_params` (compression ratio 11.025 default). https://github.com/rbrito/lame/blob/origin/libmp3lame/lame.c

Unverified (kept out of rules): the LUFS-to-RMS offset for speech; the −3.5 dBTP margin
(practitioner habit, e.g. parkerpublishers.com/audiobook-mastering-acx-requirements).
