# CEP panel <-> ExtendScript

CEP panel code and ExtendScript live in different runtimes. Treat the bridge as an explicit RPC boundary, not as a convenient string-eval shortcut.

## HTML/JS -> AE

The normal CEP bridge is `CSInterface.evalScript()`:

```js
const cs = new CSInterface();

cs.evalScript(
  '$._myTool.dispatch(' + JSON.stringify(JSON.stringify(message)) + ')',
  function (raw) {
    // parse the response envelope here
  }
);
```

The evaluated code runs in the host application's ExtendScript engine and therefore shares the normal scripting limitations of After Effects.

## One dispatcher, not many string-built calls

Avoid spreading calls such as this throughout the UI:

```js
cs.evalScript('renameLayer("' + userText + '")');
```

Problems:

- quoting/escaping bugs;
- accidental code injection;
- no stable request schema;
- inconsistent error handling;
- impossible-to-centralize logging and compatibility gates.

Prefer a single dispatcher:

```text
CEP UI
  -> JSON request
  -> one evalScript dispatcher
  -> command router
  -> AE scripting DOM
  -> JSON response
  -> UI
```

Recommended request shape:

```json
{
  "version": 1,
  "requestId": "42",
  "command": "renameSelectedLayer",
  "payload": {
    "name": "Title"
  }
}
```

Recommended response envelope:

```json
{
  "ok": true,
  "requestId": "42",
  "result": {
    "changed": 1
  }
}
```

Failure:

```json
{
  "ok": false,
  "requestId": "42",
  "error": {
    "code": "NO_ACTIVE_COMP",
    "message": "No active composition"
  }
}
```

## ExtendScript dispatcher shape

Keep host-side dispatch small and deterministic:

```jsx
$._myTool = $._myTool || {};

$._myTool.dispatch = function (raw) {
    var req = JSON.parse(raw);

    try {
        var result;

        switch (req.command) {
            case "renameSelectedLayer":
                result = $._myTool.renameSelectedLayer(req.payload);
                break;

            default:
                throw new Error("UNKNOWN_COMMAND");
        }

        return JSON.stringify({
            ok: true,
            requestId: req.requestId,
            result: result
        });
    } catch (err) {
        return JSON.stringify({
            ok: false,
            requestId: req.requestId,
            error: {
                code: err && err.message ? err.message : "HOST_ERROR"
            }
        });
    }
};
```

The exact JSON implementation must match the ExtendScript version/runtime available in the supported AE releases.

## Command design

A command should be:

- small enough to understand and test;
- idempotent when possible;
- explicit about whether it mutates the project;
- explicit about whether it requires an active project/comp/layer;
- versioned when its payload changes;
- free of UI-only assumptions unless the command is intentionally interactive.

Do not send individual property mutations across the bridge if one host command can perform the complete operation safely. Bridge latency and host scheduling make chatty protocols fragile.

Bad:

```text
set layer
set property
set property
set key
set key
set key
```

Better:

```text
applyAnimationPreset(payload)
```

with one validated payload and one undo group.

## Undo boundaries

Commands that mutate the AE project should own their undo scope:

```jsx
app.beginUndoGroup("My Tool");

try {
    // mutations
} finally {
    app.endUndoGroup();
}
```

A panel button click should normally create one understandable undo step, not dozens of low-level ones.

## Large data

`evalScript()` is a control channel, not a high-throughput binary transport.

Do not push:

- full-resolution pixel buffers;
- large model weights;
- huge encoded media;
- megabytes of per-frame telemetry;

through string serialization unless measurements prove it is acceptable.

For large payloads, use a deliberate secondary transport such as:

- temporary file + atomic rename;
- localhost service;
- named pipe / Unix domain socket;
- child-process stdin/stdout;
- native shared memory only after profiling and with explicit ownership.

The CEP/ExtendScript message should carry control metadata and a path/token, not the entire heavy payload.

## AE/ExtendScript -> panel

CEP/CSXS events can be used for host-to-panel notification.

A useful pattern is:

```text
host mutation
 -> dispatch small event
 -> panel invalidates local snapshot
 -> panel requests fresh state
```

Prefer invalidation events over trying to mirror every host object mutation in the UI.

## Request ordering

Do not assume callbacks return in the same logical order as user actions once you introduce async work around the bridge.

Include:

- `requestId`;
- optional `document/project generation`;
- optional `command sequence`;
- stale-response rejection on the UI side.

If a newer request supersedes an older one, the UI should ignore the stale result.

## Cancellation

ExtendScript itself is not a general preemptible task system.

For long operations:

1. split work into bounded chunks where possible;
2. expose progress/cancel state through your own command protocol;
3. avoid leaving the project half-mutated;
4. define rollback or safe partial-completion behavior.

If true asynchronous heavy work is required, move that work outside the scripting engine and keep AE mutations on the documented host boundary.

## Security

Treat every message as untrusted input even when the panel is local.

Validate:

- command name;
- protocol version;
- payload type/size;
- paths;
- numeric ranges;
- requested file operations.

Never evaluate user-provided JavaScript/ExtendScript source as a protocol feature.

## Testing

At minimum test:

- valid command;
- unknown command;
- malformed JSON;
- missing required field;
- Unicode;
- quotes/backslashes/newlines;
- very long strings;
- stale request rejection;
- host command error;
- no active project/comp;
- repeated command;
- panel reload during an outstanding request.

Bridge unit tests should run without AE by testing serialization, validation and routing separately. Host verification is still required for actual AE DOM behavior.

See also:

- [ExtendScript -> After Effects](05-SCRIPT-TO-AE.md)
- [Native <-> script/panel](07-NATIVE-TO-SCRIPT-PANEL.md)
- [Threading boundaries](08-THREADING-BOUNDARIES.md)
- [Data ownership](09-DATA-OWNERSHIP.md)
- `16-WORKING-TEMPLATES/cep-panel-bridge/`
