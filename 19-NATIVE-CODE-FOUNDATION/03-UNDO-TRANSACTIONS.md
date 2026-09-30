# Undo transaction

Любая пользовательская операция, меняющая project state несколькими вызовами, должна выглядеть как одна понятная undo operation, если host API для этих изменений undoable.

`UndoScope`:

- открывает undo group;
- закрывает только если start прошёл успешно;
- не бросает exceptions;
- не скрывает ошибку business operation.

Не растягивать undo scope на background/render работу и не держать его открытым через event loop.
