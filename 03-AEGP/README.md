# AEGP

AEGP (After Effects General Plug-in) — интеграция с приложением через PICA suites и callbacks. Его initializer отличается от EffectMain; команда меню не является пиксельным render callback.

## Маршрут чтения

1. [PiPL, регистрация и загрузка](../01-ARCHITECTURE/03-PIPL-AND-LOADING.md): разные точки входа, Kind, версии, экспорт, ресурсные цепочки Windows/macOS и границы диагностики загрузки.
2. [AEGP: инициализация, hooks и suites](01-HOOKS-SUITES.md): plugin/command IDs, global и hook refcon, версии suites, command/update/idle/death callbacks, частичная инициализация и UI suppression.
3. [Операции с проектом и рендером](02-PROJECT-RENDER-AUTOMATION.md): следующий раздел для подробной редакционной сверки с поставкой SDK.
4. [Владение памятью и ошибки](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md): разные release API и пределы существующих ownership helpers.

Регистрация/PiPL и lifecycle hooks расширены **2026-10-01 по SDK 25.6 build 61**. [Запись сверки](../18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md) содержит 19 source hashes, диапазоны строк, сохранённые расхождения и разбор [MenuTool](../16-WORKING-TEMPLATES/aegp-menu-command/MenuTool.cpp). Сам MenuTool не менялся и не запускался в этой итерации.

## Когда рассматривать AEGP

Применимые направления, видимые в рассмотренных SDK объявлениях: команды меню, hooks/idle, операции с проектными объектами через специализированные suites, регистрация IO/Artisan. Наличие отдельного register API ещё не делает готовой реализацию соответствующего направления; каждому требуется свой контракт и пример.

Как рекомендация выбора технологии: обычная обработка пикселей относится к Effect API; для простой автоматизации сначала стоит оценить сценарный API. Наличие AEGP не означает, что любая панельная технология поддерживается конкретной версией host — её применимость проверяется отдельно.

## Границы готовности

Текст сверяется с declarations и samples; архитектурные рекомендации помечены отдельно. Source review не равен native build, удачная компиляция не равна загрузке, а успешный initializer не равен готовности всех функций.

[COMPLETION-CHECKLIST](../COMPLETION-CHECKLIST.md) сохраняет отдельную приёмку MenuTool: сборка/регистрация, отсутствие дублей меню, действие команды, update hook, ошибки и завершение. Редакционное обновление этих пунктов не закрывает.
