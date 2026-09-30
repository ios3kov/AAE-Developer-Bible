# Memory / Undo / Persistent Data

## Undo

**Suite:** `AEGP_UtilitySuite6`

Каждая пользовательская mutation-команда должна выглядеть как одна операция:

```cpp
class ScopedUndo {
public:
    ScopedUndo(AEGP_SuiteHandler& s, const char* name)
        : suites_(s), active_(false)
    {
        if (suites_.UtilitySuite6()->AEGP_StartUndoGroup(name) == A_Err_NONE) {
            active_ = true;
        }
    }

    ~ScopedUndo() {
        if (active_) {
            suites_.UtilitySuite6()->AEGP_EndUndoGroup();
        }
    }

    ScopedUndo(const ScopedUndo&) = delete;
    ScopedUndo& operator=(const ScopedUndo&) = delete;

private:
    AEGP_SuiteHandler& suites_;
    bool active_;
};
```

В реальном codebase лучше сохранить ошибку EndUndoGroup через явный `Close()`; destructor не должен бросать exception.

---

## Host memory

**Suite:** `AEGP_MemorySuite1`

Если suite возвращает `AEGP_MemHandle`:

```text
lock
→ use pointer briefly
→ unlock
→ FreeMemHandle
```

Не:
- `free()`;
- `delete`;
- сохранять locked pointer;
- передавать pointer в другой thread после unlock.

---

## Native allocations

Ваш `new/delete`, `std::vector` и т.д. допустимы внутри вашего модуля, но не передавайте STL object через plug-in ABI/PICA generic bridge. Межмодульный ABI: POD + explicit ownership callbacks.

---

## Persistent Data

**Suite:** `AEGP_PersistentDataSuite4`

Подходит для:
- preferences;
- feature flags;
- last-used settings;
- migration version.

Не подходит для:
- pointer;
- host handle;
- live layer/effect/stream ref;
- секреты в plaintext без threat model.

Ключи должны быть namespaced вашим vendor/product ID.

---

## Error reporting

Для AEGP пользовательское сообщение — через host Utility/Report API. Не показывать native modal alert из render thread.

Ошибки внутри core лучше представлять:

```cpp
struct Error {
    int32_t domain;
    int32_t code;
    char message[256];
};
```

и конвертировать в AE-facing `A_Err` только на boundary.
