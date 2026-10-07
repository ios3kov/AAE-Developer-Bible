# Artisan reference workspace

Status: **Artie sample-derived workspace plan / RUNTIME-NOT-CLAIMED**.

Artisan replaces/customizes parts of After Effects 3D rendering and carries a substantially larger host contract than a normal effect.

Use the exact Artie sample from the target SDK as the project and registration shell.

## Source of truth

Read:

- 05-ARTISAN/README.md;
- 14-NATIVE-INTEGRATIONS/09-ARTISAN.md;
- 18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md;
- target SDK Artie sample and headers.

The supplied 25.6 review covers PR_ArtisanEntryPoints, CanvasSuite8 and the global/instance/frame state model. Recheck generations in the shipping SDK.

## Development sequence

Follow the [Artie reading route](../../../05-ARTISAN/README.md#exact-artie-sample-reading-walkthrough)
and [typed registration fragment](../../../16-WORKING-TEMPLATES/artisan-registration/README.md).
API/product versions are A_Version values. Lifecycle stubs do not provide persistent
instance settings. RegisterArtisan success followed by failed death-hook registration
is partial initialization, not automatic renderer unregistration.

~~~text
materialize Artie
→ build/load untouched
→ reproduce one sample render
→ preserve baseline
→ replace one scene/render subsystem
→ compare output
→ repeat
~~~

Do not delete sample lifecycle code before understanding which callbacks own which state.

## State layers

Document separately:

- global renderer state;
- renderer instance state;
- per-frame/per-render state;
- host-borrowed scene/canvas data;
- product caches.

A frame object must not accidentally outlive the host frame lifecycle.

## Scene handling

Before custom rendering define which host scene features are supported:

- cameras;
- lights;
- transforms;
- 3D layers;
- materials;
- transparency;
- motion blur;
- depth/intersections;
- text/vector layers;
- effects/precomps as exposed through the Artisan contract.

Unsupported scene features need explicit fallback/diagnostic behavior.

## Render correctness

Build small deterministic scenes:

- one camera/one object;
- depth ordering;
- transparency;
- moving camera/object;
- light variation;
- edge/crop cases.

Compare with the intended semantic reference. If the renderer intentionally differs from AE default rendering, document the expected difference rather than using visual similarity as the test.

## Threading/GPU

Do not infer renderer thread safety from Effect MFR rules; Artisan has its own callback/lifetime contract.

If external GPU/renderer work is used, keep host object access on documented paths and define cancellation/device teardown explicitly.

## Product failure-validation cases

If a concrete product claims recovery/support, useful cases include:

- unsupported scene feature;
- resource allocation failure;
- cancellation;
- project close;
- renderer switch;
- repeated frames;
- shutdown.

A renderer failure must not corrupt the AE project.

## Persistence/cache separation

When adapting Artie, separate:

- versioned instance settings;
- runtime scene cache;
- frame-local render data;
- interactive viewport state;
- backend/GPU resources.

Do not flatten runtime cache/backend handles into project data.

## Verification boundary

The Bible deliberately does not provide a registrar stub and label it a renderer. This is a source/workspace plan; runtime support belongs to a concrete product's evidence. Bible editorial completion does not require building the reference workspace.
