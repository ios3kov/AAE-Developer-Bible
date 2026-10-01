# AE Developer Bible — editorial completion checklist

Updated: **2026-10-01**

Этот файл — **редакционный чеклист**, а не программа QA собственных плагинов.

## Definition of done

Bible готова как редакция, когда читатель может выбрать направление разработки и получить точную, непротиворечивую, source-grounded и практически применимую инструкцию без скрытых догадок о version-sensitive API.

## A. Mission and scope

- [x] Цель: practical developer knowledge base, не product plugin suite.
- [x] Есть decision tree выбора технологии.
- [x] Покрыты основные extension families.
- [x] Отдельно покрыты macOS и Windows workflows.
- [x] Testing/release описаны как процессы продукта разработчика.
- [x] Research atlas и case studies отделены от core API guide.

## B. SDK and source accuracy

- [x] Exact SDK baseline: Adobe After Effects SDK 25.6 build 61.
- [x] High-risk native chapters имеют source-review records.
- [x] Real SDK audit: 35/35 required contracts.
- [x] Cookbook audit: 39/39 call-sites resolve to expected suite generations.
- [x] Required parser diagnostics: 0.
- [x] Non-required parser limitations сохраняются явно.
- [x] Historical sample/header discrepancies документируются как version boundaries.
- [ ] Перед freeze редакции повторно проверить датированные внешние roadmap/platform facts.

## C. Evidence vocabulary

- [x] DOCUMENTED отделён от SDK-CONTRACT-REVIEWED.
- [x] Runtime/project observations не выдаются за общий API contract.
- [x] RECONSTRUCTED claims маркируются отдельно.
- [x] Source examples не называются готовыми binaries.
- [x] Отсутствие собственного host-run не считается незакрытым completion task Bible.
- [ ] Финальным проходом проверить старые главы на устаревшие verification labels.

## D. Chapter completeness

Для каждого основного направления проверить наличие:

- [ ] зачем/когда использовать;
- [ ] когда не использовать;
- [ ] architecture/lifecycle;
- [ ] ключевые suites/selectors/entry points;
- [ ] ownership/lifetime;
- [ ] threading/main-thread boundaries;
- [ ] version/platform caveats;
- [ ] error/failure behavior;
- [ ] production workflow;
- [ ] debugging/testing guidance;
- [ ] related recipes/templates;
- [ ] sources/version boundary.

Этот пункт закрывается **редакционным проходом по главам**, а не сборкой примеров.

## Editorial sweep progress — 2026-10-01

First completeness wave expanded and normalized:

- `00-START-HERE/01-EXTENSION-TYPES.md`;
- `00-START-HERE/02-ENVIRONMENT-MATRIX.md`;
- `01-ARCHITECTURE/01-LIFECYCLE.md`;
- `01-ARCHITECTURE/04-VERSION-COMPATIBILITY.md`;
- `01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md`;
- `06-SCRIPTING/README.md`;
- `07-PANELS/README.md`;
- `08-MACOS/README.md`;
- `08-MACOS/04-GPU.md`;
- `09-WINDOWS/README.md`;
- `09-WINDOWS/03-DEBUGGING.md`;
- `09-WINDOWS/04-GPU.md`;
- `14-NATIVE-INTEGRATIONS/01-TAXONOMY.md`;
- `14-NATIVE-INTEGRATIONS/02-HOST-CALL-FLOWS.md`;
- `14-NATIVE-INTEGRATIONS/05-AEGP-TOOLS.md`;
- `14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md`;
- `14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md`;
- `17-NATIVE-SUITE-COOKBOOK/13-GUIDES-VIEWS-SELECTION.md`;
- SDK header-first/diff methodology was reconciled with the documentation mission.

These chapters now explicitly separate product validation guidance from Bible editorial evidence.

### Cookbook project/render block — completed 2026-10-01

Checked and reconciled as one logical block:

- compositions: SDK 25.6 baseline `CompSuite12`; later `CompSuite13` remains explicitly version-gated;
- layers: `LayerSuite9` + `CompSuite12`, stable-ID/invalidation guidance;
- render frames: current `RenderSuite5`/RenderOptions4/World3; older recipe `RenderSuite4` is explicitly compatibility-shaped source;
- render queue: current `RQItemSuite4` + OutputModule4; older recipe `RQItemSuite3` is explicit compatibility source;
- render-item state uses named `AEGP_RenderItemStatus_QUEUED`, not Boolean `TRUE`;
- required-contract manifest matches the same current SDK generations.

No compiler/host run is required for this editorial block; runtime results are not claimed.

## E. Recipes and reference source

- [x] Recipes/source examples отделены от лицензированных Adobe sample projects.
- [x] Для native examples объяснён sample-first подход.
- [x] Examples используют source-level evidence labels, а не обязательный host-test TODO.
- [ ] Проверить все examples/recipes на противоречия с текущими основными главами.
- [ ] Проверить snippets на устаревшие suite generations/названия.
- [ ] Удалить остаточные формулировки, где example ошибочно выглядит как обязательный release artifact Bible.

## F. Cross-section consistency

- [x] Старый completion model с обязательными build/host Gates 4–9 отменён.
- [x] Compile/host evidence сохранён как evidence, а не как условие готовности Bible.
- [x] Research atlas больше не блокирует core edition.
- [x] Сверить README / STATUS / coverage / VERIFICATION и удалить старую mandatory build/host gate model.
- [ ] Проверить cross-links и navigation.

## G. Research appendices

- [x] Case-study reuse audit сохранён.
- [x] 3D Channel Extract pilot имеет evidence audit и superseded-claim handling.
- [x] Private/internal API experiments отделены от supported SDK guidance.
- [ ] Продолжать atlas по мере ценности; полный каталог не обязателен для core release.

## H. Editorial release

- [ ] Проверить public links и датированные факты.
- [ ] Проверить third-party/provenance notices.
- [x] Пересобрать MASTER и manifest после editorial-model correction.
- [x] Прогнать strict documentation build после editorial-model correction.
- [x] Проверить generated navigation / MkDocs strict validation.
- [x] Обновить STATUS / coverage / changelog под documentation mission.
- [ ] Зафиксировать edition date/version.

## Не требуется для закрытия этого чеклиста

- build всех C++ examples;
- host-run всех examples;
- Windows/MSVC compile всей Bible;
- macOS/Xcode compile всей Bible;
- signing/notarization demo binaries;
- clean-machine install demo binaries;
- exhaustive CPU/GPU/MFR QA всех source snippets;
- полный reverse-engineering каждого bundled effect.

Такие проверки полезны для продуктов, которые разработчик строит по Bible, и могут давать дополнительное evidence для отдельных примеров, но не определяют готовность документации.

## Current next step

**Section-by-section editorial completeness sweep.**
