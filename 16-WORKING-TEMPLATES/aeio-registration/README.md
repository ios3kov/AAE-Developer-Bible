# AEIO registration working guide

Status: **registration/source guide; SDK 25.6 contract-reviewed; runtime result not claimed**.

## Why this is not a standalone implementation

AEIO registration installs a function block with many callbacks. Exact revision and required callbacks are SDK-version-sensitive.

A copied registration function without a valid callback table is not a working importer/exporter.

## Registration shape

Conceptually:

~~~cpp
A_Err RegisterMyIO(
    AEGP_SuiteHandler& suites,
    AEGP_PluginID plugin_id,
    AEGP_IORefcon refcon,
    const AEIO_ModuleInfo* module_info,
    const AEIO_FunctionBlock4* funcs)
{
    return suites.RegisterSuite5()->AEGP_RegisterIO(
        plugin_id,
        refcon,
        module_info,
        funcs);
}
~~~

The concrete supplied-25.6 review uses AEIO_ModuleInfo and AEIO_FunctionBlock4. Recheck target headers.

Exact SDK25.6 `AE_GeneralPlug.h:2791–2795` takes const pointers for both tables.
Zero initialization alone does not create a usable function block. Follow the
[IO sample reading route](../../04-AEIO/README.md#exact-io-sample-reading-walkthrough)
for callback installation and spec ownership. Sample registration uses local
tables; do not retain their addresses yourself or generalize unreviewed async lifetime.

## Module metadata

Fill only values supported by the actual implementation:

- stable signature/identity;
- file type/description;
- input/output capabilities;
- extension/type mapping where relevant.

Do not advertise audio/output/auxiliary capability before callbacks work.

## Callback table

Build the callback table from the exact SDK sample.

For an importer, implement a narrow vertical slice first:

~~~text
verify/sniff
→ create input spec
→ report basic info
→ retrieve one frame
→ dispose spec
~~~

Then add random seeking, metadata, audio and advanced features.

For an exporter:

~~~text
create output spec
→ validate settings
→ open
→ write one frame
→ close/finalize
→ dispose
~~~

Then add long sequence/audio/cancel/failure handling.

## Default callback behavior

Where the exact SDK contract explicitly permits AEIO_Err_USE_DFLT_CALLBACK, returning it can delegate optional behavior to After Effects.

Do not use it for a callback that the registered module actually promises to implement.

## Private state

Any per-file/spec private data needs:

- owner;
- initialization state;
- cleanup;
- failure cleanup;
- thread policy;
- persistence/reopen behavior if applicable.

Do not store raw callback-scoped pointers in the spec state.

## Untrusted media

File input is untrusted.

Validate:

- header size;
- offsets;
- counts;
- dimensions;
- allocation arithmetic;
- file bounds;
- decompression limits.

A malformed file must fail cleanly instead of corrupting AE memory.

## Product validation milestone

A concrete importer/exporter should not claim a capability until its relevant path has product evidence. Useful cases include:

- fresh import/export;
- deterministic frame data;
- repeated/random frame request;
- cancellation;
- malformed input/output failure;
- project save/reopen;
- cleanup/leak checks.

## Options/spec ownership

The registration layer should make the state boundary visible:

```text
host-owned InSpec/OutSpec
↕
module-owned options/private state
↕
decoder/encoder core
```

Live options and flattened options are different representations. Do not persist raw pointers or process-specific handles.

## Cancellation/failure rule

Registration-only source must not hide the fact that callbacks can be entered after partial initialization.

Every callback family needs a safe failure/cleanup path, and spec disposal must tolerate partially-created module state.

## Verification boundary

This guide preserves the registration and lifecycle contract without fabricating a stale full callback table. The exact target SDK IO/FBIO sample remains the project/function-block source reference. Bible does not claim runtime importer/exporter behavior for this guide.
