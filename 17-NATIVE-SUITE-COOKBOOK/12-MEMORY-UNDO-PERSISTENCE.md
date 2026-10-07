# Memory / Undo / Persistent Data

These three topics look unrelated, but they meet at one architectural rule:

> **state must have explicit owner, lifetime and failure semantics.**

## State classification table

Перед хранением любого state определите его класс:

| State | Typical owner | Lifetime | Persistence |
|---|---|---|---|
| project/render truth | After Effects project/effect model | project/instance | project-visible |
| user preference | product/user | across sessions | PersistentData/config |
| runtime cache | product | process/instance | rebuildable |
| host ref/handle | host/product per API | API-defined | usually not serializable |
| request state | product | request/generation | ephemeral |
| secret credential | product/platform secure store | product policy | security-specific |

Главное правило: **не переносите state в PersistentData только потому, что его удобно хранить там**.

Render-affecting state, который должен путешествовать с project, требует project/effect persistence strategy, а не hidden user preference.

## Undo

**Suite:** `AEGP_UtilitySuite6`.

For user-visible project mutation, group semantic operation into one undo group where appropriate.

Conceptual RAII shape:

```cpp
class ScopedUndo {
public:
    ScopedUndo(AEGP_UtilitySuite6* suite, const char* name);
    A_Err Close();
    ~ScopedUndo() noexcept;
};
```

Destructor should not throw. If `EndUndoGroup` error matters, expose explicit `Close()` and preserve its result.

## Undo is not transaction rollback

Important:

```text
StartUndoGroup
→ mutation A succeeds
→ mutation B succeeds
→ mutation C fails
→ EndUndoGroup
```

does not mean A/B were automatically rolled back at the moment C failed.

Product must decide partial-failure policy.

## Validate before mutate

Reduce partial changes:

1. resolve all targets;
2. validate legality/capabilities;
3. compute pure plan;
4. open undo;
5. mutate.

Do not discover obvious invalid input halfway through destructive batch.

## Nested undo

Do not assume your tool owns global undo context.

Keep groups at semantic command boundary and avoid opening/closing groups in low-level helper functions that can be composed unpredictably.

## Host memory handles

**Suite:** `AEGP_MemorySuite1`.

Common pattern:

```text
receive AEGP_MemHandle
→ lock
→ use/copy pointer briefly
→ unlock
→ FreeMemHandle
```

Never:

- `free()`;
- `delete`;
- keep pointer after unlock;
- move locked pointer to worker after unlock;
- double-free handle.

## Copy before async work

If worker needs returned string/data:

```text
lock host memory
→ copy into std::string/vector/owned buffer
→ unlock
→ free host handle
→ worker uses owned copy
```

Host handle and copied data have separate ownership.

## Host refs vs memory handles

Do not create one generic `DisposeAnything()` abstraction.

Examples of different cleanup families:

- `AEGP_MemHandle` → Memory Suite;
- StreamRefH → Stream Suite;
- EffectRefH → Effect Suite;
- FrameReceiptH → Render Suite checkin;
- FootageH → Footage adoption/dispose rules;
- MaskRefH → Mask Suite;
- PICA suite → ReleaseSuite.

Type determines cleanup contract.

## Ownership transfer and adoption

Некоторые host APIs меняют владельца после successful call.

Model:

~~~text
caller owns resource
→ adoption/attach call
→ success: host owns
→ failure: caller may still own
~~~

RAII wrapper в таком месте должен уметь **явно release ownership** только после успешной передачи.

Не вызывайте cleanup дважды после adoption и не теряйте cleanup на failure branch.

Примеры такого reasoning встречаются в footage/import и других create→adopt workflows.

## Product-native allocations

`new/delete`, `std::vector`, smart pointers etc. are fine inside your module.

But do not expose C++ standard-library objects across long-lived module ABI unless both sides deliberately share exact toolchain/runtime/allocator contract.

Prefer C-shaped/versioned POD interface for independently versioned components.

## Persistent Data

**Suite:** `AEGP_PersistentDataSuite4`.

Useful for:

- preferences;
- last-used settings;
- feature toggles;
- migration version;
- small product configuration.

Not appropriate for:

- raw pointers;
- host handles;
- live layer/effect/stream refs;
- frame receipt/world;
- secrets without threat model;
- huge cache blobs that can be rebuilt.

## Namespace keys

Use vendor/product namespace.

Bad:

```text
lastPath
version
enabled
```

Better conceptual namespace:

```text
com.vendor.product/settings/schema
com.vendor.product/ui/lastPath
```

Avoid collision with other components/products.

## Persistent schema version

Version your own stored data.

```text
schema version
→ parse known version
→ migrate
→ write current version
```

Do not reinterpret old bytes/string format as new struct without migration.

## Persistent migration failure

Migration — это тоже failure boundary.

Планируйте:

- unknown future schema;
- malformed value;
- partially written value;
- old key missing;
- migration step failed;
- downgrade to older product version.

Safe policy:

