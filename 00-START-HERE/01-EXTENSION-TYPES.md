# Extension types

## Effect plug-in

**Сильные стороны:** realtime/render path, pixels, GPU, SmartFX, MFR, параметры Effect Controls, возможность совместимости с Premiere при использовании поддерживаемого подмножества.

**Слабые стороны:** C++, ABI/lifecycle, сложное тестирование, host-managed memory, versioned suites.

## AEGP

**Сильные стороны:** широкий доступ к host functionality через PICA suites, hooks, menu commands, проектные данные.

**Слабые стороны:** сложнее lifecycle и invalidation; не заменяет effect API там, где нужен обычный per-frame effect render.

## AEIO

**Сильные стороны:** настоящий import/export pipeline для собственного media format.

**Слабые стороны:** вы отвечаете за codec/container side и корректную работу frames/audio/options.

## Artisan

**Сильные стороны:** контроль 3D rendering path.

**Слабые стороны:** огромный scope. Adobe SDK Guide прямо предупреждает, что это путь только при сильной необходимости.

## ExtendScript

**Сильные стороны:** быстро, просто распространять, огромная часть project automation.

**Слабые стороны:** legacy JS runtime, ограниченная производительность, не pixel plugin API.

## CEP

**Сильные стороны:** HTML/CSS/JS dockable UI, существующая ecosystem, shipping path в AE сегодня.

**Слабые стороны:** legacy; Adobe объявила retirement к концу 2029. Архитектурно завязан на CEF/CEP model.

## UXP

**Сильные стороны:** современное направление Adobe, более новый security/extensibility model.

**Состояние на 2026-09-30:** Adobe объявила UXP для AE, public beta запланирована к ноябрю 2026. Не проектировать текущий production AE продукт на ещё не выпущенный публичный API.

## Hybrid

Обычно лучший путь для коммерческого сложного продукта:

- C++ делает heavy compute и host-native работу;
- panel/script делает orchestration/UI;
- protocol между слоями маленький, versioned и testable.
