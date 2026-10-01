# Recipe — panel + native core

## Goal

Build a panel-driven product without coupling UI runtime, After Effects automation and heavy native compute into one fragile component.

In the 2026 transition period, keep the UI shell replaceable so CEP-specific code can later be exchanged for a verified AE UXP path.

## 1. Draw the ownership diagram first

~~~text
UI shell
  CEP now / future verified AE UXP
        |
        | commands / responses
        v
Bridge adapter
        |
        v
AE automation layer
  ExtendScript / supported host API
        |
        +---- project mutation
        |
        +---- control request
                  |
                  v
Native core
  Effect / AEGP / shared suite / helper
~~~

Assign one owner for every persistent state.

## 2. Separate control and data planes

Panel bridge carries:

- command IDs;
- small parameter objects;
- paths/IDs;
- progress;
- status/error;
- invalidation.

Do not send pixel/audio/large binary buffers as giant evalScript/Base64 messages unless there is a measured, unavoidable reason.

Keep heavy data native or in a purpose-built helper/data path.

## 3. Define protocol version 1 before UI implementation

Request:

~~~json
{
  "protocol": 1,
  "requestId": "123",
  "command": "analyzeFrame",
  "payload": {
    "layerId": 42,
    "time": 1.25
  }
}
~~~

Response:

~~~json
{
  "ok": true,
  "requestId": "123",
  "result": {
    "status": "ready"
  }
}
~~~

Error:

~~~json
{
  "ok": false,
  "requestId": "123",
  "error": {
    "code": "NO_LAYER",
    "message": "Target layer is not available"
  }
}
~~~

Human text is not the only machine-readable error contract.

## 4. One panel bridge

Do not scatter evalScript or native IPC calls through UI components.

~~~text
component
→ domain command
→ bridge.request
→ transport adapter
~~~

This is what makes a future panel-runtime migration practical.

## 5. Validate every boundary

Panel side validates user inputs.

Automation/native side validates again:

- protocol;
- command allowlist;
- message size;
- enum/range;
- path;
- target project object existence;
- native capability/version.

Never assume local UI input is trusted because it came from your own panel.

## 6. Use explicit handshake

At startup:

~~~text
panel boot
→ bridge handshake
→ protocol versions/capabilities
→ query authoritative host state
→ render UI
~~~

If native/helper version is incompatible, fail clearly with component mismatch instead of sending unknown commands.

## 7. Avoid stale responses

Use request/generation identity.

~~~text
request generation 7
user changes selection → generation 8
response 7 arrives
→ ignore
~~~

This matters for selection/preview-heavy panels.

## 8. Choose the native bridge deliberately

Possible documented/product-owned paths:

- AEGP EffectCallGeneric for small synchronous commands to one effect instance;
- published PICA suite for in-process native service;
- AEGP ExecuteScript for rare scripting-DOM capability;
- explicit external IPC for a helper/service.

Do not make undocumented AE internal IPC a shipping dependency.

## 9. Long operation lifecycle

~~~text
start(requestId)
→ progress
→ cancel(requestId)
→ canceled or completed
~~~

Panel reload must not resurrect an old operation result into new state.

Define timeout/liveness behavior for helpers.

## 10. Panel reload/restart

Panel DOM is not authoritative persistence.

On reload:

1. create bridge;
2. handshake;
3. query host/product state;
4. rebuild UI;
5. ignore stale responses from the previous generation.

Test AE restart too.

## 11. Thread boundary

Heavy worker may do pure compute/IO.

AE project/suite access stays on the documented host path unless a specific API explicitly permits other threads.

Do not hold a product mutex while calling back into AE.

## 12. Packaging/version skew

Treat these as independently identifiable components:

- panel;
- JSX/automation bundle;
- native plug-in;
- helper.

Installer/update tests must cover partial mismatch or ensure atomic replacement.

## 13. Acceptance gate

The hybrid product baseline passes when:

- fresh install opens panel;
- handshake succeeds;
- one read command works;
- one project mutation works;
- one native command works;
- malformed command is rejected;
- stale response is ignored;
- cancel works;
- panel reload reconstructs state;
- AE restart works;
- missing/wrong native component gives clear recovery;
- no large binary traffic is accidentally routed through JSX.

See [Communication architecture](../15-COMMUNICATION/README.md).
