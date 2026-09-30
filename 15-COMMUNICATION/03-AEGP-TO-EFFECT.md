# AEGP -> Effect

Есть documented direct path для согласованной пары AEGP + Effect.

## Generic call

AEGP Effect Suite предоставляет `AEGP_EffectCallGeneric()`. Подготовленный effect получает `PF_Cmd_COMPLETELY_GENERAL`; `extra` указывает на payload, который договорились понимать обе стороны.

```text
AEGP
  |
  | AEGP_EffectCallGeneric(effect_ref, payload)
  v
AE
  |
  | PF_Cmd_COMPLETELY_GENERAL
  v
EffectMain(..., extra=payload)
```

## Для чего подходит

- команда «invalidate/reload internal resource»;
- запрос/передача small control state;
- handshake между двумя модулями одного продукта;
- действия, не являющиеся скрытым render dependency.

## Для чего НЕ подходит

Не использовать generic call как обход dependency graph, чтобы render зависел от неописанного внешнего state. Это ведёт к cache invalidation bugs.

## Protocol design

Payload должен иметь explicit version + size + opcode:

```cpp
struct BridgeMessageV1 {
    uint32_t size;
    uint32_t version;
    uint32_t opcode;
    uint32_t flags;
    uint64_t request_id;
};
```

Никогда не передавать STL objects/`std::string` через module boundary как ABI contract.

См. `16-WORKING-TEMPLATES/effect-aegp-generic-bridge/`.
