# Artisan reference workspace

Status: **SDK sample workspace: Artie / host-test pending**.

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

## Failure behavior

Test:

- unsupported scene feature;
- resource allocation failure;
- cancellation;
- project close;
- renderer switch;
- repeated frames;
- shutdown.

A renderer failure must not corrupt the AE project.

## Verification boundary

The Bible deliberately does not provide a registrar stub and label it a renderer. This entry becomes an implementation only when a meaningful Artie-derived render path is compiled, loaded and validated with scene fixtures.
