# Undo groups and transaction boundaries

AEGP undo grouping gives the user one coherent undo operation for a set of host mutations.

It is not a database transaction and does not automatically roll back a half-completed command after an error.

The foundation helper is code/UndoScope.h.

## AegpUndoScope behavior

Constructor:

~~~text
suite present
→ AEGP_StartUndoGroup(name)
→ remember start error
→ active only on A_Err_NONE
~~~

Destructor:

~~~text
active
→ AEGP_EndUndoGroup()
~~~

If start fails, destructor does not call EndUndoGroup.

The test verifies both successful and failed-start paths.

## Command boundary

Good structure:

~~~text
validate all possible prerequisites
→ create UndoScope
→ check start_error
→ perform short user mutation
→ scope ends
→ return result
~~~

Validation before the first mutation reduces partial project edits.

## Undo is not rollback

Suppose:

~~~text
rename layer
→ create effect
→ third operation fails
~~~

Ending the undo group does not mean the first two operations were automatically reverted before the function returns.

If the product requires all-or-nothing semantics:

1. prevalidate;
2. stage pure/external work first;
3. perform mutations in a deliberate order;
4. explicitly clean product-created temporary state where safe;
5. document the remaining failure semantics.

Do not claim transactionality merely because StartUndoGroup/EndUndoGroup were balanced.

## Scope size

Keep undo scope around the host mutation, not around unrelated long work.

Bad:

~~~text
StartUndoGroup
→ network request
→ worker compute
→ wait for user
→ event loop
→ project mutation
→ EndUndoGroup
~~~

Better:

~~~text
external/pure work
→ validate result
→ short undo-scoped host mutation
~~~

## Nested ownership

Pick one layer that owns the user command undo group.

Low-level helpers should normally not each start their own group unless nested behavior is explicitly intended and tested.

A command should appear in Undo history at the level meaningful to the artist.

## Failure to start

AegpUndoScope exposes start_error and active.

Caller must check start_error when an undo group is required for the operation.

Do not silently continue a multi-step destructive mutation after undo-group start failed unless product policy explicitly allows it.

## End error limitation

Current destructor discards the return value from AEGP_EndUndoGroup.

This is a normal destructor-safety tradeoff but means the helper cannot report an end failure as a command result.

If the target workflow requires evidence of successful EndUndoGroup, provide an explicit close method that returns A_Err, then leave the destructor as best-effort fallback.

## Thread/lifecycle

Undo groups belong to host project mutation workflows. Do not carry an active scope into render workers/background work.

Use AEGP mutation APIs only on their documented thread/lifecycle path.

## Tests

Current tests prove:

- successful start marks active;
- successful active scope ends once;
- failed start is recorded;
- failed start does not call end;
- null suite produces inactive scope.

Product host tests still need to verify:

- actual Undo menu behavior;
- multiple host mutations appear as intended;
- command failure behavior;
- project state after undo/redo;
- nested command policy if used.

## Acceptance rule

A user-facing multi-step command is not accepted until:

- prerequisites are validated;
- undo start failure is handled;
- one meaningful undo entry is observed when expected;
- undo/redo restores expected project state;
- partial-failure behavior is documented/tested.
