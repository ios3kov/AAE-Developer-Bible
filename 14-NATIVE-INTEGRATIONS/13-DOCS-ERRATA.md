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

## Полный intro/PPro source review — 2026-10-08

Закреплённый public guide `6d9b285d9755d1fbf8ead7680ba49de24f94b547` содержит
одновременно новые и исторические указания. Это не новый exact SDK26.5 audit.

| Источник | Граница применения в Библии |
|---|---|
| [Exceptions](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/exceptions.md), строки 3–5 | Совет передать чужое exception обратно AE противоречит следующему запрету. Не превращать его в разрешение unwinding через callback; применяется [containment policy](../19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md) |
| [Apple Silicon](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/apple-silicon-support.md), строки 49–64 | Неполный пример `EffectMain` и `catch` не являются точным C++ declaration; форма берётся из SDK25.6 baseline |
| [Symbol export](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/symbol-export.md), строки 7–41 | Слово «entry» не основание удалить dispatcher или registration export. Их разные роли уже разобраны в [PiPL chapter](../01-ARCHITECTURE/03-PIPL-AND-LOADING.md) |
| [SDK audience](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/sdk-audience.md), строка 15 | Список старых проверенных IDE не задаёт современные требования всех target; Windows ARM64 guidance требует VS17.4+, а exact sample имеет собственный toolset |
| [Other integration](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/other-integration-possibilities.md), строки 11,37–39 | Исторические заявления о поставке ESTK, защите через JSXBIN и произвольном scripting через aerender не превращены в текущие tooling/security/CLI гарантии |

Исторические разделы What's New читаются в границах своих версий: утверждения
2021 года об Apple Silicon или 13.5 об async work-in-progress не отменяют более
поздних контрактов. Номер guide release не переносит эти старые абзацы в настоящее.

## Native effects public-guide review, 2026-10-08

Полностью прочитаны 38 страниц effect-basics, effect-details, effect-ui-events и
SmartFX в [snapshot 6d9b285](https://github.com/docsforadobe/after-effects-plugin-guide/tree/6d9b285d9755d1fbf8ead7680ba49de24f94b547).
Это DOCUMENTED review; ранее проверенные SDK 25.6 declarations не заменены guide.

| Расхождение | Классификация и решение |
|---|---|
| [PF_ParamDef](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-basics/PF_ParamDef.md#L22-L26) разрешает change flags в UPDATE_PARAMS_UI; selector/supervision pages запрещают value mutation | Несогласованная таблица. Сохранён запрет SDK 25.6; косметика через копию для `PF_UpdateParamUI` |
| [PF_InData.shutter_angle](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-basics/PF_InData.md#L120-L128): 0…1 для оборота рядом с примером `==180` | Противоречивые единицы. Не выводить числовую shutter formula из этой страницы |
| [PF_InData](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-basics/PF_InData.md#L244-L258) prose предлагает менять input origin, `PF_OutData` описывает output width/height/origin | Ошибочная ссылка на структуру; текущий header-first resize contract сохранён |
| [Parameter-types page](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-basics/parameters.md#L88-L94) называет `path_id` индексом; PathQuery отдельно переводит index в unique ID | Не считать ID и index взаимозаменяемыми; bridge определяется точным API |
| [Command tables](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-basics/command-selectors.md): `PF_Cmd_PARAM_SETUP`, `PF_Cmd_GPU_SMART_RENDER_GPU` | Опечатки не вводят новые selectors; действуют имена из текущих главы/headers |
| [Integer slider](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-basics/parameters.md) помечен «No longer used», хотя supplied Skeleton его использует | Историческое обобщение. Сохраняемый тип и disk ID не меняются по одной строке guide |
| [Заголовок «Change defaults? Change IDs»](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-details/changing-parameter-orders.md) | Не общая migration policy. Стабильные IDs, old-project value и Reset default рассматриваются раздельно |
| [Compute Cache hash sample](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-details/compute-cache-api.md#L150-L186) использует `sizeof` pointer и не завершает return/error paths | Иллюстрация не готова к переносу в native callback; hash inputs и cleanup описаны отдельно |
| [Sequence page](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-details/global-sequence-frame-data.md#L68-L101) разрешает менять contents при любом selector, затем вводит MFR const | Старую общую формулировку читать с более узким современным MFR contract |
| [Drawbot release prose](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/effect-ui-events/custom-ui-and-drawbot.md#L152-L160) дважды называет Supplier; старый sampling UI пишет state в render и keys в DRAW | Не подмена ownership из reviewed SDK и не современный MFR recipe |

SmartFX legacy `func`, положительный/non-negative checkout ID и optional early
pixel checkin уже разобраны выше; этот review не отменяет предыдущие исправления.
Уточнение bounds также сохраняется: неизменность `max_result_rect` относится к
выбору request, а не к любому времени/параметрам. Неиспользованный input допустим;
«one-to-one» в guide не требует получать pixels каждого объявленного input.

Сами главы теперь дают операции для path/segment ownership, keyframe checkout,
dependency flags, sampling, gesture/Drawbot и MFR cache. Наличие page ledger не
означает полной инвентаризации всех SDK declarations или нового host PASS.

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

## AEGP / AEIO / Artisan / audio public-guide review, 2026-10-08: расхождения, которые нельзя копировать в код

| Участок | Редакционное решение |
|---|---|
| Project getters используют TimeDisplay3 рядом с разделом TimeDisplay2; несколько setter rows печатают имена других функций | Сохранить generation и exact SDK declaration, не собирать ABI из соседних таблиц |
| `GetLayerSourceItemID` описан как layer ID | Не заменять source-item identity на `GetLayerID` / `LayerIDVal` |
| `GetRenderState`/`SetRenderState` напечатаны с Boolean | Сохранить уже проверенный SDK25.6 enum и исправление TRUE→QUEUED |
| `ReportInfo` приписан ItemSuite; `GetLayerParentComp` — CompSuite | Навигация ведёт к Utility и Layer operations соответственно |
| AUDIO_SETUP prose: startsampL/endsampL | PF_InData/PF_OutData страницы используют `start_sampL`/`dur_sampL`; не изобретать `endsampL` |
| Artisan field-of-view: две несовместимые формулы | Из `tan(θ)=H/(2f)` алгебраически следует `f=H/(2tan(θ))`. Это исправление преобразования формулы, не подтверждение units/projection современного renderer |

Источники: [suites](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aegps/aegp-suites.md), [AEGP details](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aegps/aegp-details.md),
[effect bridge](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aegps/cheating-effect-usage-of-aegp-suites.md), [audio range](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/audio/accessing-audio-data.md),
[Artisan geometry](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/artisans/artisan-data-types.md). Для audio spelling дополнительно проверены
`docs/effect-basics/PF_InData.md:169–175` и `PF_OutData.md:44` того же pin;
provenance этих страниц включается в соседний native-effects ledger.
