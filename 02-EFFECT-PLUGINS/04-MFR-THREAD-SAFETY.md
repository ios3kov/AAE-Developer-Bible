# Multi-Frame Rendering (MFR) and thread safety

After Effects 2022+ может рендерить несколько кадров одновременно. Effect сообщает поддержку threaded rendering соответствующим SDK flag **только после того, как реализация стала thread-safe**.

## Нельзя

- mutable file-static/global variables без safe synchronization;
- писать в `global_data` во время render;
- обычным способом менять `sequence_data` во время render;
- использовать singleton third-party state, который не thread-safe;
- полагаться на «предыдущий кадр уже посчитался»;
- держать mutex во время вызова host suite/checkout.

## Можно

- immutable globals;
- per-render/per-frame scratch;
- immutable precomputed tables;
- thread-safe cache с ясным ownership;
- Compute Cache API для подходящих дорогих вычислений;
- documented mutable sequence mechanism, если действительно необходим и корректно включён.

## Migration procedure

1. Запустить current effect без MFR flag.
2. Найти все globals/statics/singletons.
3. Классифицировать: immutable / per-instance / per-frame / cache.
4. Убрать write-on-render shared state.
5. Проверить third-party libs.
6. Добавить stress harness внутри AE: несколько instances + long comp + random seeks.
7. Сравнить MFR off/on output hashes/images.
8. Thread Sanitizer там, где применим к отдельной testable core library.
9. Включить threaded-rendering flag.
10. Повторить crash/perf/correctness matrix.

## Performance trap

Thread-safe код с одним глобальным mutex технически может «работать», но уничтожит scaling. Сначала correctness, затем lock contention profiling.

## Required regression

- render same frame repeatedly;
- random frame order;
- forward/backward scrubbing;
- duplicate layer/effect;
- multiple comps rendering;
- render queue;
- project close/reopen;
- cache purge;
- MFR toggle.
