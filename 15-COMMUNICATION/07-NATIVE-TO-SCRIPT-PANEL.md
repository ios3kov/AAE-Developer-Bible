# Native <-> script/panel: hybrid product architecture

A hybrid After Effects product can contain:

- CEP, UXP or ScriptUI interface;
- ExtendScript automation;
- native Effect plug-in;
- AEGP service;
- external helper process.

The architectural failure mode is allowing every layer to call every other layer ad hoc.

## Recommended layers

~~~text
UI shell
  CEP now / UXP later / ScriptUI for small tools
       |
       | typed commands + plain data
       v
Automation / command layer
  ExtendScript dispatcher or future host adapter
       |
       +---- project edits ----------> AE scripting DOM
       |
       +---- native control ---------> effect params / documented bridge
       |
       +---- external service -------> explicit IPC adapter

Native layer
  Effect plug-in / AEGP
       |
       +---- PF/AEGP suites ---------> After Effects
       +---- PICA/shared suite ------> another native module
~~~

Keep the UI unaware of raw AE handles and keep native code unaware of DOM widgets.

## Control plane vs data plane

Use panel/script messaging for control:

- start analysis;
- choose mode;
- set parameters;
- request status;
- receive small result summaries.

Do not push heavy data through it:

- pixel frames;
- large ML tensors;
- multi-megabyte caches;
- thousands of messages per frame.

Large data should stay native or in a helper, while UI sends commands/references.

## Simplest bridge first: project state

If a native effect can be configured using normal AE parameters, let script/panel modify those parameters through the scripting DOM.

~~~text
panel
→ dispatcher.jsx
→ layer/effect/parameter
→ native effect receives normal parameter state during render
~~~

Benefits:

- AE owns project persistence;
- undo and keyframes use normal host concepts;
- render dependencies are visible to the host;
- no private transport is required.

Use a custom bridge only when the normal project model cannot express the operation.

## AEGP / PICA bridge

For native-to-native communication use documented AEGP/PICA mechanisms described elsewhere in this section.

If a shared suite is used, define:

- suite name;
- suite version;
- POD/C-compatible function table boundary where practical;
- ownership of every pointer and returned object;
- thread constraints;
- acquire/release lifetime;
- behavior when the provider is absent;
- behavior when the requested version is unsupported.

Do not invent a raw global pointer bridge between separately loaded modules.

## Native -> script

AEGP_ExecuteScript can bridge from native AEGP code into ExtendScript when the scripting DOM exposes a useful capability not available in the native route.

Use it deliberately, not as high-frequency IPC.

Avoid:

~~~text
CEP
→ huge JSX command
→ native call
→ huge ExecuteScript call back
→ CEP event storm
~~~

One layer must own the request lifecycle.

## CEP event bridge

For CEP products, native/ExtendScript code can use supported CSXS/PlugPlug event mechanisms for notifications.

Treat the event bus as messages:

~~~text
producer
→ event type + small payload
→ panel listener
→ state invalidation / reload
~~~

Do not make undocumented Adobe internal events or internal IPC a production contract.

## External helper IPC

When UI/native/service are separate processes, choose explicit versioned IPC.

Reasonable transports:

- localhost socket;
- Windows named pipe;
- macOS Unix domain socket;
- child-process stdin/stdout;
- product-owned temporary files with atomic rename;
- shared memory only after profiling and with explicit synchronization/ownership.

The transport is secondary. The protocol contract is primary.

## Protocol header

For a native binary protocol, validate compatibility before parsing payload:

~~~cpp
struct MsgHeader {
    uint32_t size;
    uint32_t version;
    uint32_t opcode;
    uint32_t flags;
    uint64_t request_id;
};
~~~

Validate size, version, opcode, offsets and element counts before use.

A JSON protocol should carry the same concepts explicitly.

## Request lifecycle

Every asynchronous operation needs a state model:

~~~text
created
→ accepted
→ running
→ completed | failed | cancelled
~~~

Define:

- who owns cancellation;
- whether cancellation is best-effort;
- whether a result may arrive after UI disposal;
- how duplicate request IDs are handled;
- what helper/native restart does to outstanding requests;
- whether partial output is valid after cancel.

A progress bar is not a lifecycle protocol.

## Host object ownership

Never pass across process/module boundaries:

- PF_InData pointers;
- selector-specific extra pointers;
- borrowed PF_EffectWorld pointers;
- AEGP handles with callback/project-dependent lifetime;
- pointers to temporary C++ objects;
- STL container objects as a cross-module ABI.

Copy or serialize the minimum plain data needed at the boundary.

## Threading

A worker thread may own pure compute and product-owned buffers.

Host callbacks/handles/suites should remain on documented host-safe threads. Do not assume that because your helper is asynchronous, AE project APIs become thread-safe.

For UI commands that eventually touch AE:

~~~text
worker/helper
→ finish pure work
→ enqueue/return result
→ host-side command
→ mutate/read AE
~~~

## Backpressure

If the UI can produce commands faster than native work completes, define policy:

- reject while busy;
- coalesce latest state;
- queue with a fixed maximum;
- cancel previous request and replace.

Never allow an unbounded queue of stale analysis jobs.

## Failure isolation

The panel should survive a helper/native failure and show a structured status rather than becoming permanently stuck.

The native/helper side should reject malformed messages without crashing AE.

Log enough to correlate:

- request ID;
- protocol version;
- component version;
- command/opcode;
- terminal result.

Do not log secrets or full private user content by default.

## Migration rule

A hybrid product is migration-ready when replacing CEP with UXP does not require changing the native protocol or core business model.

The shell changes; the stable command contract remains.

## Verification boundary

These are architecture rules derived from the documented AE/CEP/PICA boundaries. They do not claim that the current Bible hybrid templates have completed end-to-end host tests.
