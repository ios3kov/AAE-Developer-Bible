# Published PICA suite contract

Status: **ABI/source design template; no runtime result is claimed by Bible**.

Source review baseline: Adobe After Effects SDK **25.6 build 61**, especially Sweetie + Checkout. See [PICA chapter](../../14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md) and [source review](../../18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).

`SharedSuite.h` deliberately contains only the shared function-table shape. It does **not** register itself.

## Important source-language caveat

The current header uses `std::int32_t/std::uint64_t`, so it is a **C++ header with C-shaped ABI data**, not a header that can currently be included unchanged by a C translation unit.

The ABI intent remains:

- plain function-pointer table;
- no STL objects crossing the boundary;
- no exceptions crossing the boundary;
- explicit pointer/size ownership.

If true C-source compatibility is required, adapt the header to C-compatible integer declarations and test it with both C and C++ compilers.

## Provider requirements

- acquire `SPSuitesSuite`;
- publish a stable table with `AddSuite`;
- use a unique stable suite name;
- version incompatible public ABI changes;
- keep the advertised function table alive for the required provider lifetime;
- validate pointer/size inputs;
- return integer error codes; never throw through function pointers;
- document thread/lifetime rules;
- do not claim hot replacement unless the product has a separately designed lifecycle and runtime evidence.

Sweetie publishes a static table into `kSPRuntimeSuiteList`; it does not demonstrate generic unpublish/replacement.

## Consumer requirements

- acquire exact name + public version through `SPBasicSuite`;
- handle missing suite explicitly;
- release matching acquisition on all paths;
- do not cache the table after release;
- do not assume provider load order;
- obey documented thread restrictions.

Checkout demonstrates an optional dependency: missing DuckSuite does not make the whole effect fail.

## Suite-name lifetime

If consumer ownership helper stores the suite-name pointer until release, the name storage must remain valid for the entire acquisition.

Safe:

~~~text
static suite-name literal
→ acquire
→ use
→ release
~~~

Unsafe:

~~~text
temporary_string.c_str()
→ acquire
→ temporary destroyed
→ later ReleaseSuite uses dangling pointer
~~~

The Bible `PicaSuiteRef` follows the first model and documents the requirement rather than copying the name.

## Version evolution

For incompatible ABI change:

~~~text
CoreSuite1
→ new public version
→ CoreSuite2
~~~

Do not silently append/reorder/change function pointers under the same public version unless provider/consumer compatibility is explicitly designed and documented.

A multi-version consumer should use version-specific adapters, not cast one table layout to another.

## Provider shutdown

The template does not define generic hot-unpublish.

A concrete product should ensure product-owned consumers/async work stop using the service before backing provider state is destroyed.

PICA refcounting is not treated by Bible as proof of arbitrary module hot-unload safety.

## Product validation cases

If a concrete product claims these behaviors, useful runtime cases include:

1. provider present/absent;
2. wrong version;
3. correct version;
4. supported version fallback;
5. repeated acquire/release;
6. two consumers;
7. malformed buffer sizes;
8. service/domain error propagation;
9. shutdown ordering;
10. declared concurrency mode;
11. restart/hot-reload only if claimed.

## Evidence boundary

This is an ABI/source design template based on SDK 25.6 Sweetie/Checkout/PICA contracts. Bible does not claim a runtime provider/consumer result for the template.

Reference sources: SDK Sweetie, Checkout, `SPBasicSuite`, `SPSuitesSuite`.
