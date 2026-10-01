# ExtendScript -> After Effects

ExtendScript executes inside the After Effects scripting environment and accesses the host through the scripting DOM: app, project, items, compositions, layers, properties/keyframes, import and render queue.

It is a control and automation API, not a per-pixel render API.

## Typical command flow

~~~jsx
app.beginUndoGroup("My Tool");

try {
    var comp = app.project.activeItem;

    if (!(comp instanceof CompItem)) {
        throw new Error("No active composition.");
    }

    if (comp.numLayers < 1) {
        throw new Error("Composition has no layers.");
    }

    comp.layer(1).name = "Renamed by Tool";
} finally {
    app.endUndoGroup();
}
~~~

Validate prerequisites before mutation. beginUndoGroup/endUndoGroup creates coherent user undo history; it does not promise automatic rollback after an exception.

## Main-thread implication

Host-side scripting is synchronous from the point of view of the AE operation. In CEP, Adobe explicitly documents that evalScript executes in the host ExtendScript engine on the host main thread.

Design consequences:

- prefer short commands to one giant script;
- do not poll AE state continuously from a panel;
- keep binary/heavy compute out of JSON/string bridge traffic;
- validate and batch project mutations;
- return a compact result instead of hundreds of UI-side follow-up queries.

## Stable identifiers

For effects/properties, prefer match names where available. User-visible layer/effect names are presentation data and can be localized or renamed.

If the script creates product-owned objects, store a deliberate stable identifier instead of depending only on layer.name.

## Structural mutation invalidates references

Adding, moving or removing properties in indexed groups can invalidate saved ExtendScript references.

A protocol handler that performs a structural edit should reacquire the affected objects before the next operation.

Do not expose a fake pointer-identity model to a panel. A panel should request objects by stable product ID or by a deliberately resolved path each time.

## Script -> effect/property

A script or panel can control a native effect through normal project state:

~~~text
script
→ layer
→ Effects property group
→ target effect by match name
→ parameter property
→ setValue / setValueAtTime
~~~

This is often the safest bridge when the operation can naturally be expressed as effect parameters or project data.

Advantages:

- AE owns project persistence;
- undo/keyframes use normal host concepts;
- parameter dependencies remain visible to the host;
- no custom IPC is needed.

Do not abuse effect parameters as an unbounded binary transport.

## Script -> menu command

app.executeCommand(id) can invoke a host command, but numeric command IDs are not a strong public compatibility contract across versions/localizations.

Use only when:

- no better public scripting API exists;
- the dependency is isolated;
- supported host versions were actually tested;
- failure has a safe fallback;
- the command ID dependency is documented in the support matrix.

Do not build a large product around undocumented menu-ID archaeology.

## Native -> script

AEGP Utility Suite exposes AEGP_ExecuteScript, allowing native AEGP code to execute ExtendScript for a capability better exposed through the scripting DOM.

Treat this as a synchronous host bridge:

- keep the called script small;
- obey the actual suite ownership contract for returned data;
- do not call from arbitrary worker threads;
- avoid circular designs where JSX calls native and native immediately invokes a large JSX workflow back.

One layer should own the command lifecycle.

## Request and response contract

A script command should accept plain data and return plain data.

Request:

~~~json
{
  "protocol": 1,
  "requestId": "7",
  "command": "renameSelected",
  "payload": {"name": "Hero"}
}
~~~

Failure:

~~~json
{
  "ok": false,
  "requestId": "7",
  "error": {
    "code": "NO_ACTIVE_COMP",
    "message": "No active composition"
  }
}
~~~

The UI can localize a stable error code while logs retain the source message.

## Cancellation

ExtendScript does not make every long host mutation safely cancellable automatically.

If a workflow supports cancel:

1. define checkpoints between atomic chunks;
2. decide what partial result is valid;
3. close undo groups and files in finally blocks;
4. never interrupt a product-owned file halfway through an unsafe write;
5. return CANCELLED as a normal protocol result where appropriate.

## Recommended boundary

~~~text
plain request
→ validate
→ resolve AE host objects
→ perform short query/mutation
→ normalize plain response
~~~

Never leak raw host object references into CEP, helper-process or native IPC protocols.

## Verification boundary

This chapter describes the scripting communication contract. It does not upgrade the current JSX examples to host-verified status; AE execution remains pending in the completion matrix.
