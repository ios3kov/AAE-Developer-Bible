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

## Tests

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

## Verification boundary

Sweetie/Checkout prove a provider/consumer pattern in the SDK, not this product ABI in the host. The Bible shared suite remains runtime result not claimed until provider and consumer are compiled and exercised together.
