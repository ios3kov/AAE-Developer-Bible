# Artisan registration skeleton

Status: **registration contract template**. Start from the current SDK `Artie` sample.

```cpp
A_Err RegisterMyArtisan(
    AEGP_SuiteHandler& suites,
    AEGP_PluginID plugin_id,
    void* refcon,
    PR_ArtisanEntryPoints* entry_points)
{
    return suites.RegisterSuite5()->AEGP_RegisterArtisan(
        /* api version */      ARTISAN_API_VERSION,
        /* plugin version */   MY_ARTISAN_VERSION,
        plugin_id,
        refcon,
        "com.myco.renderer",
        "My Renderer",
        entry_points);
}
```

`render_func` is the fundamental required behavior; other Artisan callbacks depend on the current `PR_ArtisanEntryPoints` contract.

Do not substitute guessed constants for `ARTISAN_API_VERSION`/your version. Use the exact definitions from the SDK headers/sample you compile against.
