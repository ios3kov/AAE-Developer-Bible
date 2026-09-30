# Memory, threading, errors

## Memory

After Effects SDK часто предоставляет host allocators/handles и буферы со своим lifetime. Главные правила:

- освобождать тем API, которым выделили;
- не считать pixel rows tightly packed;
- проверять `rowbytes`;
- не писать за extent/output bounds;
- учитывать 8/16/32-bpc layouts;
- не хранить frame-local buffer pointer после callback;
- избегать per-pixel heap allocations.

## Threading

MFR означает, что разные frames одного и того же эффекта могут одновременно заходить в render code.

Thread-safe означает:
- mutable globals отсутствуют или синхронизированы;
- render не пишет в обычный `global_data`;
- `sequence_data` не мутируется в запрещённых фазах;
- caches либо immutable, либо имеют безопасную concurrency model;
- third-party libraries тоже thread-safe в выбранном режиме.

### Deadlock rule

**Не держать blocking lock, когда вызывается host callback/suite/checkout.** Host может реэнтерабельно вызвать код или ждать другой render path.

## Errors

Внутренний код может использовать `Result<T>`/exceptions — но на границе SDK:

```cpp
extern "C" PF_Err EffectMain(...) {
    try {
        return Dispatch(...);
    } catch (const std::bad_alloc&) {
        return PF_Err_OUT_OF_MEMORY;
    } catch (...) {
        return PF_Err_INTERNAL_STRUCT_DAMAGED; // choose the real appropriate error in your codebase
    }
}
```

Конкретный error code должен соответствовать реальной причине; пример выше — только архитектурный паттерн.

## Logging

Production logging должен быть:
- bounded;
- async/non-blocking where possible;
- без secrets/license tokens;
- с version/build/architecture/GPU backend;
- с crash correlation id.

Debug logging может включать:
- `PF_Cmd`;
- thread id;
- frame/time;
- render backend;
- input/output dimensions;
- cache hit/miss.
