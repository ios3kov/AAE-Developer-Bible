# Expressions vs scripts

**Script** говорит After Effects выполнить действия над проектом.  
**Expression** вычисляет значение property во время evaluation.

Не использовать expression как замену batch automation и не использовать script как per-frame expression engine.

## Expression constraints

- может вычисляться очень часто;
- должна быть максимально pure/deterministic;
- expensive project traversal быстро становится bottleneck;
- side effects — неправильная модель.

## Script constraints

- запускается как операция/tool;
- может создавать/менять project structure;
- не является частью render callback для каждого pixel/frame.
