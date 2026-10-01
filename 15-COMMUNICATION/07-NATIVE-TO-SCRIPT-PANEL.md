# Native <-> script/panel: как собирать гибридный продукт

A hybrid AE product usually has three different jobs:

1. UI and user interaction.
2. Project automation.
3. Native high-performance work.

Do not force all three into one runtime.

## Recommended architecture

```text
UI layer
  CEP now / UXP later
       |
       | versioned commands + JSON
       v
Automation layer
  ExtendScript dispatcher
       |
       +---- project edits ----------> AE scripting DOM
       |
       +---- control native feature -> parameter/menu/file/IPC bridge

Native layer
  Effect plug-in / AEGP service
       |
       +---- PICA suites ---> AE native APIs
       +---- shared suite --> other native modules
       +---- external IPC --> helper/service when justified
```

The layer boundary is more important than the UI technology. A future CEP -> UXP migration should not require rewriting the domain model or native engine.

## Which bridge should you use?

| Need | Preferred path |
|---|---|
| Rename layers, create comps, set properties | Scripting DOM |
| Add a small native command reachable from AE | AEGP command/menu/service |
| Effect parameter or render behavior | Effect API |
| Native module to native module | PICA/shared suite |
| Panel calling project automation | CEP/UXP -> scripting bridge |
| Heavy external compute | Helper/service + explicit IPC |
| High-volume pixels | Native effect/GPU path, not JSON |

## Native -> scripting

AEGP Utility Suite exposes script execution capabilities such as `AEGP_ExecuteScript`.

Use this when:

- the scripting DOM exposes a capability not convenient in the native API;
- the call is infrequent;
- synchronous execution is acceptable;
- the script is controlled by the product.

Do not turn native-to-script execution into a high-frequency RPC bus.

## Panel -> native

There is no reason to invent an undocumented direct pointer bridge from HTML to an AE plug-in.

Common patterns are:

### 1. Project state as the bridge

The panel writes normal AE state that the effect/native plug-in already reads:

- effect parameters;
- layer markers;
- footage/project data;
- controlled files.

Simple and robust when the native behavior naturally depends on project state.

### 2. Script/AEGP command bridge

Panel command:

```text
panel
 -> ExtendScript
 -> host-visible command/state
 -> AEGP/effect action
```

Good for low-rate control operations.

### 3. External IPC

For a helper process or service:

```text
panel/native module
 -> versioned IPC
 -> helper/service
 -> response/progress
```

Possible transports:

- localhost socket;
- named pipe;
- Unix domain socket;
- child process stdin/stdout;
- temporary file + atomic rename;
- shared memory only when necessary.

Undocumented AE internal IPC is not a product API.

## IPC contract

Every nontrivial native IPC should define:

- protocol version;
- message type/opcode;
- request ID;
- payload size;
- timeout;
- cancellation behavior;
- ownership of buffers/files;
- process shutdown behavior;
- compatibility policy.

Example header:

```cpp
struct MsgHeader {
    uint32_t size;
    uint32_t version;
    uint32_t opcode;
    uint32_t flags;
    uint64_t request_id;
};
```

Validate the header before reading the payload.

## State ownership

Choose one source of truth for each piece of data.

Examples:

```text
project-visible setting -> AE project/effect parameter
panel-only transient UI -> panel state
render cache -> native render/cache layer
account/session -> service/auth layer
large derived asset -> file/cache store
```

Do not keep the same authoritative mutable state independently in CEP, ExtendScript and native code.

## Snapshot model

For complex panels, prefer:

```text
AE state
 -> read/normalize
 -> immutable UI snapshot
 -> UI renders snapshot
 -> user command
 -> host mutation
 -> invalidate
 -> read new snapshot
```

This avoids fragile incremental mirroring of host internals.

## Threading

The UI, scripting engine, AEGP callbacks, render callbacks and helper processes do not share one threading contract.

Rules:

- AE project mutations stay on the documented host-safe boundary;
- render callbacks must obey MFR/re-entrancy rules;
- worker threads may do pure compute/files/network;
- never hold your own mutex while calling arbitrary host APIs unless the API contract explicitly permits it;
- never pass callback-scoped AE pointers to a worker for later use.

## Failure model

Design for each component disappearing independently:

- panel reloads;
- AE project changes;
- effect instance is deleted;
- helper process crashes;
- helper is upgraded;
- socket closes;
- stale reply arrives;
- AE shuts down.

A robust protocol returns to a known state instead of assuming all components have identical lifetime.

## Versioning

Protocol compatibility should be explicit.

Example:

```text
major mismatch -> refuse with clear error
minor mismatch -> negotiate supported features
unknown optional field -> ignore if schema permits
unknown required feature -> fail closed
```

Do not infer compatibility from product marketing version alone.

## Security

For localhost/helper IPC:

- authenticate the peer when privileged operations are possible;
- use unguessable session tokens where appropriate;
- do not expose an unauthenticated arbitrary-file or command API;
- validate paths and payload sizes;
- never allow "run arbitrary shell command" as a convenience protocol.

## Performance rule

Only cross a runtime boundary when there is a clear reason.

A good architecture minimizes:

```text
UI <-> script <-> native <-> helper
```

round-trips while keeping ownership and responsibilities clear.

## Verification checklist

For a hybrid product, record tests for:

- panel reload;
- AE project close/open;
- native plug-in missing;
- version mismatch;
- helper missing/crashed;
- malformed message;
- timeout;
- cancellation;
- Unicode/path handling;
- repeated request;
- stale response;
- AE shutdown;
- clean reinstall/upgrade.

Source-level architecture is not host verification. The actual bridge must still be exercised inside supported AE builds.


## Project case-study lessons

The [FSTR Line / AE Hot Loader reuse audit](../22-PROJECT-CASE-STUDIES/REUSE-AUDIT-2026-10-01.md) provides two practical boundaries:

- FSTR Line supports the snapshot → guarded command → Host Adapter pattern, request coalescing and generation-based stale-response rejection as reusable architecture. Its original AE synchronization limitation remains scoped to that project.
- AE Hot Loader supports request/version correlation and main-thread ownership as useful bridge principles, but its text-file bridge is a PoC-specific transport and its private `ML::LoadPlugins` path remains research-only.

Do not import a private loader path into an ordinary panel/native recipe just because the control-plane pattern is reusable.
