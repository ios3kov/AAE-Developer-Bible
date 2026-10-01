# Effect ↔ AEGP bridge reference

Status: **sample-derived / runtime result not claimed**.

Protocol.h forwards to the canonical protocol in 16-WORKING-TEMPLATES/effect-aegp-generic-bridge.

## Supported native path

The reviewed direct path is AEGP_EffectCallGeneric:

~~~text
AEGP finds target effect instance
→ owns/holds EffectRef according to host contract
→ constructs versioned message
→ converts target time to layer timebase
→ calls current EffectSuite generic API
→ Effect receives generic selector/command
→ reads/writes message synchronously
→ call returns
→ caller releases target references
~~~

For the supplied SDK 25.6, current EffectSuite5 includes the explicit PF_Cmd argument. Historical ProjDumper/older-suite syntax is pattern evidence and must not be copied as the current signature.

## Protocol rules

Message ABI must be self-describing:

- fixed-width integer fields;
- total size;
- protocol version;
- opcode;
- request ID;
- result/status;
- optional payload length.

Validate size/version before reading the extended payload.

Do not expose:

- STL containers;
- C++ exceptions;
- allocator-specific objects;
- temporary pointers;
- AE host handles as persistent external identity.

## Synchronous pointer lifetime

The void pointer payload is treated as valid for the call unless a stronger ownership transfer is explicitly documented by your own protocol/API.

~~~text
caller owns storage
→ effect reads/writes during call
→ return
→ effect does not retain pointer
~~~

For long-lived work, pass an ID into a separate product-owned service, not a pointer to stack memory.

## Timebase

The current SDK contract uses target layer time.

Do not pass composition time by assumption. Convert using documented host APIs when needed.

## Render dependency warning

Do not hide render-affecting state behind generic messages.

If rendering depends on state changed by AEGP but AE cannot see that dependency, cached frames can become stale.

Render truth should remain visible through supported parameters/dependency/cache identity.

## Error model

Keep separate:

1. host delivery A_Err;
2. protocol validation error;
3. command/domain result.

This makes diagnostics distinguish target missing from command rejected.

## Product validation cases

- target effect missing;
- target removed/reordered;
- wrong protocol version;
- short message;
- unknown opcode;
- correct request/response;
- layer-time conversion;
- repeated calls;
- save/reopen when persistent state involved;
- stale-cache check;
- cleanup on call error.

## Target-ref freshness

Resolve the current target effect for each semantic command whenever project edits may have invalidated an older ref.

Do not keep one `AEGP_EffectRefH` in long-lived UI/background state and assume it survives effect removal/reorder/project changes.

## Protocol evolution

A new message version must preserve explicit size/version validation.

Do not reinterpret a V1 message buffer as a larger V2 without checking the caller-provided size first.

Reserved/tail fields should have defined defaults so compatible additive evolution remains possible.

## Verification boundary

The contract is source-reviewed against SDK 25.6 and sample history. Bible labels the reference RUNTIME-NOT-CLAIMED unless a separate runtime record exists; compilation/host execution is product evidence, not a documentation-completion requirement.
