# Native C++ foundation — повторно используемые безопасные куски

Эта папка — не ещё один sample plug-in, а маленький слой для типовых ошибок native AE разработки: suite ownership, handle cleanup, undo и exception boundary.

**Как использовать правильно:** graft этих файлов в ближайший официальный Adobe sample и заменить suite generations на те, которые реально есть в вашем target SDK.

## Файлы

- `code/PicaSuiteRef.h` — acquire/release одной PICA suite через `SPBasicSuite`.
- `code/AegpOwners.h` — move-only owners для часто возвращаемых AEGP resources.
- `code/UndoScope.h` — balanced `StartUndoGroup/EndUndoGroup` без исключений.
- `code/HostCallbackGuard.h` — не выпускает C++ exception через host callback ABI.

## Важное ограничение

RAII работает только пока соответствующая host suite жива. Не оставлять объект, который в static destructor попытается вызвать AE после shutdown. Освобождение long-lived state выполнять из normal lifecycle/death hook **до** teardown host API.
