# Data ownership and lifetime

Обновлено **2026-10-01**. Для каждого pointer/handle/table/buffer нужен ответ: кто владеет, как долго валиден и кто освобождает.

## 1. Ownership classes

### Borrowed callback-scoped pointer

~~~text
use during allowed callback
→ do not retain after return
~~~

### Host opaque handle/reference

Не предполагать stable address, eternal lifetime, survival after structural mutation или cross-thread safety.

### Acquired suite

~~~text
AcquireSuite
→ use
→ ReleaseSuite
~~~

### Checkout/checkin resource

~~~text
checkout
→ use
→ checkin even on failure
~~~

### Product-owned allocation

Product memory не продлевает lifetime borrowed host pointer, который в неё записан.

## 2. Pair table

| Acquire/create | Release |
|---|---|
| AcquireSuite | ReleaseSuite |
| checkout | checkin |
| lock host memory | unlock |
| owned AEGP memory handle | matching free |
| product worker | explicit stop/join policy |
| IPC/file handle | close |

Если cleanup API возвращает meaningful error, не теряйте его автоматически в destructor.

## 3. Early-return safety

~~~text
acquire A
acquire B
operation fails
return
B/A leak
~~~

Нужен RAII, scope guard, single cleanup section или explicit result-preserving cleanup.

## 4. Structural invalidation

После project/property structural mutation reacquire references, которые могут быть invalidated.

Cached host ref не permanent object ID.

## 5. Generic call payload

AEGP_EffectCallGeneric передаёт void pointer синхронному effect call.

Без documented ownership transfer:

~~~text
caller owns payload
→ effect reads/writes during call
→ return
→ effect does not retain pointer
~~~

Для long-lived object передавайте stable service ID/handle, не stack pointer.

## 6. Published suite lifetime

Provider function table живёт достаточно долго для valid acquisitions. Sweetie использует static table, но это не доказательство generic hot replacement/unload protocol.

## 7. ExecuteScript memory handles

Если AEGP_ExecuteScript возвращает result/error AEGP_MemHandle:

1. check call;
2. lock/read по Memory Suite rules;
3. unlock;
4. free owned handle matching API;
5. не сохранять raw pointer после unlock/free.

## 8. Message ABI

~~~cpp
struct MsgHeader {
    uint32_t size;
    uint32_t version;
    uint32_t opcode;
    uint32_t flags;
    uint64_t request_id;
};
~~~

Validation order:

~~~text
non-null
→ minimum header
→ supported version
→ total size bounds
→ opcode
→ payload lengths/counts
→ payload access
~~~

Optional tail нельзя читать до size check.

## 9. No C++ object ABI across boundary

Не передавать как public ABI:

- std::string/std::vector;
- exceptions;
- RTTI-dependent graph;
- allocator-owned object без shared allocator contract;
- raw lambda/function object;
- platform UI object.

Cross-process raw pointer бессмысленен.

## 10. Strings

Определите encoding, length unit, null termination, allocator/free owner и embedded-zero policy.

## 11. Large buffers

Protocol должен определять:

~~~text
owner
capacity
valid bytes
mutability
alignment
lifetime
thread
release API
~~~

## 12. Persistent vs runtime

Persistent state должен иметь version/migration и выбранный persistent owner.

Runtime cache должен быть rebuildable и не быть единственным source of render-affecting truth.

## 13. Render dependency ownership

~~~text
global singleton changed
→ output depends on it
→ AE graph does not know
→ stale cached frame
~~~

Render-affecting state должен участвовать в поддержанном parameter/dependency/cache identity mechanism.

## 14. Cross-process ownership

Передавайте values, IDs, paths, offsets, lengths, protocol version. Не передавайте AE handles/C++ addresses/process-local pointers.

## 15. Shutdown order

~~~text
stop new requests
→ cancel/drain borrowers
→ release host/provider acquisitions
→ destroy transports
→ destroy backing data
→ unload code
~~~

Owner переживает borrower.

## 16. Product validation cases

- acquire failure;
- partial acquire then failure;
- early return;
- exception boundary;
- wrong message size/version;
- oversized length/count;
- stale host reference;
- structural mutation;
- provider shutdown;
- panel/helper disconnect;
- cancel during buffer use;
- AE shutdown;
- leak/double-release checks.

## Verification boundary

Это ownership model поверх public SDK contracts и product protocols. Конкретный lifetime определяется соответствующим API/header.

ASan/leak/stress/host validation относится к concrete product evidence where relevant; отсутствие такого run не делает source-level Bible guidance незавершённой.
