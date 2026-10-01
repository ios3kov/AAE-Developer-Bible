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
