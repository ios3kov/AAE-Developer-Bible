# Parameters and Effect UI

## Native parameters first

Если UI можно выразить стандартными AE controls — slider, checkbox, color, popup, layer и т.п. — сначала использовать их.

Причины:
- automation/keyframes работают естественно;
- accessibility/host theme лучше;
- меньше custom event code;
- меньше platform-specific bugs;
- проекты сохраняют значения стандартным путём.

## Parameter stability

После публичного релиза parameter layout — сериализованный контракт.

Правила:
- стабильные parameter IDs;
- append/migrate вместо случайной перестановки;
- тест открытия проекта из N-1 версии plug-in;
- extreme/min/max/default values входят в fixtures.

## Custom UI / Drawbot

Custom UI нужен, когда стандартных controls недостаточно: overlay, handles, custom visualization.

Drawbot предоставляет host abstraction для paths/fill/stroke/image/text capabilities. Drawing выполняется в предназначенной для этого draw event фазе, а не произвольно из drag/click callback.

Custom UI должен:
- не выполнять тяжёлый render;
- отделять interaction state от render state;
- invalidation/rerender запрашивать через поддержанный host mechanism;
- соответствовать host theme, где доступна theme suite;
- работать на HiDPI/Retina.

## Full application-like UI

Если нужен browser-like rich panel, asset list, settings, accounts, web content — это **panel technology (CEP/UXP)**, а не попытка превратить Effect Controls в приложение.
