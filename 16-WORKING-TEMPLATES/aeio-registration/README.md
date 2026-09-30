# AEIO registration skeleton

Status: **registration contract template**. Start from the current official `IO`/`FBIO` SDK sample because `AEIO_FunctionBlock` contains many version-specific callbacks.

```cpp
A_Err RegisterMyIO(
    AEGP_SuiteHandler& suites,
    AEGP_PluginID plugin_id,
    AEGP_IORefcon refcon,
    AEIO_ModuleInfo* module_info,
    AEIO_FunctionBlock4* funcs)
{
    // Fill module_info: signature, file type/description/capabilities.
    // Fill funcs: verify/init/info/frame/audio/output callbacks.
    return suites.RegisterSuite5()->AEGP_RegisterIO(
        plugin_id,
        refcon,
        module_info,
        funcs);
}
```

For optional operations where the current SDK permits it, return `AEIO_Err_USE_DFLT_CALLBACK` and let AE do its default processing.

Why this template does not fabricate the whole callback table: exact function-block revision and required callbacks are SDK-version-sensitive. A “complete” table copied from an old SDK is less useful than the current official `IO` sample.
