# Lifetime + threading rules

Это cross-cutting chapter для всего native cookbook.

Главная мысль:

> **lifetime, ownership, validity и thread permission — четыре разных свойства.**

Handle может быть owned, но уже invalid. Pointer может быть valid, но borrowed. Product-owned buffer может жить долго, но host API рядом с ним всё равно может быть main-thread-only.

## 1. Classify every resource

Перед использованием native resource определите:

| Dimension | Questions |
|---|---|
| ownership | borrowed / caller-owned / host-owned / adopted? |
| cleanup | dispose / free / checkin / release / end? |
| lifetime | callback / transaction / frame / instance / module? |
| invalidation | что делает ref stale? |
| threading | где разрешено читать/менять? |
| persistence | можно ли хранить через project reload? |

Нельзя заменить эту таблицу правилом «все handles надо dispose».

## 2. Borrowed vs owned

Типичные категории в AE API:

- borrowed host handle/ref;
- caller-owned AEGP ref;
- Memory Suite handle;
- checked-out receipt;
- lock/unlock view;
- begin/end transaction cookie;
- adopted resource;
- platform view/container.

Каждая категория имеет свою paired operation.

Примеры:

```text
StreamRefH      → DisposeStream
EffectRefH      → DisposeEffect
MemHandle       → Lock/Unlock + FreeMemHandle
FrameReceiptH   → CheckinFrame
PICA suite      → ReleaseSuite
Undo group      → EndUndoGroup
Keyframe batch  → EndAddKeyframes
```

Не делайте один generic DisposeAnything(void*).

## 3. Acquisition success creates an obligation

```text
acquire/create/checkout succeeds
→ cleanup obligation exists
→ later operation fails
→ cleanup still required
```

Общий err не должен быть единственным признаком того, надо ли чистить ресурс. Храните ownership state отдельно.

## 4. Cleanup after failure

Плохой pattern:

```text
AcquireThing
→ UseThing fails
→ normal cleanup skipped because global err already nonzero
```

Лучше:

```text
acquire succeeds
→ mark owned
→ operation may fail
→ cleanup runs independently
→ preserve primary error
→ record cleanup error separately
```

Это особенно важно для checkin, suite release, memory unlock/free, render receipt и begin/end transactions.

## 5. First-error preservation

Если основная операция и cleanup обе дают error, обычно primary error остаётся главным результатом, а cleanup failure логируется как secondary context.

Не затирайте root cause случайно.

## 6. Structural invalidation

Structural mutation может сделать refs/indices stale, даже если pointer value всё ещё ненулевой.

Особенно опасны:

- Dynamic Stream hierarchy;
- Render Queue item order;
- Output Module order;
- effect delete/reorder;
- layer delete/reorder;
- project/item graph mutation;
- selection/view lifecycle.

После structural mutation:

```text
drop old transient refs
→ re-query target
→ validate identity
→ continue
```

## 7. Stable identity is contextual

Stable ID лучше transient ref, но не обещайте вечную стабильность.

Записывайте scope гарантии: within comp, within project session, across save/reopen, across import/merge, after duplication.

Если docs этого не обещают, Bible не должна изобретать guarantee.

## 8. Index is not identity

Layer index, RQ index и stream child index — ordering.

После insert/delete/reorder/duplicate тот же index может означать другой объект.

Если command зависит от identity, храните ID/match-name/product model и re-resolve.

## 9. Begin/end transactions

Примеры:

- StartUndoGroup / EndUndoGroup;
- StartAddKeyframes / EndAddKeyframes;
- render Checkout / Checkin;
- memory Lock / Unlock.

Каждая started transaction должна иметь defined close path на success и error.

## 10. RAII is useful but not magic

RAII хорошо решает early return, exception cleanup, unique ownership и move transfer.

RAII не решает:

- borrowed-vs-owned mistake;
- wrong cleanup function;
- host ref invalidated before destructor;
- cleanup after suite teardown;
- thread-affinity violation;
- host mutation rollback.

Сначала понять contract, потом оборачивать RAII.

## 11. Suite lifetime must outlive resource owner

Если owner destructor использует suite pointer:

```text
suite acquired/available
→ resource owner created
→ owner reset/destroyed
→ suite released
→ host teardown
```

Нельзя оставлять process-global owner, чей destructor вызовет уже мёртвую function table после teardown.

## 12. Memory handle has two lifetimes

Для AEGP_MemHandle:

```text
handle allocation lifetime
    └─ lock lifetime
         └─ temporary raw pointer
```

Raw pointer valid только в lock lifetime.

Не хранить raw pointer после unlock, не отдавать его worker с последующим unlock в другом scope, не free-ить handle while pointer retained.

Если данные нужны позже — copy into product-owned memory.

## 13. Borrowed world / receipt relationship

