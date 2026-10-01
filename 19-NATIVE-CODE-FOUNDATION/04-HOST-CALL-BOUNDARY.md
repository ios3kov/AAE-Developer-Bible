# Host callback ABI boundary

C++ exceptions must not escape through a C callback/entry point invoked by After Effects.

The foundation helper code/HostCallbackGuard.h provides a minimal containment boundary.

## Model

~~~text
After Effects C ABI
→ noexcept wrapper
→ C++ implementation
→ A_Err returned to host
~~~

Inside the implementation you may use normal C++ according to project policy. At the outer host boundary, every exception path must be converted to a valid host error.

## Helper behavior

GuardAeHostCallback accepts:

- callable;
- fallback A_Err selected by the product.

It is noexcept.

Behavior:

~~~text
callable returns A_Err
→ return it unchanged

callable throws nonzero A_Err
→ return that A_Err

callable throws zero A_Err
→ return fallback

callable throws anything else
→ return fallback
~~~

The helper deliberately does not invent one universal Adobe error constant. Different callback contexts/products may need a deliberate fallback choice.

## Example

~~~cpp
extern "C" A_Err SomeHostEntry(...) {
    return GuardAeHostCallback(
        [&]() -> A_Err {
            return DispatchHostCall(...);
        },
        kProjectChosenFallback);
}
~~~

The exported function remains a simple ABI boundary.

## Why catch-all exists

Exceptions can originate from:

- product code;
- STL allocation;
- third-party library;
- explicit throw;
- unexpected internal error.

Letting an exception unwind through a foreign C ABI is not a safe recovery strategy.

## Logging

The current helper converts errors but does not log exception type/message.

If diagnostics are required, log inside the product-owned C++ layer or wrap the callable with a no-throw diagnostic policy.

Logging itself must not throw across the host boundary.

Do not perform large synchronous logging/network work from render callbacks.

## Thrown A_Err policy

The helper supports code that throws A_Err, but that does not mean throwing host error integers throughout the architecture is recommended.

A cleaner project may prefer:

~~~text
internal typed result/status
→ boundary maps status to A_Err
~~~

Use thrown A_Err only if the codebase has an intentional policy.

## Cleanup before conversion

Exception containment does not replace ownership safety.

Resources acquired before the throw still need RAII/scope cleanup.

~~~text
acquire resource owner
→ operation throws
→ owner destructor releases
→ Guard maps exception
→ host receives A_Err
~~~

This is why the callback guard and ownership helpers are designed to compose.

## Do not swallow fatal process conditions blindly

A catch-all handles C++ exceptions. It is not a universal recovery mechanism for arbitrary memory corruption, access violations, corrupted host state or OS fatal signals.

If memory is corrupted, returning an error may not make the process safe.

Treat sanitizer/crash evidence separately.

## Callback-specific fallback

Choose fallback based on:

- callback contract;
- whether host expects PF_Err/A_Err domain;
- whether partial host mutation occurred;
- whether more specific product error mapping exists.

Record the project policy instead of scattering magic integers.

## Test coverage

tests/test_foundation.cpp verifies:

- normal A_Err return passthrough;
- std::runtime_error maps to fallback;
- thrown nonzero A_Err is preserved;
- thrown zero A_Err maps to fallback.

For a concrete product, useful tests include:

- allocation failure policy where feasible;
- third-party exception;
- callback cleanup after exception;
- host behavior for the chosen fallback error.

## Product rule

Every exported/native host callback in product C++ should have a documented exception boundary.

Bible's local guard tests demonstrate the containment pattern; they do not claim that every possible product callback/third-party failure has been executed inside After Effects.
