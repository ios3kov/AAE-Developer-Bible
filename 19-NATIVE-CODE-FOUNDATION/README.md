# Native C++ foundation — reusable safety layer

This directory is not another sample plug-in. It contains small C++ helpers for recurring native After Effects failure classes:

- PICA suite acquire/release;
- AEGP resource ownership;
- undo-group balancing;
- C++ exception containment at host callback boundaries.

Use these helpers by grafting them into the closest official Adobe sample and adapting suite generations to the exact target SDK.

## What is included

### code/PicaSuiteRef.h

Move-only owner for one SPBasicSuite AcquireSuite / ReleaseSuite pair.

It stores:

- SPBasicSuite pointer;
- suite name pointer;
- public suite version;
- acquired function-table pointer.

### code/AegpOwners.h

Four explicit move-only owners:

- AegpStreamRefOwner;
- AegpEffectRefOwner;
- AegpFrameReceiptOwner;
- AegpMemHandleOwner.

They intentionally stay separate because each AE resource has a different release API.

### code/UndoScope.h

AegpUndoScope starts an AEGP undo group, records start failure and ends the group only if start succeeded.

### code/HostCallbackGuard.h

GuardAeHostCallback converts C++ exceptions into an A_Err chosen by the caller so exceptions cannot escape through the AE C ABI.

## Design principles

~~~text
exact host ownership contract
→ one narrow helper
→ move-only lifetime
→ no hidden host acquisition
→ no exception from cleanup
~~~

The helpers do not attempt to build a universal AE abstraction layer.

## Host lifetime remains above RAII lifetime

RAII is safe only while the suite/function table used by the destructor is still valid.

Bad:

~~~text
process-global static owner
→ AE tears down suites
→ C++ static destructor runs later
→ destructor calls dead host function table
~~~

Good:

~~~text
host initialization
→ acquire/create resource
→ owner lives inside product lifecycle
→ owner destroyed/reset
→ release suites/host
→ module teardown
~~~

Long-lived product state must be explicitly drained before host teardown.

## Borrowed vs owned

Never wrap a borrowed handle in one of these owners.

Before constructing an owner, answer:

1. did this API transfer ownership?;
2. what exact matching release/checkin call is required?;
3. on which thread/lifecycle is release legal?;
4. can the handle be invalidated earlier by host mutation?;
5. can cleanup fail meaningfully?

RAII cannot repair a wrong ownership assumption.

## Cleanup errors

Current helpers intentionally discard errors returned by cleanup functions inside destructors/reset paths.

That avoids throwing from destructors, but it means these helpers are inappropriate when release failure itself must become explicit acceptance evidence.

For such a path, add an explicit close/checkin method that returns the host error before destruction.

## Suite-generation boundary

The current code names concrete suite generations from the supplied SDK baseline, for example StreamSuite6 and EffectSuite4.

Do not copy those generation numbers into a different SDK blindly.

The target SDK headers remain the compile-time source of truth.

## Test coverage

tests/test_foundation.cpp currently checks:

- PICA acquire success/failure;
- single matching release after moves/reset;
- move-only AEGP owners;
- release transfer;
- four AEGP cleanup paths through stubs;
- successful/failed/null undo start;
- no EndUndoGroup after failed start;
- standard exception → fallback A_Err;
- thrown A_Err preservation;
- zero thrown A_Err → fallback;
- normal callback result passthrough.

These are pure foundation tests with stubs. They do not prove real AE host lifetime, suite generation compatibility or thread legality.

## Production checklist

Before using this layer in a product:

- [ ] exact SDK suite generations checked;
- [ ] every wrapped resource confirmed owned, not borrowed;
- [ ] suite owners destroyed before host teardown;
- [ ] suite-name lifetime is stable;
- [ ] release errors reviewed for whether silent cleanup is acceptable;
- [ ] callback fallback errors chosen deliberately;
- [ ] product logging wraps failures without throwing;
- [ ] real host integration test exists for each used resource family.

## Verification boundary

The foundation tests prove local move/cleanup mechanics against stubs. Host correctness still requires compile/link plus After Effects execution on the declared platform matrix.
