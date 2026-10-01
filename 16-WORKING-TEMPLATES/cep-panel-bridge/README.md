# CEP -> ExtendScript JSON bridge

Standalone logic files for a CEP panel.

To package as an actual extension, add:

- Adobe `CSInterface.js` from the CEP Resources version you target;
- `CSXS/manifest.xml` matching the AE/CEP versions you support;
- load `host/index.jsx` from manifest or panel startup;
- load a vetted ES3-compatible JSON polyfill before `host/index.jsx` when ExtendScript has no `JSON` global;
- signing/packaging config.

## Protocol

The reusable piece is a single versioned dispatcher protocol:

```json
{
  "protocol": 1,
  "requestId": "123-1",
  "command": "renameSelected",
  "payload": {
    "prefix": "Bible_"
  }
}
```

Success:

```json
{
  "ok": true,
  "requestId": "123-1",
  "result": {
    "changed": 2
  }
}
```

Failure:

```json
{
  "ok": false,
  "requestId": "123-1",
  "error": {
    "code": "NO_ACTIVE_COMP",
    "message": "No active composition"
  }
}
```

The panel tracks the latest request and ignores a stale reply after a newer command supersedes it.

The template deliberately demonstrates:

- one dispatcher instead of arbitrary generated code;
- `command/payload` schema matching the communication chapter;
- request IDs;
- structured error codes;
- host-owned undo scope;
- stale-response rejection.

It does **not** prove AE host execution. Packaging, JSON-polyfill compatibility and actual host behavior still require the verification steps in `10-TESTING/`.

See [CEP panel <-> ExtendScript](../../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md).
