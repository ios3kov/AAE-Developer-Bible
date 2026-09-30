# After Effects -> Effect

## Единственная точка входа поведения

After Effects посылает Effect selector-команды в `EffectMain`:

```cpp
PF_Err EffectMain(
    PF_Cmd cmd,
    PF_InData* in_data,
    PF_OutData* out_data,
    PF_ParamDef* params[],
    PF_LayerDef* output,
    void* extra);
```

`cmd` определяет meaning остальных arguments.

## Входящий канал

- `PF_InData` — host/time/context/callbacks/suite access.
- `PF_ParamDef[]` — текущее значение parameter streams.
- `output` — destination world, когда selector подразумевает render.
- `extra` — selector-specific payload: events, SmartFX structures, parameter supervision и т.п.

## Исходящий канал

- return `PF_Err`;
- `PF_OutData` flags/state/version/messages;
- заполненный output world;
- host callback calls / suite calls.

## Важная мысль

Effect — **reactive component**. Он не должен иметь произвольный background loop, меняющий AE. Если нужна host/project automation — вынести её в AEGP/panel/script layer.
