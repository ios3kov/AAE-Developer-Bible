# Учебный комплект: Minimal Gain — source lesson

**ILLUSTRATIVE / NOT_RUN**, не runtime evidence. Product: Bible-derived Gain demo,
SDK baseline 25.6, [source](../../16-WORKING-TEMPLATES/effect-basic/EffectMain.cpp).
Actual release SHA/binary hashes/AE build заполняются при создании reader artifact;
ни один placeholder не означает проверенную совместимость.

## Specification

Classic 8/16-bpc RGB gain 0…4, default 1; alpha unchanged; integer channels clamp
to 255/32768. Float/GPU/MFR support не заявлены. Gain disk ID=1 сохранён. Identity
gain=1 сохраняет допустимые integer values; gain=2/input red=100 → red=200 при 8-bpc.
Sequence/arbitrary state отсутствует. UI source mutation не требуется для render.

## Compatibility and correctness record

| SDK | Host | Architecture | Compile | Load/render | Основание |
|---|---|---|---|---|---|
| 25.6 build61 | Exact AE build: unrecorded | mac arm64 | NOT_RUN | NOT_RUN | Учебная форма |
| 25.6 build61 | Exact AE build: unrecorded | Win x64 | NOT_RUN | NOT_RUN | Учебная форма |

Fixture: ramp+distinct RGBA+transparent edge+odd width+ROI. Expected values до
прогона; export precision/alpha/profile/decoder/calibration отдельно. Не считать
export byte equality raw-world proof. Product acceptance requires owned artifact
identity и complete observed results, не эту форму.

## Failure report

Illustrative: gain fixture did not produce expected 60 decoded frames; 19 found.
Status FAIL, cause UNKNOWN, source/binary/loaded UUID unrecorded, raw evidence absent.
No timing accepted from incomplete run. `launcher exit0` не исправляет FAIL.
Это учебный пример структуры, не событие с Minimal Gain.

## Performance and release record

Warmup=2, repetitions=5 — **план**, measurements отсутствуют. Native core, ordinary
host render/export, Preview fill и displayed playback измерять отдельно. No speedup
number claimed. Release decision BLOCKED for demonstration runtime claims; docs
can remain source-reviewed. Release notes: added gain source lesson, no tested
AE/OS support range. Install/signing/upgrade NOT_RUN; no distribution artifact.

## Machine-readable форма

```json
{"kind":"ILLUSTRATIVE","product":"Gain lesson","sourceSha":null,"artifactHash":null,"hostBuild":null,"status":"NOT_RUN","confidence":"SOURCE EXAMPLE","decision":"not accepted for runtime claims","expectedFrames":60,"decodedFrames":null,"rawEvidence":[]}
```

Test status, evidence origin и accepted/rejected decision — независимые поля.
После реального run сохранить raw record immutable; исправление документации не
переписывает старый FAIL. Pair этот комплект с BUG-REPORT, PERFORMANCE-REPORT,
PLUGIN-SPEC, COMPATIBILITY-MATRIX и RELEASE-NOTES templates.
