# Published PICA suite contract

Status: **ABI design template, not a complete provider implementation and not host-verified**.

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
- do not claim hot replacement unless separately implemented and host-tested.

Sweetie publishes a static table into `kSPRuntimeSuiteList`; it does not demonstrate generic unpublish/replacement.

## Consumer requirements

- acquire exact name + public version through `SPBasicSuite`;
- handle missing suite explicitly;
- release matching acquisition on all paths;
- do not cache the table after release;
- do not assume provider load order;
- obey documented thread restrictions.

Checkout demonstrates an optional dependency: missing DuckSuite does not make the whole effect fail.

## Verification required before calling this working

1. provider present/absent;
2. wrong version;
3. correct version;
4. repeated acquire/release;
5. two consumers;
6. malformed buffer sizes;
7. service error propagation;
8. provider/consumer restart lifecycle;
9. declared concurrency mode;
10. target AE build evidence.

Reference sources: SDK Sweetie, Checkout, `SPBasicSuite`, `SPSuitesSuite`.
