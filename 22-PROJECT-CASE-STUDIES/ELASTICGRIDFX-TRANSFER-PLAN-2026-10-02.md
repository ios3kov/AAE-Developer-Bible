# План переноса опыта ElasticGridFX в Bible

Дата: **2026-10-02**. Статус: **источники прочитаны; перенос в главы запланирован**. Часть [плана завершения](../COMPLETION-PLAN.md).

Ретроспектива FSTR Stretch 0.9.3-perf.1 полезна как конкретный пример оптимизации native Effect без уменьшения качества и как пример ограниченных performance/release доказательств. Она дополняет core главы практическими случаями, но не устанавливает новые обязательные правила Bible и не подтверждает все продукты или версии AE.

## Источник и identities

Изучен documentation snapshot **`9d0162de64d01ceb41f6a1374a73544729ed0ec2`**:

- [Ретроспектива](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/retrospective-0.9.3-perf.1.md).
- [Обобщённый project know-how](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/AE_ENGINEERING_KNOWHOW.md).
- Shipping source: `f611312bd7b76ebe5bc5f2bd8b48b44f50c0c761`.
- Build ID: `EGFX-6147dc406abc596e7f2d1b60`; embedded version: 0.9.3 Develop Build 2.
- Package/tag: 0.9.3-perf.1 / v0.9.3-perf.1; release target `cb429e1ffab06cd79cb0873ba8909b2a8369198d`.
- Outer ZIP SHA-256: `a563f8e14961e19ee0740d5eb063c89e4bbec830ac1053d23fa09de02f2a6d14`.
- Recorded host: AE25.6x101, macOS26.6.2, M1 Pro, 16 GiB; recorded candidate toolchain: Apple Clang21 / Rust1.98.1, arm64 release profile.

Это identities из источника. В Bible они сохраняются как **PROJECT-REPORTED**, пока нет независимого повторения. Метку PROVEN исходного проекта нельзя автоматически преобразовать в Bible-owned RUNTIME-OBSERVED. Новая загрузка AE, сборка, установка и performance run в этой работе не выполнялись.

## Что добавить

| Урок | Куда добавить | Источник и граница | Проверяемый результат редакционного переноса |
|---|---|---|---|
| Сначала определить реально исполняемый render route | Performance architecture, profiling recipe, Effect anatomy | Plane entry points отличались от generic CPU renderer; instrumentation даёт attribution, не обычную скорость AE | Сценарий route → профиль → optimization target; запрет переносить timing другого path |
| Exact separable-axis/Bicubic caching | SmartFX, pixel/color, MFR/GPU, performance | Axis computations и четыре source rows переиспользуются только для eligible mappings; general/exceptional cases сохраняют прежний path | Схема eligibility/fallback, неизменного порядка arithmetic, call-local scratch и проверок; source example только после отдельного source review |
| Negative zero, NaN/Inf и нейтральные shortcuts | Pixels/color, render correctness, CPU/GPU equivalence | Первоначальный shortcut был rejected; исправленный candidate прошёл native byte comparisons с отдельной архитектурной областью | Отрицательный пример apparent identity ≠ byte identity; случаи signed zero/nonfinite и границы numerical policy |
| Matched-toolchain parity control | Render correctness, build systems, compatibility | Старый artifact отличался в 29 channels на шести matrix frames; unchanged source rebuilt с matching toolchain даёт отдельное exact comparison | Две отдельные записи: original-artifact deltas и matched-toolchain comparison; причина старого расхождения не объявляется установленной |
| Контракт export/decoder входит в identity сравнения | Render correctness, color, performance report | 32-bpc project экспортировался в straight RGBA16 PNG, decode независимый и calibrated | В template поля output precision/alpha/working space/decoder/calibration; encoded equality не называется native HDR/OCIO proof |
| Раздельные performance метрики | Performance testing, profiling, performance report | Native median ≈12.062×; ordinary AE export ratio of medians ≈1.3507×; Preview — интервалы наблюдения | Заполненный пример с separate metrics, pair counts, median definition, warmup, outliers, cache/order/capture limitations |
| Viewer resolution и Preview preset — разные состояния | Host verification, Custom UI, performance | Поздний Full readback не подтверждает preset прежней interval series; cache fill не равен first-playable latency | Таблица требуемых readbacks и наблюдений для каждого заявления; unknown preset остаётся unknown |
| Exit0 не доказывает завершение рендера | Host verification, render automation, crash diagnostics | Launcher exit0 сопровождался 19/60 outputs в прерванном control run | Completion contract: expected frame coverage + decode + process/image identity; отдельные launcher/render/output statuses |
| MFR requested не означает measured concurrency; non-reproduction не causal fix | MFR stress, crash diagnostics, evidence/acceptance | Исходный crash сохранён; bounded retries не повторили его, причина UNVERIFIED | Incident record отдельно от retry outcomes и user closure; запрещены speculative fixes и broad stability claims без evidence |
| Native gesture, effect result, Undo и latency — разные доказательства | Custom UI, host verification, bug-report template | Guide displacement и Undo наблюдались в названном сценарии; failed automation delivery исключена; latency не измерена | Functional gesture test с before/after/Undo; separate latency criterion; helper permissions не входят в plugin installation |
| Downloaded package и фактически loaded binary | macOS installation/debug, clean-machine acceptance, release artifacts | Quarantine retained, outer hash и loaded UUID проверены на существующем Mac; clean environment отдельно USER-REPORTED | Identity chain source → build → package → installed → loaded; controlled reinstall не называется clean-machine test |
| Save/reopen, animated legacy project и принятие пользователем | Version compatibility, parameters, release notes, case study | Instrumented selected-frame/user-scene checks отдельно от пользовательского сообщения о других средах | Старые project/state/animation fixtures, scoped acceptance и указание, какие raw fixtures не предоставлены |

