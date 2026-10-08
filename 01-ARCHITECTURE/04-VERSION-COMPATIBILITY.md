# Version compatibility

Compatibility in After Effects development is not one boolean.

A plug-in can be:

- source-compatible but not binary-compatible;
- binary-loadable but semantically broken;
- compatible on one CPU architecture and not another;
- compatible in AE but not in another host;
- compatible for basic render but not for MFR/GPU/custom UI.

Define the contract explicitly.

## Compatibility layers

### 1. Source compatibility

Can the code compile against a given SDK/toolchain?

Affected by:

- removed/changed declarations;
- suite generations;
- calling conventions;
- platform headers;
- compiler language rules.

### 2. Binary/loader compatibility

Can the built artifact be discovered and loaded?

Affected by:

- PiPL/resource declarations;
- architecture;
- exported entry points;
- package layout;
- dependent libraries;
- signing/platform trust.

### 3. Runtime API compatibility

Do required suites/selectors/features exist at runtime?

Affected by:

- host version;
- suite acquisition/version;
- optional capabilities;
- host-product differences.

### 4. Semantic compatibility

Does the same operation still behave as the product expects?

Examples:

- project mutation semantics;
- color behavior;
- render/cache behavior;
- custom UI lifecycle;
- GPU backend behavior.

### 5. Project/data compatibility

Can projects created with one plug-in version reopen safely with another?

Affected by:

- parameter IDs;
- match names;
- sequence data;
- persistent schemas;
- defaults;
- migration logic.

## SDK baseline vs supported AE range

Do not write:

> built with SDK 25.6, therefore supports AE 25.6+

That inference is not automatic.

An SDK baseline tells you which source contracts you used. Product support range is a separate policy.

## Suite version gating

For PICA/AEGP suites:

~~~text
need feature
→ know suite name + public version
→ acquire
→ handle unavailable/older version
→ use
→ release
~~~

Do not cast an older suite pointer to a newer struct just to avoid branching.

If feature is optional, degrade gracefully.

If feature is fundamental, fail early with a useful compatibility message.

## Effect selectors and flags

Effect plug-ins also have compatibility contracts in:

- PiPL;
- API version fields;
- global outflags;
- selector handling;
- SmartFX/MFR/GPU capability declarations.

Advertising a capability can cause the host to call selectors/paths the plug-in must actually implement.

## Stable identity

Changing these can break existing projects:

- match name;
- parameter IDs;
- persistent data schema;
- effect registration identity.

Display name is not the same thing as persistent identity.

Plan renames separately from ABI/project identity.

## Parameter evolution

Safe parameter evolution requires deliberate IDs.

Typical rules:

- never recycle an old parameter ID for a different meaning;
- append/add parameters carefully;
- define migration/default behavior;
- preserve project interpretation.

UI index and persistent ID are different concepts.

## Persistent data

Version your own stored data.

Illustrative product policy, **not Bible's tested support matrix**:

~~~text
magic
schema version
payload size
payload
~~~

On load:

1. validate size/version;
2. migrate known old version;
3. reject/repair malformed state deliberately;
4. never reinterpret arbitrary old bytes as a new struct.

C/C++ struct layout is not a durable serialization format by default.

## Cross-architecture compatibility

### macOS

Universal support implies all native dependencies and nested components support required slices.

### Windows

ARM64 support is not implied by x64 source compiling.

Check:

- dependencies;
- installer paths;
- helper processes;
- GPU backends;
- code-generation assumptions.

## Host-product compatibility

Some AE SDK concepts overlap with Premiere or other Adobe hosts, but support must be explicit.

Do not infer Premiere compatibility from:

- shared headers;
- similar pixel structs;
- same MediaCore install path.

Check the exact host contract.

### Premiere Pro: отдельный маршрут Effect API

