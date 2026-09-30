# AEGP hooks and suites

После entry registration AEGP взаимодействует с AE через зарегистрированные hooks и versioned suites.

## Suite discipline

Каждый suite:
- acquire требуемую version;
- проверить success;
- не использовать function pointer после release;
- иметь fallback/unsupported path, если suite отсутствует.

## Opaque handles

AEGP APIs часто возвращают opaque handles. Их lifetime может меняться после host operations.

Критический пример: операции с render queue могут invalidate ранее полученные render-queue references. Поэтому handle нельзя превращать в «вечный ID» без документации.

## Begin/end transactions

Некоторые host operations требуют start/begin → batch → end semantics. Это не cosmetic API: host таким образом сохраняет consistency/undo/state вокруг операции.

## Hooks

Hook callback должен:
- быть коротким;
- не блокировать UI без необходимости;
- не хранить transient host data;
- корректно работать при project switch/close;
- защищать границу от exceptions.