Целевые главы находятся в [Performance architecture](../01-ARCHITECTURE/05-PERFORMANCE-ARCHITECTURE.md), [SmartFX](../02-EFFECT-PLUGINS/03-SMARTFX.md), [MFR](../02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md), [Pixels/color](../02-EFFECT-PLUGINS/06-COLOR-PIXELS.md), [Custom UI](../02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md), [Testing](../10-TESTING/README.md), [Distribution](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md), [Profiling recipe](../12-RECIPES/06-PROFILING.md), [Performance report](../13-TEMPLATES/PERFORMANCE-REPORT.md).

## Primary project records для переноса

Все ссылки закреплены на прочитанном snapshot:

- [Optimization/failure history](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-resume-2026-10-01.md).
- [Native corrected comparison](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-plane-corrected-comparison-2026-10-01.json).
- [Exceptional-float comparison](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-plane-nonfinite-comparison-2026-10-01.json).
- [Host matrix and original-artifact limits](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-host-matrix-2026-10-02.json).
- [Ordinary export samples and limits](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-host-render-2026-10-02.json).
- [Preview intervals and uncertainties](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-host-preview-intervals-2026-10-02.json).
- [MFR incomplete-output incident](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-host-mfr-2026-10-02.json).
- [Bounded retry closure](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/mfr-closure-retry-2026-10-02.json).
- [Native guide evidence](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/performance-host-guide-2026-10-02.json).
- [Downloaded-candidate check](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/public-install-project-check-2026-10-02.json).
- [Project validation](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/postrelease-project-validation-2026-10-02.json).
- [User-reported release acceptance](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/release-user-acceptance-2026-10-02.json).

Ретроспектива и know-how прочитаны полностью; основные JSON matrix/export/Preview/install/nonfinite/retry records просмотрены для сопоставления полей, scopes и ограничений. Все raw observations, private fixtures и прочие linked records независимо не повторялись. Перед написанием отдельного утверждения в главе читать целиком соответствующий первичный record; нельзя расширять его смысл по одному заголовку ретроспективы.

## Confidence и принятый outcome

Добавить в evidence chapter разделение трёх осей:

1. Статус выполненного теста: PASS/FAIL/BLOCKED/NOT_RUN.
2. Происхождение/уверенность: DOCUMENTED, SDK-CONTRACT-REVIEWED, PROJECT-REPORTED, RUNTIME-OBSERVED, RECONSTRUCTED; пользовательское сообщение обозначается USER-REPORTED явно.
3. Решение: accepted/rejected/closed within scope, которое не меняет исходный статус или неустановленную причину отказа.

Так можно сохранить «crash не воспроизведён в шести retries, пользователь закрыл investigation» без ложного вывода «причина устранена».

## Чего не переносить как правило или доказанный факт Bible

- «12× быстрее в AE», universal HDR/OCIO correctness и blanket MFR stability.
- Exact first-playable/gesture-to-display latency: в источнике нет такого measurement.
- Приписывание доли wall-time PNG encoding только по его наличию в sampled stack.
- Общую рекомендацию отказаться от signing/notarization на основании project-specific ad-hoc release policy. Совместимость, техническая возможность установки и политика распространения — разные вопросы.
- Project rules6.0.0 или central PR16 как автоматически принятую политику Bible; текущий редакционный guide сохраняет свой scope.
- User projects, media, private crash logs и privileged helper setup как публичный sample.
- Project PROVEN или user acceptance как независимо полученный Bible PASS.

## Инструменты как кандидаты для adaptation

На source snapshot существуют [render_observation.py](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/tools/render_observation.py), [live_identity.py](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/tools/live_identity.py), [perf_fixture_runner.py](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/tools/perf_fixture_runner.py).

Планировать сначала review, затем решение reuse/adapt/do not transfer. Проверить dependencies, imports install_candidate/build identity utilities, output paths, OS assumptions, AE invocation, timeouts, restoration и licensing. `perf_fixture_runner` имеет execute mode с host calls; наличие inspect mode не делает весь tool read-only. В этой работе tools не запускались и не копировались в Bible.

## Приёмка переноса

- [x] Immutable source snapshot и identities записаны.
- [x] Уроки сопоставлены с core chapters и блоками общего плана.
- [x] Отрицательные результаты и ограничения включены в задачи.
- [ ] Прочитать соответствующие primary records полностью перед написанием каждой темы.
- [ ] Дополнить core главы в их логических блоках, согласовать recipes/templates.
- [ ] Написать scoped ElasticGridFX case study после source/performance blocks.
- [ ] Проверить tool candidates отдельно и записать transfer decision; копирование необязательно.
- [ ] Проверить links, generated docs и evidence wording после каждого completed block.

Полное повторение performance/release матрицы ElasticGridFX не является условием готовности Bible. Предмет этого дополнения — применимые методы, точная область project evidence и полезные failure examples.