**DOCUMENTED / RUNTIME-NOT-CLAIMED, review 2026-10-08.** Полностью прочитаны девять
[PPro-страниц закреплённого public guide](https://github.com/docsforadobe/after-effects-plugin-guide/tree/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro).
В них есть исторические ветки CS/CC. Описанная модель помогает проектировать adapter,
но не устанавливает поддержку всех этих возможностей каждым новым PPro build.

[Host identity](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/ppro.md)
и [host IDs](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/third-party-plug-in-hosts.md):
`appl_id` равен `'PrMr'` и у Premiere Pro, и у Premiere Elements; `'FXTC'` обозначает
AE. Поэтому `PrMr` недостаточно для различения двух продуктов. Для такой задачи
guide указывает Premiere App Info Suite. Таблица Effect API major/minor содержит
исторические значения: это не номер приложения и не одинаковая capability с AE.
Проверять продукт, версию и требуемый контракт отдельно; сигнатуры Premiere-specific
suites брать из соответствующих headers, которых этот review не подменяет.

#### Request context и состояние

[Basic differences](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/basic-host-differences.md)
описывает следующие различия:

| Вход или событие | Что учитывать |
|---|---|
| Time | Использовать отношение time values; не фиксировать исторический `time_scale` |
| Playback / Paused render | Одно время может запрашиваться с разными resolution/bit depth; `quality` относится к monitor |
| Native-format field render | `PF_Cmd_RENDER` приходит для поля; `height` — половина кадра, `rowbytes` удвоено относительно обычного кадра |
| Scheduling | Возможны speculative, повторные и непоследовательные запросы; cached frame может не вызвать effect |
| Instances | Разные экземпляры вызываются параллельно; описанная serialization одного instance исключает arbitrary callbacks |

**Рекомендация adapter:** сначала нормализовать фактические format, stride, dimensions,
field, time и quality, затем вызывать ядро. Cache key не должен состоять только из
времени. Не хранить последний отрендеренный кадр как обязательный вход следующего.
Suite acquisition failure обрабатывать до обращения к таблице; наличие AE utility
не предполагать. Guide показывает отдельные callback/macro alternatives, например
`PF_COPY` и `PF_FILL`; применимость к формату всё равно проверяется.

В parameter UI PPro `PF_ParamFlag_START_COLLAPSED` не учитывается. Для перемещения
time needle без ключей guide с CC2015 связывает доставку `PF_Cmd_UPDATE_PARAMS_UI`/
`PF_Event_DRAW` с `PF_OutFlag_NON_PARAM_VARY`: интерфейс должен переживать пропуски
redraw, а флаг соответствовать реальным зависимостям эффекта. Экспоненциальная шкала
описана через `PF_ADD_FLOAT_EXPONENTIAL_SLIDER`; точную форму macro и доступность
брать из выбранных headers, а не восстанавливать по примеру чисел в guide.

[Multithreading note](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/multithreading.md)
советует не включать `PF_OutFlag2_PPRO_DO_NOT_CLONE_SEQUENCE_DATA_FOR_RENDER` из-за
проблем parameter UI. Этот флаг не является общей оптимизацией памяти и не заменяет
спроектированное владение состоянием.

#### Pixel formats, checkout и unsupported paths

[Bigger differences](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/bigger-differences.md)
описывает отдельную регистрацию поддерживаемых форматов и float-обработку через
`PF_Cmd_RENDER`; перенос AE 16-bit/SmartFX пути этим разделом не обещан. Исходники
**SDK Noise** служат ориентиром для PPro float/YUV adapter. Обычные 8-bit AE helpers
нельзя применять к произвольному BGRA/YUV/float buffer.

Для дополнительных checkout guide описывает opt-in на `PF_Cmd_GLOBAL_SETUP`, чтобы
`PF_CHECKOUT_PARAM` возвращал формат render request; без него исторический путь
возвращает ARGB8. Поэтому проверять и основной input, и checked-out input: один
не устанавливает layout другого. Отдельно учитывать настройки глубины preview и
export; успех одного маршрута не доказывает другой.

[Unsupported features](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/unsupported-features.md)
не обещает AEGP, AE audio, auxiliary/3D и ряд sampling/world utilities. В описанном
PPro host `PF_OutFlag_I_USE_AUDIO` препятствует загрузке. Не рекламировать такой
Effect как общий video-host payload только из-за расположения в MediaCore.
Успешный discovery AEGP также не означает поддержку его callbacks: отсутствие
обязательной AE suite должно завершать инициализацию ошибкой до регистрации работы.

#### Кэш загрузки и presets

[Plug-ins reloaded](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/plug-ins-reloaded.md)
описывает сохранение части PiPL/`GLOBAL_SETUP` capabilities между запусками.
Для диагностики изменённой регистрации: установить один идентифицированный binary
→ перезапустить PPro с описанным guide Shift-reload → проверить фактически загруженный
путь и полученные capabilities. Это отдельный механизм от frame cache и не hot reload.
Guide также называет `PF_SetNoCacheOnLoad` для намеренного отказа от кэша; точную
форму и применимость брать из Premiere headers, не конструировать callback по названию.

Preset PPro создаётся из применённого эффекта с выбранными значениями/ключами через
Save Preset, затем Export Preset. Его схема отдельна от AE presets. Описанная установка
presets в plug-in directory делает их read-only; пользовательские presets остаются
редактируемыми. Исторические Vista-пути не использовать как современный универсальный
installer target. Custom ECW UI workaround на этой же странице предлагает отдельный
data parameter и supervision: отображение не должно становиться единственным
хранилищем значения.

Для стороннего host применять тот же принцип capability adapter. Раздел
[Other hosts](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/other-hosts.md)
не даёт поддержки Adobe для сторонней реализации host; историческое отсутствие
SmartFX у других hosts не превращается в бессрочную таблицу рынка.

## Compatibility matrix

Product support statement should distinguish **supported** and **tested evidence**.

Example:

| Host | mac arm64 | mac x86_64 | Win x64 | Win ARM64 | Policy |
|---|---:|---:|---:|---:|---|
| AE 25.x | supported | no | supported | no | supported |
| AE 26.x | supported | no | supported | planned | supported with stated limits |
| Beta | lab | no | lab | lab | no customer support promise |

Avoid treating “Beta opened once” as a support claim.

Keep these identities in separate fields, for example:

| Field | Bible example | What it does not establish |
|---|---|---|
| SDK release | 25.6 build61 | A supported AE range |
| Suite type | `AEGP_StreamSuite6` | Numeric public version guessed from suffix |
| Host | Exact AE build recorded by a product | Every patch in the marketing major |
| Artifact target | macOS arm64 or Windows x64 | Other slices, dependencies or host support |
| Evidence | Syntax/type check or source review | Discovery/load/render/signing success |

Failure walkthrough: a command needs a required suite → acquire with the exact
name/public-version macros → if unavailable, return unsupported before mutation.
An optional fallback must acquire its own typed older contract and state semantic
limits; do not cast the unavailable/new table or silently claim equivalent output.

## New AE release workflow

When a new AE release appears:

1. read Adobe release/SDK notes;
2. diff relevant SDK/header contracts if SDK changed;
3. identify changed high-risk areas;
4. load existing product artifact where policy allows;
5. exercise representative project/render workflows;
6. check MFR/GPU/UI paths used by the product;
7. check save/reopen and persistent state;
8. update support statement only after evidence is adequate.

This workflow belongs to the product team. Bible documents the method; it does not need to perform it for every version.

## New SDK adoption workflow

Published26.5 delta now has a [scoped currentness/source map](../CURRENTNESS-REVIEW-2026-10-07.md#native265-public-contract-reconciliation).
Guide/ItemView, Comp13 mesh creation and Stream7 sampling stages must be treated
as feature contracts, not replacements for the entire25.6 baseline. PProBeta27-only
PiPL metadata/preview additions do not establish AE support.

Do not begin with “fix compiler errors until green”.

Use:

~~~text
old SDK contract
+ new SDK contract
→ declaration diff
→ classify changes
→ inspect official samples/comments
→ update source/gating
→ update documentation/support policy
~~~

The [SDK contract tools](../18-SDK-HEADER-TOOLS/README.md) exist to help with this review.

## Version-sensitive documentation

When Bible names a specific suite generation or platform rule, include its boundary.

Good:

> SDK 25.6 exposes StreamSuite6 in the supplied baseline.

Bad:

> StreamSuite6 is always the current stream API.

Future editions may use another baseline.

## Deprecation and legacy samples

Official SDK bundles can contain old samples using older suite generations.

Treat them as:

- pattern evidence;
- lifecycle examples;
- historical compatibility examples.

Do not automatically treat sample signatures as the newest contract when current headers differ.

## Graceful degradation

Feature gating should be deliberate.

Example:

~~~text
if new suite available:
    enable advanced feature
else:
    use documented fallback
~~~

Do not silently run a partially equivalent fallback that changes project/render semantics.

## Compatibility failures to plan for

- suite unavailable;
- newer project data loaded by older plug-in;
- unsupported CPU architecture;
- missing nested dylib/DLL;
- changed GPU capability;
- host calls optional selector now advertised by flags;
- old sample copied with obsolete ABI;
- panel runtime migration;
- installer finds multiple AE versions.

## Documentation/release language

Prefer precise language:

- “supported”;
- “tested on”;
- “known issue”;
- “experimental”;
- “not supported”.

Avoid:

- “should work everywhere”;
- “compatible with all newer AE versions”;
- “future proof”.

## Related chapters

- [Environment matrix](../00-START-HERE/02-ENVIRONMENT-MATRIX.md)
- [PiPL and loading](03-PIPL-AND-LOADING.md)
- [SDK diff policy](../18-SDK-HEADER-TOOLS/03-SDK-DIFF-POLICY.md)
- [Compatibility matrix template](../13-TEMPLATES/COMPATIBILITY-MATRIX.md)
- [Distribution](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)

## Evidence boundary

Current Bible native baseline is SDK 25.6 build 61. The chapter describes compatibility design methodology; it does not claim universal compatibility for Bible source examples.
