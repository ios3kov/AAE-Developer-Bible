# AEGP

AEGP (After Effects General Plug-in) — интеграция с приложением через PICA suites и callbacks. Его initializer отличается от EffectMain; команда меню не является пиксельным render callback.

## Маршрут чтения

1. [PiPL, регистрация и загрузка](../01-ARCHITECTURE/03-PIPL-AND-LOADING.md): разные точки входа, Kind, версии, экспорт, ресурсные цепочки Windows/macOS и границы диагностики загрузки.
2. [AEGP: инициализация, hooks и suites](01-HOOKS-SUITES.md): plugin/command IDs, global и hook refcon, версии suites, command/update/idle/death callbacks, частичная инициализация и UI suppression.
3. [Операции с проектом и рендером](02-PROJECT-RENDER-AUTOMATION.md): чтение project/item/comp/layer, время, Undo и частичные ошибки; очередь, enum статуса и invalidation; render options, borrowed worlds, sync/async receipts и кэш.
4. [Владение памятью и ошибки](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md): разные release API и пределы существующих ownership helpers.

Регистрация/PiPL и lifecycle hooks расширены **2026-10-01 по SDK 25.6 build 61**. [Запись сверки](../18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md) содержит 19 source hashes, диапазоны строк, сохранённые расхождения и разбор [MenuTool](../16-WORKING-TEMPLATES/aegp-menu-command/MenuTool.cpp). Проект/render automation разобран в [следующей сверке](../18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md), а streams/keyframes — в [SDK 25.6 review](../18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md). Старые Adobe samples используются как pattern evidence; актуальные signatures берутся из current headers.

[Сверка проекта и рендера](../18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md) добавляет диапазоны шести SDK-файлов и разбор трёх существующих рецептов. У RenderQueueRecipes обнаружено использование TRUE вместо именованного статуса: это не QUEUED. Ошибка и необходимость исправления кода отмечены в главе и README рецептов; host-проверка не заявляется.

## Когда рассматривать AEGP

Применимые направления, видимые в рассмотренных SDK объявлениях: команды меню, hooks/idle, операции с проектными объектами через специализированные suites, регистрация IO/Artisan. Наличие отдельного register API ещё не делает готовой реализацию соответствующего направления; каждому требуется свой контракт и пример.

Как рекомендация выбора технологии: обычная обработка пикселей относится к Effect API; для простой автоматизации сначала стоит оценить сценарный API. Наличие AEGP не означает, что любая панельная технология поддерживается конкретной версией host — её применимость проверяется отдельно.

## Границы готовности

Текст сверяется с declarations и samples; архитектурные рекомендации помечены отдельно. Source review не равен native build, удачная компиляция не равна загрузке, а успешный initializer не равен готовности всех функций.

[COMPLETION-CHECKLIST](../COMPLETION-CHECKLIST.md) сохраняет отдельную приёмку MenuTool: сборка/регистрация, отсутствие дублей меню, действие команды, update hook, ошибки и завершение. Редакционное обновление этих пунктов не закрывает. Следующий редакционный блок — AEIO и Artisan; это порядок чтения/написания, не закрытие более ранних gates.


## Текущий редакционный статус

Streams/properties, keyframes, masks, text/markers и footage/import теперь сверены с supplied SDK 25.6. Исправлены утечки later-SDK generations: baseline здесь использует `StreamSuite6`, `DynamicStreamSuite4`, `KeyframeSuite5` и `CompSuite12`. [Сверка masks/text/footage](../18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md) отдельно фиксирует ownership MaskRef, Text/Marker MemHandle и переход владения FootageH при adoption. Host execution этих cookbook операций всё ещё требует отдельной приёмки по `COMPLETION-CHECKLIST.md`.
