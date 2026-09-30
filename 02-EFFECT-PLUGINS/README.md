# Effect plug-ins

Effect plug-in — основной путь, если инструмент должен обрабатывать/генерировать pixels или audio внутри стандартного effect pipeline AE.

## Порядок разработки

1. Взять **Skeleton** или максимально близкий SDK sample.
2. Добиться clean build и загрузки без собственных изменений.
3. Переименовать sample и PiPL identifiers.
4. Реализовать CPU reference path.
5. Добавить 8/16/32-bpc correctness.
6. Перевести на SmartFX там, где это оправдано/необходимо.
7. Сделать thread-safe.
8. Только после этого включать MFR flag.
9. Добавить GPU backend, если benchmark доказывает пользу.
10. Custom UI — последним, после стабильной render core.

## Production layers

```text
AE entry point / selectors
        ↓
Adapter: PF_* ↔ internal types
        ↓
Pure render core
        ↓
CPU backend / GPU backend
        ↓
Tests + golden images
```

Чем меньше AE-specific типов проходит в render core, тем проще тестировать алгоритм вне After Effects.