```text
receipt
→ borrowed world
→ borrowed base address
→ CheckinFrame
→ world/base address no longer usable by product
```

Если worker нужен после checkin — копировать bytes до checkin.

## 14. Adoption changes ownership

Некоторые APIs меняют owner после successful adoption.

```text
product creates resource
→ product owns
→ adoption succeeds
→ host owns
→ product must not dispose as pre-adoption owner
```

Failure path может оставлять ownership у caller. Это ownership state transition, которую helper должен выражать явно.

## 15. Thread permission is separate from ownership

Owned object не означает «можно использовать на любом thread».

Product-owned pure buffer может быть worker-safe, если ваш код это гарантирует. Host ref legality зависит от конкретного API/callback contract.

Suite availability тоже не делает suite methods thread-safe.

## 16. Main-thread project mutation

Project/UI mutations не должны выполняться из MFR worker, arbitrary std::thread, background helper callback или effect render callback, если exact host contract этого не разрешает.

Safe architecture:

```text
worker:
    pure compute / parse / network / file IO

host-safe callback:
    re-resolve current refs
    validate state
    mutate project
```

## 17. UI/project state vs render state

Render result не должен зависеть от hidden AEGP query, который host dependency/cache model не видит.

Если render зависит от state, state должен быть представлен в effect dependency/persistent contract или architecture должна быть переработана.

## 18. AEGP from Effect render

То, что Effect технически может получить некоторые AEGP suites, не делает arbitrary project queries безопасной render dependency.

Rule:

```text
render depends on external project fact?
→ make dependency visible/declared
→ or redesign
```

## 19. Do not hold product mutex across host call

Плохой scenario:

```text
lock product mutex
→ call AE
→ AE re-enters product callback
→ callback waits same mutex
→ deadlock
```

Safer:

```text
lock
→ copy minimal product state
→ unlock
→ host call
→ lock again only to merge result
```

## 20. MFR and shared state

For MFR classify state as immutable shared, per-instance read-only, per-frame, thread-local or synchronized shared cache.

Плохая модель: one mutable scratch buffer per effect instance shared by concurrent frames.

Global mutex может убрать race и одновременно уничтожить MFR scaling.

## 21. Async request lifetime

Async request needs request ID, request state, cancellation state, refcon lifetime, result ownership and shutdown policy.

Не уничтожайте refcon сразу после cancel, если callback/lifetime contract не обещает этого.

Не предполагайте callback during host shutdown без explicit guarantee.

## 22. Panel/helper generation

Panel async result can become stale.

```text
request generation 10 starts
→ project changes
→ generation 11 starts
→ response 10 arrives
→ discard
```

Это application-level lifetime/invalidation, а не только native handle issue.

## 23. Plugin unload

Shutdown order:

1. stop accepting new product work;
2. invalidate future callbacks/requests;
3. signal workers/helpers;
4. drain/drop according to bounded policy;
5. destroy product resource owners;
6. release suites/services;
7. return from host shutdown.

Не рассчитывайте на C++ static destructors после host teardown.

## 24. External helper/process

Helper process добавляет новый lifetime domain.

Define who launches, who owns process, reconnect/restart policy, protocol version, stale requests, shutdown and temp/shared-memory cleanup.

## 25. Failure matrix

| Phase | Failure question |
|---|---|
| acquire | что если ресурс не создан? |
| use | что если host state changed? |
| transfer | кто owner после success/fail? |
| cleanup | может ли cleanup fail? |
| shutdown | suite/host ещё valid? |
| async | callback ещё может прийти? |

## 26. Long-lived product model

Хорошо хранить:

- your own immutable IDs;
- config values;
- serialized product state;
- copied strings/data.

Плохо хранить без documented guarantee:

- StreamRefH;
- EffectRefH;
- RQItemRefH;
- OutputModuleRefH;
- borrowed WorldH;
- locked-memory raw pointer;
- platform view pointer after view destruction.

## 27. Product workflow

Before using any new API:

1. identify returned resource type;
2. identify exact owner;
3. identify cleanup pair;
4. identify invalidation triggers;
5. identify thread permission;
6. identify transfer/adoption semantics;
7. identify shutdown order;
8. only then write helper/RAII wrapper.

## 28. Related chapters

- [Memory / Undo / Persistent Data](12-MEMORY-UNDO-PERSISTENCE.md)
- [Memory/threading/errors](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md)
- [RAII ownership](../19-NATIVE-CODE-FOUNDATION/02-RAII-OWNERSHIP.md)
- [Undo transactions](../19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md)
- [Host callback boundary](../19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md)
- [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md)

## Evidence boundary

These rules combine exact cleanup/invalidation contracts from source-reviewed API families with conservative architecture guidance.

When Bible says runtime-not-claimed, it means the source/API pattern is documented without asserting a particular host-observed product result.
