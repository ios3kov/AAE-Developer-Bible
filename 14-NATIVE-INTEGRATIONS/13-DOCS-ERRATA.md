# Public SDK docs errata / verification notes

> Supporting errata/conflict record. Canonical editorial policy: [EDITORIAL-GUIDE.md](../EDITORIAL-GUIDE.md).

Research baseline: **SDK 25.6 source review + dated public documentation review**.

Purpose of this file: preserve places where public guide, bundled sample, historical code and exact SDK headers can disagree.

Главное правило:

> **не выбирать источник по удобству. Классифицировать, что именно каждый источник доказывает.**

## Evidence order

For exact native declarations:

1. exact target SDK header;
2. SuiteHandler/utility from same SDK;
3. official sample from same distribution;
4. public guide;
5. historical/community material.

Для lifecycle/ownership prototype alone недостаточен: нужны comments, paired APIs и sample behavior.

## Erratum vs version difference

Не всякое расхождение — ошибка документации.

Possible classes:

- typo;
- stale generated HTML;
- sample intentionally uses older suite;
- API changed between SDK versions;
- public guide describes concept, not exact signature;
- sample has simplified teaching code.

Всегда записывайте class before “fixing” Bible text.

## Confirmed/observed mismatches

### Project Suite

В одном public render встречалось:

```text
AEGP_GetProjectProjectByIndex
```

Exact API/header baseline uses:

```text
AEGP_GetProjectByIndex
```

Treat the doubled `Project` form as documentation typo, not alternate function.

### Item Suite — CreateNewFolder

Some historical/public HTML showed an extra project argument.

Current reviewed header shape for the relevant baseline does not use that extra project handle.

Rule: copy signature from exact header, not remembered HTML.

### Layer Suite — AddLayer

Some HTML renderings showed an incorrect third-argument type.

Reviewed header contract uses output `AEGP_LayerH*`.

## Legacy sample generations

### SmartFX / audio / PiPL reconciliation

The 2026-10-06 audit commit `31fba78` records further guide/header differences.
Read these through the current baseline chapters, not as replacement signatures:

- SmartFX delete callback is `delete_pre_render_data_func` in SDK 25.6, not the
  guide's historical `func` rendering. Checkout ID is non-negative in the header;
  ID1 in the authored Copy satisfies both non-negative and positive guidance.
- Early layer-pixel checkin is optional in this SmartFX contract; parameter
  checkin depends on phase. The [SmartFX table](../02-EFFECT-PLUGINS/03-SMARTFX.md)
  separates pre-render automatic checkin from render explicit checkin.
- Audio prose about “floating point (24-bit)” is not a buffer storage declaration.
  Use format and sample size in bytes, as in the [audio chapter](../02-EFFECT-PLUGINS/07-AUDIO.md).
- Newer PiPL guide Search Keywords/Description notes are scoped to Premiere Pro
  Beta 27.0, not automatically After Effects or SDK25.6 features. Consult target
  headers and [the dated guide](https://ae-plugins.docsforadobe.dev/intro/pipl-resources/)
  before adopting them. This preserves the audit's scope, not a new SDK26.5 review.

Bundled samples can intentionally use old suites.

Examples already documented in Bible include older Stream/Keyframe/DynamicStream generations in samples shipped alongside newer headers.

Correct use:

- learn workflow/lifecycle from sample;
- take current signature/generation from exact header;
- record version boundary.

Incorrect use:

- declare sample generation “current” because Adobe shipped it in the SDK folder.

## Suite-number trap

Type suffix and public suite version macro are not guaranteed to be the same number.

Example pattern:

```text
AEGP_StreamSuite6
but AcquireSuite public version constant may have another numeric value
```

Use the official suite-name/version macro pair rather than deriving number from struct suffix.

## Guide/ItemView later-version notes

Later SDK research includes newer Guide/ItemView/Comp/Stream suite generations.

These notes must remain explicit version-gated additions; they cannot silently become SDK 25.6 baseline.

## PiPL/sample comments

Comments in old `.r` samples can be stale even when constants are correct.

Treat:

```text
constant value
header macro
current resource contract
```

as stronger evidence than a historical explanatory comment.

## Callback signature drift

Old AEGP samples may use initializer/callback signatures that differ from current typedefs.

Do not force compiler casts to reproduce old sample ABI.

Instead:

1. read current typedef;
2. compare sample;
3. document version/history;
4. adapt current code to current contract.

## Boolean vs enum mistake

Native APIs with enum parameter must not receive `TRUE/FALSE` merely because C++ accepts integer conversion.

Bible's render-queue review found a concrete case where `TRUE == 1` mapped to a different enum state than intended `QUEUED`.

Lesson: semantic type matters even when binary width looks compatible.

## Ownership errata

Public prose can omit cleanup detail.

Whenever docs say “returns X”, search for:

- `GetNew...` naming;
- dispose/release/checkin pair;
- sample cleanup;
- header comment;
- handle type.

Do not infer borrowed/owned from pointer syntax.

## UTF-8 / UTF-16 evolution

Historical samples may use char buffers where newer suite generations return UTF-16 MemHandle.

Do not port only function name and ignore string/ownership contract changes.

## Platform docs

Signing, debugger attach, installer and UXP/CEP roadmap facts are time-sensitive.

For these, current Apple/Microsoft/Adobe platform documentation may outrank old SDK guide snapshots.

Record review date.

## How to write an erratum

Use a compact record:

```text
topic
observed source A
observed source B
exact baseline chosen
reason
version boundary
impact on Bible/code
```

## Bible policy

Executable-looking native snippet should be one of:

- SDK-CONTRACT-REVIEWED;
- SOURCE EXAMPLE with explicit baseline;
- historical/sample-derived with version note;
- RECONSTRUCTED and clearly labeled.

Do not label source `binary-tested`/`runtime-observed` without corresponding evidence.

## What absence of runtime evidence means

It means only:

> Bible does not claim that runtime result.

It does **not** mean the documentation is incomplete if the chapter is about documented/source contract rather than measured runtime behavior.

## Stop rule

When header, sample and guide disagree:

1. stop;
2. identify exact SDK baseline;
3. classify mismatch;
4. update Bible with explicit provenance;
5. never cast/guess merely to make an example look consistent.

## Related

- [Header-first rules](../18-SDK-HEADER-TOOLS/04-HEADER-FIRST-RULES.md)
- [SDK diff policy](../18-SDK-HEADER-TOOLS/03-SDK-DIFF-POLICY.md)
- [SDK contract audit tools](../18-SDK-HEADER-TOOLS/README.md)
