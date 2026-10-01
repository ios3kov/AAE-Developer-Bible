# Artisan registration working guide

Status: **registration/source guide; SDK 25.6 contract-reviewed; runtime result not claimed**.

## Registration shape

Conceptually:

~~~cpp
A_Err RegisterMyArtisan(
    AEGP_SuiteHandler& suites,
    AEGP_PluginID plugin_id,
    void* refcon,
    PR_ArtisanEntryPoints* entry_points)
{
    return suites.RegisterSuite5()->AEGP_RegisterArtisan(
        ARTISAN_API_VERSION,
        MY_ARTISAN_VERSION,
        plugin_id,
        refcon,
        "com.myco.renderer",
        "My Renderer",
        entry_points);
}
~~~

Use exact constants/types from the SDK you compile. Do not invent API-version numbers.

## Why the Artie sample is required

Artisan has a large renderer lifecycle:

- registration;
- global renderer state;
- renderer instance;
- frame/render state;
- scene/canvas access;
- render callbacks;
- teardown.

A registrar that never renders a scene is not a reference renderer.

## First milestone

Keep the official Artie registration/function-table plumbing and make one minimal deterministic render path work unchanged.

Only then replace renderer behavior incrementally.

## Entry-point table

render_func is fundamental, but the real required/optional callback set is defined by the target PR_ArtisanEntryPoints contract.

Do not copy a function table from another SDK generation without checking layout/signatures.

## State ownership

Explicitly separate:

~~~text
global product renderer state
instance state
frame/render state
borrowed AE scene/canvas objects
product caches
~~~

Destroy in the reverse order of ownership and before host APIs disappear.

## Stable renderer identity

Use a stable renderer identifier distinct from the user-visible localized renderer name.

Changing identity can affect project/workspace compatibility and discovery.

## Feature scope

Before implementation list which scene features are supported.

For unsupported features define:

- fallback;
- explicit limitation;
- safe failure.

Do not silently render a materially wrong scene and call it success.

## Product validation milestone

If a concrete product claims renderer behavior, useful runtime cases include:

- renderer appears/selects;
- one simple scene renders;
- repeat same frame deterministically;
- camera transform change affects output;
- project save/reopen;
- renderer switch away/back;
- cancel;
- shutdown.

Expand fixtures as supported scene features grow.

## Persistence/state boundary

Registration source should make the state model visible:

~~~text
GlobalData
→ InstanceData
→ RenderData
~~~

If instance settings persist, define a versioned flat representation separately from live runtime resources.

Do not store Canvas/RenderContext pointers in persistent instance data.

## Resource cleanup boundary

A render path may acquire textures, worlds and receipts from different APIs. Track each cleanup obligation independently; a generic renderer-resource deleter is not enough.

## Verification boundary

This file documents the registration/startup/source boundary. It deliberately does not pretend a registrar stub is a complete Artisan, and Bible does not require host execution of this guide for editorial completion.
