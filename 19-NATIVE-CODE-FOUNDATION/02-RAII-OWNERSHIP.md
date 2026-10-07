# AEGP ownership / RAII

The main native leak class is often not ordinary C++ heap memory. It is a host resource that requires a specific dispose, free or checkin call.

code/AegpOwners.h contains narrow move-only owners for four contracts from the current Bible baseline.

## Included owners

| Owner | Stored resource | Cleanup |
|---|---|---|
| AegpStreamRefOwner | AEGP_StreamRefH | AEGP_DisposeStream |
| AegpEffectRefOwner | AEGP_EffectRefH | AEGP_DisposeEffect |
| AegpFrameReceiptOwner | AEGP_FrameReceiptH | AEGP_CheckinFrame |
| AegpMemHandleOwner | AEGP_MemHandle | AEGP_FreeMemHandle |

Each owner also stores the suite function table required for cleanup.

## Why separate classes

A generic void-pointer owner hides the most important information: which host contract releases the resource.

Explicit owners make the pair visible in code review.

~~~text
resource type
↔ exact cleanup function
~~~

## Construction rule

Construct an owner only after an API has successfully returned an owned resource.

Conceptual:

~~~cpp
AEGP_StreamRefH raw = nullptr;
A_Err err = /* host call creating owned stream ref */;

if (!err && raw) {
    AegpStreamRefOwner owner(stream_suite, raw);
    // use owner.get()
}
~~~

Do not create an owner for a borrowed handle simply because its type matches.

## Move-only semantics

Copy is disabled.

Move transfers the raw host handle so there remains exactly one cleanup owner.

~~~text
owner A owns H
→ move to B
→ A empty
→ B owns H
→ B destructor disposes H
~~~

This is the intended protection against double release.

## release

release returns the raw handle and makes the owner empty.

After release, responsibility moves back to the caller.

Use it only for a deliberate ownership transfer.

~~~text
owner.release()
→ caller now owns host cleanup obligation
~~~

The test explicitly releases one stream ref and manually disposes the returned raw handle to prove this transfer.

## reset

reset disposes/checks in the current handle and can optionally replace it with another raw handle while keeping the same suite pointer.

Important: a default-constructed owner has no suite pointer. Do not call reset(newHandle) on such an object and assume it can later clean that handle.

Prefer constructing with both the correct suite and owned handle.

## Suite lifetime

The stored suite pointer must remain valid until the owner has been reset/destroyed.

This creates a strict order:

~~~text
resource owners destroyed
→ acquired suites released
→ host/module teardown
~~~

Not the reverse.

## Error handling

Current reset/destructors intentionally cast cleanup return values to void.

That prevents cleanup from throwing, but it also means a failed checkin/dispose is not surfaced.

For resources whose cleanup status affects correctness, add an explicit close/checkin operation that:

1. performs cleanup;
2. returns A_Err;
3. clears ownership only according to the chosen failure policy;
4. runs before destructor fallback.

## Memory-handle locking is separate

AegpMemHandleOwner owns the handle allocation. It does not model lock/unlock of the memory contents.

Those are separate lifetimes:

~~~text
MemHandle owner
  └─ lock
      └─ temporary raw pointer
      └─ unlock
  └─ free handle
~~~

Never preserve the locked raw pointer after unlock or free.

## Frame receipt semantics

Frame receipt cleanup uses CheckinFrame. Do not treat the checked-out world/receipt as an ordinary heap object.

A borrowed frame/world pointer obtained through the receipt cannot outlive the receipt contract.

## Structural invalidation

RAII prevents forgotten cleanup. It does not guarantee a host reference remains semantically valid after project structural mutation.

Reacquire references when the relevant AEGP contract requires it.

## Tests

Current stub tests cover:

- stream owner move assignment disposes the previous destination handle;
- moved-from owner is empty;
- release transfers cleanup;
- effect ref cleanup;
- frame receipt checkin;
- memory handle free.

For a concrete product, additional runtime evidence may cover:

- host error paths;
- actual suite lifetime;
- invalidation after project mutation;
- async cancellation;
- shutdown ordering;
- leak diagnostics.

These are product-evidence concerns, not conditions for Bible editorial completion.

## Read the helpers with an actual operation

The canonical authored [render recipe](../17-NATIVE-SUITE-COOKBOOK/code/RenderRecipes.cpp)
composes the receipt owner with the callback guard:

~~~text
caller owns configured RenderOptions
→ recipe acquires RenderSuite through SuiteHandler
→ RenderAndCheckoutFrame returns receipt
→ receipt owner borrows suite table
→ GetReceiptWorld returns borrowed world
→ consume completes while receipt is alive
→ explicit CheckinFrame on the ordinary return path
→ resource owner destroyed before SuiteHandler
~~~

The consumer must not retain the world or pointers into it. The recipe does not
dispose caller-owned options, schedule asynchronous work or perform export/file
verification. On the ordinary path it returns a checkin error only when there is
no primary error. On exception unwind the owner performs fallback checkin and
discards its status. Thus **both errors are not recorded by this helper**; a
product needing that diagnostic must provide an explicit result/logging policy.

In contrast, [the keyframe recipe](../17-NATIVE-SUITE-COOKBOOK/code/KeyframeRecipes.cpp)
borrows its input stream and owns newly obtained StreamValue and batch resources.
It cleans ordinary error paths but has no callback guard or scope owners for
exception unwind. Do not infer that every cookbook recipe already composes this
foundation layer. See [callback boundary](04-HOST-CALL-BOUNDARY.md) before calling
it from an exported host callback.

## Verification boundary

RAII proves deterministic local cleanup only when the ownership assumption and suite lifetime are correct.

It does not prove that a host ref remains valid or that cleanup is legal from the current thread/context.
