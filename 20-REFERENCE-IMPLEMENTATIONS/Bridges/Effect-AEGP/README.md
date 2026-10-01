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

For the supplied SDK 25.6, current EffectSuite4 includes an explicit PF_Cmd argument. Historical ProjDumper syntax is older and must not be copied as the current signature.

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

## Tests

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

## Verification boundary

The contract is source-reviewed against SDK 25.6 and sample history, but the Bible bridge remains runtime result not claimed until the actual caller/effect pair is compiled and run.
