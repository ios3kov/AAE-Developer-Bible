# Native public guide: полная сверка страниц

Дата: **2026-10-08**. Parent Bible revision:
`4bf9d4e079d46b2dfb6407d27613e057a27e69a8`.

Полностью прочитаны и сопоставлены с практическими главами **89/89 Markdown
страниц под `docs/`** в public guide. Точная native база остаётся **SDK25.6 build61**.
Эта работа закрывает чтение выбранного публичного документа; она не подменяет
отсутствующий exact SDK26.5 archive, его headers, utilities и samples.

## Источник и предел полноты

| Поле | Значение |
|---|---|
| Repository | [docsforadobe/after-effects-plugin-guide](https://github.com/docsforadobe/after-effects-plugin-guide/tree/6d9b285d9755d1fbf8ead7680ba49de24f94b547) |
| Commit | `6d9b285d9755d1fbf8ead7680ba49de24f94b547`, 2026-09-11 |
| Git tree | `35566e8001d791aa6322602978df27ae5da4ceee` |
| Исходный scope | Все 89 `.md` blobs под `docs/`, включая history/index/shared navigation |
| Exact bytes / lines | 2 953 983 / 12 918 |
| Inventory | [native-guide-inventory-2026-10-08.json](native-guide-inventory-2026-10-08.json) |
| Редакционная карта | [native-guide-reviewed-2026-10-08.json](native-guide-reviewed-2026-10-08.json) |

Три непересекающихся части: 31 intro/Premiere Pro/provenance страница,
38 Effect/UI/SmartFX страниц и 20 AEGP/AEIO/Artisan/audio страниц. Проверены точные
Git blob SHA1, размеры и SHA256. Декоративный table padding убирался только из
копий для чтения; provenance рассчитывается по неизменённым raw bytes.

Guide — community-maintained публикация Adobe SDK material. Его старые и новые
поколения suites сосуществуют: `GuideSuite2`, `ItemViewSuite2`, `CompSuite13`,
`StreamSuite7` не делают соседние `EffectSuite4`/`KeyframeSuite3` современными
заменами проверенных SDK25.6 declarations. Конкретные расхождения сохранены
в [errata](14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md).

Особенно большая `aegp-suites.md` прочитана целиком: 1 188 864 bytes / 4 141 строка,
SHA256 `c27d64011443b983b379d1c6c2279d29fc35fb0a50bd6eed5436cf0f872be0c7`.
Её 88 headings и 596 именованных строк таблиц сопоставлены с разделами Bible.
Map сохраняет поля структур, повторения, legacy и опечатки. Это **не** 596 уникальных
функций текущего SDK, отдельный implementation для каждой строки или автоматически
восстановленный C ABI. Ранее датированные partial reviews той же страницы остаются
partial reviews своего времени.

## Что добавлено в главы

| Область | Практическое дополнение |
|---|---|
| [Compatibility](01-ARCHITECTURE/04-VERSION-COMPATIBILITY.md), [PiPL](01-ARCHITECTURE/03-PIPL-AND-LOADING.md), [install](11-DISTRIBUTION/04-INSTALL-LOCATIONS.md) | PPro/Elements host identity, time/fields/depth/checkout и UI differences; Rez string bounds, media/import/display routes, historical preview versus Beta27 metadata |
| [Effect anatomy](02-EFFECT-PLUGINS/01-ANATOMY.md), [parameters](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md) | Dependency/dialog/error commands, localization, keyframe/path checkout and cleanup; explicit rejection of input parameter0 in UI helper |
| [SmartFX](02-EFFECT-PLUGINS/03-SMARTFX.md), [MFR](02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md) | Empty/bounds-only requests, ROI versus max bounds, checkout IDs/stages, dependency flags; host-call lock boundary, cache recomputation, request versus thread state |
| [Pixels](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md), [Drawbot](02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md) | Typed world and graphics constraints, PAR/coordinates/iteration; drag lifecycle, inverse-transform failure, draw-state/text/image ownership boundaries |
| [AEGP hooks](03-AEGP/01-HOOKS-SUITES.md), [memory/persistence](17-NATIVE-SUITE-COOKBOOK/12-MEMORY-UNDO-PERSISTENCE.md) | Third-party suite readiness after initializer; preference getters can write defaults, existence and migration separated; MemorySuite accounting scope |
| [Project/render](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md), [queue](17-NATIVE-SUITE-COOKBOOK/11-RENDER-QUEUE.md) | UI getters with window side effects; SoundData acquisition/lock/copy/cleanup; monitor listener IDs/statuses/text ownership and shutdown limits |
| [Import](17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md), [AEIO](04-AEIO/README.md), [AEIO contract](14-NATIVE-INTEGRATIONS/08-AEIO.md) | Media decoder versus project FIM translator; incoming world depth versus export depth; host output reservation, Collect Files close/reopen, folder and unconfirmed OutSpec cases |
| [Artisan](05-ARTISAN/README.md), [audio](02-EFFECT-PLUGINS/07-AUDIO.md) | Interactive versus final renderer scope, transform/view times and receipt semantics; visual audio analysis, clip-tail limit and automation metadata |

Existing detailed recipes were retained when they already covered the operation.
New architecture recommendations are distinguished from documented host contracts.
Native signatures were not reconstructed from malformed public tables.

## Существенные исправления источников

Errata now record conflicting exception guidance, incomplete effect/cache snippets,
Drawbot spelling/lifetime omissions, AEGP setter names and suite attribution,
`GetLayerSourceItemID` identity, Boolean render-state declarations, and audio
`startsampL/endsampL` versus `start_sampL/dur_sampL`. AEIO public48 callback rows and
IOIn5/IOOut4 do not replace exact25.6 49 slots and IOIn7/IOOut6. The missing
`GetActiveExtent` in a bare-bones summary does not make its required callback optional.

Artisan's printed FOV transformation is algebraically inconsistent: from
`tan(θ)=H/(2f)` follows `f=H/(2tan(θ))`. The correction establishes the algebra only;
it does not establish the projection/units of an unreviewed current renderer.

## Воспроизведение inventory

Use the repository's Python documentation environment:

```sh
python scripts/audit_public_guide_inventory.py --profile native --output native-guide-inventory-2026-10-08.json
python -m unittest discover -s scripts -p 'test_public_guide_inventory.py' -v
python scripts/check_docs_consistency.py
python scripts/build_docs.py --check
mkdocs build --strict
```

For offline reproduction, supply `--tree-json` with the complete canonical Git tree
response and `--source-root` with raw files preserving source paths. The script
checks the **tree SHA**, distinct from the commit SHA, rejects a truncated tree,
duplicate/nonregular pages and byte/blob mismatches. It includes navigation pages
instead of silently omitting pages without API headings. Network access is needed
only when cached inputs are not supplied.

## Проверки и evidence

Exact source set/hash/blob checks and AEGP section/member range checks passed.
Local checks passed: public-guide inventory4/4, consistency11/11, UXP inventory3/3,
129-core checker, generated source-table freshness and whitespace. Python3.12.14
with pinned docs dependencies; strict MkDocs build completed in6.02 seconds.
Negative consistency fixtures intentionally report stale generated files.
Independent editorial review found and corrected a duplicated PPro paragraph and
the distinction between key-count and key-find outputs; final review found no
remaining blockers. Generated outputs are rebuilt and checked after recording
these results. Exact GitHub workflow evidence belongs to the later published record.

Public additions are **DOCUMENTED / RUNTIME-NOT-CLAIMED**. No new native compile,
installed suite acquisition, AE/PPro/Artisan/audio execution, SDK26.5 acceptance,
signing or driver result is asserted. Those are separate product claims, not a
reason to leave the documented operations unwritten.
