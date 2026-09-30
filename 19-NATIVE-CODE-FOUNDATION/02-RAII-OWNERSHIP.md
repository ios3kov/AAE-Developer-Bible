# AEGP ownership / RAII

Главная причина утечек в AEGP — не C++ heap, а host-owned handles/refs с отдельными dispose/checkin вызовами.

## Типичные пары

- `GetNew...Stream` → `AEGP_DisposeStream`;
- effect ref, который API требует dispose → `AEGP_DisposeEffect`;
- `RenderAndCheckoutFrame` receipt → `AEGP_CheckinFrame`;
- `AEGP_MemHandle` → `AEGP_FreeMemHandle`.

`code/AegpOwners.h` содержит move-only owners для этих четырёх случаев. Это уменьшает количество early-return leaks.

Не оборачивать borrowed handle в owner. Перед созданием owner всегда проверить ownership contract конкретной функции.
