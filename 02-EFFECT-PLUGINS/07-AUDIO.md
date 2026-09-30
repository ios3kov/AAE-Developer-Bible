# Audio effects

After Effects SDK имеет отдельные audio selectors/data structures. Audio path нельзя проектировать как «те же pixels, только samples».

## Checklist

- sample rate/channel assumptions;
- buffer length and requested range;
- float/range semantics;
- latency/stateful processing;
- random access / non-linear timeline requests;
- thread safety;
- silence/empty input;
- project sample-rate changes;
- determinism after seeks.

Если алгоритм имеет history (filter/delay), нельзя полагаться на то, что host будет вызывать samples строго последовательно от начала к концу.
