# Anatomy of an Effect plug-in

## Entry point

Host вызывает одну export-функцию, заданную PiPL. Точный signature берётся из SDK headers/sample вашей версии.

Архитектурно dispatch выглядит так:

```cpp
PF_Err EffectMain(PF_Cmd cmd, ...) {
    try {
        switch (cmd) {
            case PF_Cmd_GLOBAL_SETUP:   return GlobalSetup(...);
            case PF_Cmd_PARAMS_SETUP:   return ParamsSetup(...);
            case PF_Cmd_RENDER:         return Render(...);
            // SmartFX/event/sequence selectors as required
            default:                    return PF_Err_NONE;
        }
    } catch (...) {
        return MapExceptionToPfErr();
    }
}
```

Не копировать signature из этого файла — использовать текущий SDK sample.

## Global setup

Здесь заявляются capabilities/outflags и создаётся только тот global state, который действительно нужен.

Global state должен быть:
- immutable после setup, либо concurrency-safe;
- не зависеть от конкретного effect instance;
- корректно освобождаться в global setdown.

## Params setup

Параметры — часть project compatibility contract. Изменение parameter index/order после релиза может ломать старые проекты.

Для released plug-in:
- параметрам давать стабильные IDs;
- не переиспользовать старый ID для нового смысла;
- migration старых sequence/project data тестировать отдельными fixtures.

## Sequence data

Использовать для per-instance state, но проектировать serialization/flattening заранее, если state должен переживать save/load/copy.

Render path не должен «тихо» мутировать state так, что два concurrent frames видят гонку.

## Frame data

Frame-local scratch лучше frame-local и оставлять. Не превращать его в global cache ради «оптимизации» без lifetime design.

## Output correctness

Каждый render path должен учитывать:
- actual input/output dimensions;
- rowbytes;
- extent/ROI;
- alpha semantics;
- pixel depth;
- premultiplication assumptions;
- pixel aspect/time information, если алгоритм от них зависит.
