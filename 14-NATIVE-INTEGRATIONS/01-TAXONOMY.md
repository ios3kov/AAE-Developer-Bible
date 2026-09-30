# Native SDK taxonomy

## Effect plug-ins

### Core image effect
Получает input world + parameters и пишет output world. Host инициирует все вызовы.

### SmartFX
Использует `PF_Cmd_SMART_PRE_RENDER` и `PF_Cmd_SMART_RENDER`. Нужен для корректного deep/floating-point pipeline и сложной dependency/ROI логики.

### MFR-aware effect
Не отдельный API. Effect объявляет поддержку MFR только после того, как render path и sequence state безопасны для нескольких одновременно рендерящихся кадров.

### GPU effect
Не отдельный plug-in type. CPU effect получает GPU lifecycle/render selectors и `PF_GPUDeviceSuite`/GPU-specific context.

### Custom UI effect
Effect получает `PF_Cmd_EVENT`; рисует/обрабатывает custom controls в Effect Controls и/или Composition/Layer panels. Drawbot — рекомендуемый host drawing layer.

### Arbitrary parameter effect
Хранит свой data type внутри parameter stream и реализует copy/flatten/compare/interpolate/print callbacks.

### Audio effect
Effect API, но render contract оперирует `PF_SoundWorld`/samples вместо image world.

## AEGP family

### General tool
Меню, команды, проект, composition, items, layers, streams, masks, text, effects, render queue, preferences.

### Keyframer
Пакетно читает/создаёт/изменяет keyframes. Обычно виден в Animation > Keyframe Assistant.

### Native panel
Dockable panel, построенная через native panel APIs. Рабочий путь, но значительно тяжелее HTML panel.

### Suite provider
Публикует собственный PICA suite, чтобы другие native plug-ins вызывали стабильный C ABI без прямого линкования.

### File/project importer helper
AEGP может регистрироваться с File Import Manager Suite для специализированного import workflow.

## Specialized AEGP

### AEIO
Регистрирует `AEIO_ModuleInfo` и `AEIO_FunctionBlock*`; получает import/export callbacks.

### Artisan
Регистрирует `PR_ArtisanEntryPoints`; получает render context и берёт на себя 3D render композиции.

### Interactive Artisan
Вариант Artisan для интерактивного preview/render.

## Display / output hooks

### BlitHook
AE пушит отображаемые frames в plug-in. Подходит для внешнего display/monitor-like поведения. Не превращать его в скрытый render engine.

## Legacy native APIs

- Photoshop format plug-ins/filters — поддерживаются исторически, но не являются рекомендуемым путём нового AE integration.
- Foreign Project Format (FPF) — deprecated в пользу более современных integration APIs.
- ADM-based palette UI — исторический путь; не стартовать новый UI на ADM.

## Почему эта taxonomy важна

Если продукт одновременно делает несколько вещей, он может состоять из **нескольких модулей**:

```text
[CEP/UXP panel]
      |
      v
[ExtendScript / command bridge]
      |
      v
[AE project model]

[Native AEGP service] <----PICA----> [Effect plug-in]
        |
        +---- AEGP suites ----> project/layers/keyframes

[Effect plug-in] <---- PF selectors ---- [AE render graph]
```

Не надо пытаться заставить один Effect выполнять работу AEGP или наоборот.
