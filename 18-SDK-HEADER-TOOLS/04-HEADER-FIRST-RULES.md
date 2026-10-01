# Header-first rules

When documentation, sample history and memory disagree, use a strict evidence order.

## Rule 1 — exact declaration comes from the build SDK

For:

- function signature;
- struct layout;
- suite generation;
- typedef;
- macro/constant used by the compiler;

the exact target SDK header is the compile-time source of truth.

Do not rewrite a call to match a web page when the exact supported SDK header says otherwise.

## Rule 2 — ownership needs more than a prototype

A prototype rarely describes the whole lifetime.

Determine ownership from:

~~~text
header comments
+ paired acquire/dispose/checkin APIs
+ official sample usage
+ public guide
+ host test
~~~

Write down whether a returned object is:

- borrowed;
- owned;
- locked view;
- checkout requiring checkin;
- host reference requiring dispose;
- valid only inside callback.

## Rule 3 — runtime availability is separate from compile availability

A suite can exist in headers while an older target host does not provide it.

Runtime code must:

- request the exact public suite version;
- handle acquisition failure;
- use fallback when intentionally supported;
- report a clear compatibility error otherwise.

Never dereference a null table.

## Rule 4 — current header outranks historical sample for ABI

Samples are essential for workflow/lifecycle, but a bundled sample may preserve old syntax or compatibility.

If sample and current header differ:

1. record both;
2. identify likely version boundary;
3. compile against current header;
4. do not silently publish old signature as current.

The Bible already records examples of legacy/current AEGP differences.

## Rule 5 — public guide provides context, not a cast license

HTML documentation is useful for:

- design explanation;
- lifecycle;
- feature introduction;
- platform guidance.

If it conflicts with exact build headers, record an erratum/version note.

Do not cast a function pointer or suite table solely to reproduce guide syntax.

## Rule 6 — suite generations are types, not labels

Suite version changes can change:

- table layout;
- function signatures;
- semantics;
- ownership;
- availability.

Never reinterpret SuiteN as SuiteN+1 because the first members look similar.

## Rule 7 — size/version before tail fields

For versioned product messages and host structs that expose size/version:

~~~text
validate base size
→ validate supported version
→ validate total length
→ only then access optional tail
~~~

This rule prevents old/new ABI reads from running past a smaller object.

## Rule 8 — integer/enum width matters

Do not replace enum parameters with bool/int just because constants compile.

Check the exact typedef and semantic values.

The existing render-queue source review contains a concrete warning where TRUE numerically maps to a different enum state than the intended QUEUED value.

## Rule 9 — constness is a contract clue

A new const qualifier can indicate changed mutation expectations.

Do not cast const away before understanding why the API changed.

MFR-era sequence-data changes are an example of lifetime/thread semantics becoming stricter.

## Rule 10 — compiler success is not runtime proof

Headers/compiler establish source/type compatibility for a particular toolchain/SDK snapshot.

They do not prove:

- suite is available in a particular target AE build;
- PiPL loads;
- output pixels are correct;
- callback order assumption is valid;
- ownership logic is correct at runtime;
- thread safety;
- installer/signing behavior.

For **Bible**, this means: do not claim runtime behavior unless runtime evidence exists.

For a **product**, this means: support/release claims may require compiler/host/product evidence appropriate to that claim.

It does **not** mean every Bible source example must be compiled or host-tested before the documentation can be complete.

## Rule 11 — missing evidence stays at the correct evidence level

If:

- parser cannot understand a required declaration;
- sample is absent;
- documentation is ambiguous;

label that contract fact unresolved and do not fill the gap from memory.

If host run is not available, do not claim a host-observed result. The source/documented contract may still be described when its own evidence is sufficient.

Use precise labels rather than turning every missing runtime result into an editorial TODO.

## Rule 12 — preserve provenance

When a Bible chapter states an exact SDK fact, preserve enough provenance to recover:

- SDK version/build;
- header path;
- sample path if used;
- source hash in formal review records where appropriate;
- date of public-doc review.

This is what makes future SDK diffs possible.

## Practical decision table

| Question | Primary source |
|---|---|
| exact function signature | target SDK header |
| function-table generation | target SDK header |
| ownership/lifetime | header comments + sample + guide |
| introduction/deprecation | release notes/guide + runtime check |
| how Adobe wires a project | exact SDK sample |
| whether a concrete product supports it | product-specific compile/host evidence appropriate to the claim |
| current platform signing/install policy | current platform documentation |

## Stop rule

Never make code compile by weakening a native contract you have not understood.
