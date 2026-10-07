# ElasticGridFX: почему 12× не означает 12× в AE

Evidence **PROJECT-REPORTED**. Review 2026-10-07, immutable documentation snapshot
`9d0162de64d01ceb41f6a1374a73544729ed0ec2`; [identity/source map](ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md).
Пять primary JSON records прочитаны целиком, arithmetic summary сопоставлен с
samples. Это проверка опубликованных records, не independent runtime replication.

| Record | Scoped finding | Чего он не доказывает |
|---|---|---|
| Native corrected comparison | 1080p32 region dense: medians 386.483/32.0415 ms = 12.06195×; five alternating pairs, fresh process, two warmups | AE export, Preview, все mapping types |
| Ordinary host render | 65.870721/48.766815 s = 1.350728×; five pairs, 60 frames, AE25.6, MFR requested OFF | Cold-cache/per-frame time, measured concurrency |
| Preview intervals | Baseline median bounds 11.546–12.924 s; candidate 1.753–6.007 s | Exact first-playable/gesture latency, known Preview preset |
| MFR record | INCOMPLETE; only three complete measured pairs, rejected 19/60 control | Five-pair speed acceptance, general MFR reliability |
| Closure retry | Three control + three candidate runs, NOT_REPRODUCED_IN_SIX_RUNS | Cause fixed; actual concurrent callbacks |

Host output — straight RGBA16 PNG из 32-bpc project; record содержит decoder и
calibration. Equality encoded output не сертифицирует native HDR/OCIO. Timing
включает startup, PNG и polling; cache/ambient activity не controlled. Изображение
PNG в sampled stack не позволяет оценить процент wall-time encoder.

## Incident, retry и решение — разные записи

Первоначальный control: SIGABRT, thread17, build
`EGFX-a733d95d2018fb8bc321b6d8`, loaded UUID
`22704d84-3ab5-3c47-90ab-eabf9daa05b1`, 19/60 outputs несмотря на launcher exit0.
Private raw-report SHA256:
`43eb0a1fce26e0a12815592009881e5d96d7f0e3053df682a5e0bc5aaa4e08fa`.
Cause UNKNOWN, fix NONE. Adobe termination frames не устанавливают первопричину
и не оправдывают/обвиняют effect. Partial equality относится только к найденным files.

Bounded retries не повторили crash; issue21 закрыт пользователем как not_planned,
NOT FIXED. Reopen условие — новый exact-identity crash + AEP hash и pre-termination
context. Старый failure record остаётся immutable. Не создавать speculative
shipping workaround после non-reproduction; не удалять evidence ради зелёного статуса.

## Provenance прочитанных bytes

Все filenames ниже разрешаются под
`https://raw.githubusercontent.com/ios3kov/ElasticGridFX/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/`.

| Filename | SHA-256 |
|---|---|
| performance-plane-corrected-comparison-2026-10-01.json | bb36898b4976d895cb70d655d9c7be89b402ed37aa1c8af39bace49960c09987 |
| performance-host-render-2026-10-02.json | 1316e12f899e9064022fa00d30ea591a1e6ade77fd8978b76f24160a19fab59d |
| performance-host-preview-intervals-2026-10-02.json | e0f60e9560c6e1bc42f1398e323f13d2c677e0ea84c1a1693634b6a23bdc7e24 |
| performance-host-mfr-2026-10-02.json | a6285cf92a6524241c2c96f6bb5b2273084954be68e9f895ddc16138ad95d761 |
| mfr-closure-retry-2026-10-02.json | 0db17c7110829d8ba01df817f228acf85e0887b77b6c5f855e44846379b53085 |

Private fixtures/logs не доступны независимо; public JSON aggregate не заменяет их.
Tools не копировались: **do not transfer in this edition** до отдельного licensing/
dependencies/host-side-effect review. Это решение не утверждает завершённый audit tools.
