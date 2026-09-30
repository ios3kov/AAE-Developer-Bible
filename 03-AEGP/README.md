# AEGP

AEGP (After Effects General Plug-in) нужен для глубокой интеграции с host через PICA suites и hooks.

## Когда выбирать

- menu command;
- project/item/layer manipulation на native уровне;
- render queue integration;
- keyframe/stream operations;
- hooks/idle callbacks;
- service, который должен предоставлять suites другим plug-ins;
- foundation для AEIO/Artisan.

## Когда не выбирать

- обычный pixel effect → Effect API;
- простая project automation → ExtendScript часто дешевле;
- rich UI panel → CEP/UXP + AEGP/native core при необходимости.
