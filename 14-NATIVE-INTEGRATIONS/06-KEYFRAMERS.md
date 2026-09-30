# Keyframers

Keyframer — specialization AEGP, обычно видимый как команда в **Animation > Keyframe Assistant**.

## Основная модель

1. Получить selection/property stream.
2. Проверить, keyframe-able ли stream.
3. Начать undo transaction.
4. Для массового добавления использовать begin/add/end family API, а не много независимых insert calls.
5. Изменить interpolation/ease/value/time.
6. Закончить undo transaction.

## Почему batching важен

Каждый отдельный insert может создавать дорогую undo/update работу. Для массовых операций использовать `AEGP_StartAddKeyframes` → add/set → `AEGP_EndAddKeyframes`.

## Что хранить

Не хранить `AEGP_StreamRefH` дольше, чем гарантирует API. Многие opaque handles становятся невалидными после структурных изменений проекта.

## Reference sample

Adobe SDK sample **Easy Cheese** — базовый ориентир Keyframe Assistant. Исторический **Mangler** показывает более сложный keyframer UI, но его старые ADM UI решения не следует переносить в новый продукт.
