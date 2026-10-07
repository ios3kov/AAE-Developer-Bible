# PICA provider ↔ consumer reference

Status: **sample-derived / runtime result not claimed**.

SharedSuite.h forwards to the canonical shared ABI in 16-WORKING-TEMPLATES/pica-shared-suite.

## Model

~~~text
provider initializes
→ publishes versioned function table
→ consumer AcquireSuite(name, version)
→ consumer calls table
→ consumer ReleaseSuite(name, version)
→ provider remains valid for active acquisitions/lifecycle
~~~

The supplied SDK review uses Sweetie as the provider pattern and Checkout as an optional consumer pattern.

## ABI design

Treat the suite struct as a C ABI.
The forwarding header is C++-source-only with C-shaped ABI data, not a C-compatible
header or a provider/consumer implementation. See the [actual source boundary](../../../14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md#actual-shared-header-versus-service-implementation-2026-10-07).

Use:

- stable unique suite name;
- explicit public version;
- fixed-width/POD-compatible inputs;
- explicit lengths/sizes;
- explicit ownership;
- A_Err/product result codes.

Avoid:

- std::string/std::vector;
- exceptions crossing boundary;
- C++ class layout;
- allocator ambiguity;
- temporary borrowed pointers with undocumented lifetime.

## Public version

AcquireSuite uses the public suite version.

Do not confuse it with low-level internal provider version fields.

A breaking layout/semantic change needs a new public version.

## Provider lifetime

A published function table must remain valid for every legitimate consumer acquisition.

Static table lifetime is a simple pattern used by the SDK sample, but it does not prove hot replacement/unload safety.

Do not replace or free provider state under active consumers without a separately designed lifecycle.

## Consumer ownership

Use a balanced acquire/release owner such as 19-NATIVE-CODE-FOUNDATION/code/PicaSuiteRef.h.

Remember that the helper itself requires:

- stable suite-name lifetime;
- valid SPBasicSuite until release;
- correct thread/lifecycle for acquisition.

## Optional vs required

Optional:

~~~text
suite absent
→ feature disabled
→ plug-in continues
~~~

Required:

~~~text
suite absent/wrong version
→ initialization/command fails clearly
~~~

Never dereference a missing table.

## Thread contract

Publishing a suite does not make its functions thread-safe.

Document each function/service as one of:

- main-thread-only;
- render-thread-safe;
- serialized internally;
- re-entrant;
- may call host;
- must not call host.

Consumer follows the most conservative contract if unspecified.

## Product validation cases

- provider missing;
- correct version;
- wrong version;
- repeated acquire/release;
- two consumers;
- provider function error;
- malformed sizes;
- shutdown ordering;
- concurrency mode;
- restart.

## Suite-name lifetime

`PicaSuiteRef` stores the suite-name pointer so it can call matching `ReleaseSuite` later.

Therefore the name storage must outlive the acquisition. Prefer a static suite-name literal or equivalent stable product-owned storage.

## Shutdown boundary

Published table lifetime and backing service-state lifetime are separate.

Do not destroy service state merely because your own initializer is ending, and do not infer hot-unload safety from suite reference counting alone.

If a product supports dynamic provider restart/replacement, that requires its own explicit lifecycle/protocol evidence.

## Verification boundary

Sweetie/Checkout establish the SDK provider/consumer pattern, not a runtime result for the Bible template. The reference remains RUNTIME-NOT-CLAIMED unless separate runtime evidence exists; product compilation/host execution is not a Bible editorial-completion requirement.
