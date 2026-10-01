# Suite acquisition

PICA suites use a reference-counted name/version acquire/release contract.

The foundation helper is code/PicaSuiteRef.h.

## Contract

~~~text
SPBasicSuite is valid
→ AcquireSuite(name, public version)
→ check error
→ check returned pointer
→ use suite
→ ReleaseSuite(same name, same version)
~~~

A successful acquire creates a lifetime obligation.

Do not use the function-table pointer after release.

## Why wrap it

Manual code tends to leak on paths such as:

~~~text
AcquireSuite
→ second operation fails
→ early return
→ ReleaseSuite skipped
~~~

PicaSuiteRef makes the successful acquisition move-only and releases it on reset/destruction.

## Helper behavior

acquire:

1. resets any existing suite first;
2. rejects null SPBasicSuite or null suite name;
3. calls AcquireSuite;
4. requires both success error code and non-null returned pointer;
5. stores basic suite, name, version and typed function table.

reset:

1. calls ReleaseSuite only when a suite is currently owned;
2. clears all stored state;
3. is safe to call repeatedly.

Move construction/assignment transfer the owned acquisition and leave the source empty.

## Important suite-name lifetime

The current helper stores the suite name as a borrowed const char pointer because ReleaseSuite later needs the same name/version.

Therefore the name must outlive the PicaSuiteRef.

Good:

~~~cpp
static const char kMySuiteName[] = "com.example.MySuite";
ref.acquire(basic, kMySuiteName, 1);
~~~

Also normally safe: SDK/product suite-name constants with static lifetime.

Risky:

~~~text
temporary/local dynamically built character buffer
→ acquire succeeds
→ buffer dies
→ destructor later calls ReleaseSuite with dangling name pointer
~~~

The helper does not copy the name.

## Version policy

Public suite version is part of compatibility.

Do not always request the newest version and assume old AE hosts provide it.

A product policy may be:

~~~text
try required version
→ if absent, fail feature with explicit diagnostic
~~~

or, where APIs genuinely support a compatibility fallback:

~~~text
try preferred version
→ try documented older version
→ adapt through an explicit wrapper
~~~

Do not reinterpret an older function table as a newer struct.

## Optional dependency

For an optional service:

~~~text
AcquireSuite fails
→ feature unavailable
→ product remains usable
~~~

For a required service:

~~~text
AcquireSuite fails
→ initialization/command fails explicitly
→ diagnostic names suite/version
~~~

Never dereference a null table.

## Threading

Suite availability does not imply suite functions are thread-safe.

The acquisition helper also does not grant permission to acquire/release on arbitrary worker threads.

Follow the threading contract of the host/API in which SPBasicSuite is being used.

## Host lifetime

PicaSuiteRef stores the SPBasicSuite pointer and calls ReleaseSuite from reset/destructor.

Destroy/reset it before the host invalidates SPBasicSuite.

Do not put it in a process-global object whose static destructor can run after After Effects teardown.

## Cleanup error boundary

reset currently discards ReleaseSuite return status.

That is appropriate only where cleanup failure cannot be usefully recovered at destructor time.

If release failure must be logged/gated, use an explicit release path that returns the SPErr before the fallback destructor path.

## Test cases

The foundation test verifies:

- successful acquire;
- typed suite access;
- move construction;
- move assignment;
- repeated reset;
- exactly one release;
- acquisition failure leaves owner empty.

For a concrete product, useful runtime cases include:

- provider missing;
- wrong version;
- shutdown order;
- multiple consumers;
- repeated acquire/release;
- any declared concurrency mode.

Those tests support product runtime/support claims; they are not editorial prerequisites for Bible.

## Verification boundary

Stub tests prove local ownership mechanics only.

They do not prove real suite discovery, provider lifetime or thread legality. Bible records that boundary instead of treating missing host execution as unfinished documentation.
