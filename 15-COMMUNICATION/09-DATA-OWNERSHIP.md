# Data ownership and lifetime

Большая часть тяжёлых AE plug-in bugs — не «неправильная формула», а неправильный lifetime.

## Rules

1. Opaque AE handles не считать вечными.
2. После structural project mutation заново получать references, которые API считает invalidated.
3. `PF_InData`, params, worlds и selector-specific `extra` — callback-scoped, если docs не обещают больше.
4. Передавать через module boundary POD/versioned messages, а не pointers на temporary C++ objects.
5. Большой buffer — owner должен быть указан в protocol.
6. Любой acquire должен иметь парный release; checkout — checkin; lock — unlock.
7. Render cache dependency должна быть видна AE, а не прятаться в global singleton.

## Recommended message header

```cpp
struct MsgHeader {
    uint32_t size;
    uint32_t version;
    uint32_t opcode;
    uint32_t flags;
    uint64_t request_id;
};
```

Сначала валидировать `size/version`, затем читать payload.