~~~text
read version
→ validate representation
→ migrate known versions
→ on unknown/corrupt: use explicit recovery/default policy
→ write new version only after successful migration
~~~

Не затирайте старые данные новым schema marker до успешного преобразования.

## Project state vs preferences

Do not store project-essential render state only in global preferences.

Ask:

- should this travel with project?
- should it be per-user?
- can it be regenerated?
- does it affect render output?

Render-affecting state needs a host/project-visible persistence/dependency strategy, not a hidden preference.

## Secrets

PersistentData is not automatically secure secret storage.

License token/credential design needs a separate threat model and platform storage strategy.

Do not document plaintext preference storage as secure merely because API persists it.

## Quiet errors

Utility quiet-error APIs can suppress/report UI noise for expected operations, but they do not make failed host calls successful.

Always inspect returned `A_Err`.

Suppressed error UI and operation result are separate concerns.

## Error reporting

Inside product core use structured errors:

```text
domain
code
context
message
cause
```

At AE boundary convert to `A_Err` and optionally report user-facing context through supported host/UI layer.

## Cleanup error policy

Разделяйте два класса cleanup:

### Best-effort destructor cleanup

Подходит, когда:

- ошибка cleanup уже не может быть полезно обработана;
- destructor обязан быть noexcept;
- ресурс всё равно должен быть освобождён насколько возможно.

### Observable close/checkin

Нужен, когда cleanup result влияет на correctness/diagnostics.

Pattern:

~~~text
owner.Close()
→ returns host error
→ caller records/propagates result
→ destructor becomes fallback only
~~~

Это особенно важно для frame checkin, transaction end и других cleanup calls, где silent failure может скрыть проблему.

## First-error preservation

Pattern:

```text
operation fails
→ cleanup also fails
```

Usually preserve primary operation failure as main result and record cleanup error separately.

Do not lose root cause because destructor cleanup returned another code.

## C++ exception boundary

Never let exception escape `extern "C"` / host callback.

Use boundary guard:

```text
try implementation
catch known error
catch std::exception
catch ...
→ A_Err
```

## Persistent data is not a synchronization primitive

То, что state записан через PersistentData, не делает concurrent access автоматически безопасным.

Если несколько callbacks/threads читают и меняют product state:

- определите собственную synchronization policy;
- не используйте preference store как lock;
- не делайте high-frequency render coordination через persistent settings.

PersistentData решает хранение, не concurrency.

## Threading

Memory ownership does not imply thread permission.

A product-owned buffer may be thread-safe to move to worker; a host ref/handle may not be legal to use there.

Separate:

- lifetime;
- ownership;
- thread-affinity.

## Shutdown ordering

Memory/undo/persistence helpers должны завершаться **до** того, как исчезнут suites/host services, которые нужны их cleanup.

Типичный порядок:

~~~text
stop new work
→ close active requests/transactions
→ destroy resource owners
→ flush product settings if policy requires
→ release suites/services
→ module teardown
~~~

Не оставляйте host-cleanup RAII objects process-global до C++ static destruction.

## Shutdown

On shutdown:

- stop new requests;
- release product-owned global state;
- drain/drop work by policy;
- avoid host calls after lifetime;
- do not rely on exceptions for cleanup.

## RAII design

Good RAII wrappers:

- are move-only for unique ownership;
- have explicit `release()` when ownership transfers;
- never throw in destructor;
- expose cleanup error when it materially matters;
- encode correct cleanup family in type.

Bad RAII wrapper:

```text
void* + one generic free callback for all AEGP resources
```

because semantic lifetime differs.

## Product workflow

Concrete composition with shipped snippets:
[`Bible_ApplyEffect`](code/EffectStreamRecipes.cpp) disposes an EffectRef after apply,
not the installed layer effect; failed disposal can follow successful mutation.
[`Bible_AddOneDKeyframes`](code/KeyframeRecipes.cpp) closes its batch on ordinary
errors, but not C++ unwind; command guard alone does not resume skipped cleanup.
[`Bible_WithRenderedWorld`](code/RenderRecipes.cpp) has a receipt owner whose suite
outlives it, but destructor checkin discards diagnostics. UndoGroup in
[`BibleAegpCommon.h`](code/BibleAegpCommon.h) is balance-only and exposes neither
Start nor End errors. These are source limits, not an implemented transaction layer.
Before composing them, supply observable Undo start/end, primary/secondary errors
and compensation only for the command's permitted project changes.

1. Classify state.
2. Define owner.
3. Define cleanup pair.
4. Define thread use.
5. Define persistence/reload behavior.
6. Define partial failure.
7. Add RAII only after contract is understood.

## Related chapters

- [Memory/threading/errors](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md)
- [Undo transactions](../19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md)
- [RAII ownership](../19-NATIVE-CODE-FOUNDATION/02-RAII-OWNERSHIP.md)
- [Host call boundary](../19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md)

## Evidence boundary

Suite families/ownership patterns are source-reviewed. Security/persistence architecture recommendations are product guidance unless tied to a specific host contract.
