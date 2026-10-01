# AEIO registration working guide

Status: **registration contract guide / complete AEIO still requires the official IO/FBIO sample**.

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
    AEIO_ModuleInfo* module_info,
    AEIO_FunctionBlock4* funcs)
{
    return suites.RegisterSuite5()->AEGP_RegisterIO(
        plugin_id,
        refcon,
        module_info,
        funcs);
}
~~~

The concrete supplied-25.6 review uses AEIO_ModuleInfo and AEIO_FunctionBlock4. Recheck target headers.

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

## Testing milestone

Do not label the AEIO working until at least one meaningful format path passes:

- fresh import/export;
- deterministic frame data;
- repeated/random frame request;
- cancellation;
- malformed input/output failure;
- project save/reopen;
- cleanup/leak checks.

## Verification boundary

This guide preserves the registration contract without fabricating a stale full callback table. The exact SDK sample remains the project/function-block source of truth.
