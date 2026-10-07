# Artisan — custom composition 3D renderer

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Core API:** `PR_ArtisanEntryPoints`, `AEGP_RegisterArtisan` / `AEGP_RegisterInteractiveArtisan`, `AEGP_CanvasSuite8`, `AEGP_ArtisanUtilSuite1` plus camera/light/layer/world suites.
**Evidence level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED.

Artisan — это не «GPU effect» и не callback, который получает один layer image. Artisan регистрируется как **renderer implementation для 3D composition rendering path** и через render context запрашивает scene information у After Effects.

## Exact Artie sample reading walkthrough

SDK 25.6 `Examples/AEGP/Artie/Artie.cpp`: registration table → `Artie_GlobalSetup`
(360)/GlobalSetdown (348) → SetupInstance (373)/SetdownInstance (388) →
FlattenInstance (294) → FrameSetup (324)/FrameSetdown (308) → render paths.
`AEGP_GetCompRenderTime` occurs at 434, layer-context iteration near 918–930,
own render-world dispose near 899. Names are more robust than line numbers for
another distribution. Sample uses CanvasSuite5/WorldSuite2 in these locations;
current chapter contract is CanvasSuite8, не cast старых structs.

Scene route: borrowed render context → query comp/time/ROI/layer contexts → copy
permitted geometry/material/camera/light data into normalized own scene → renderer
work → output by exact host contract → release own textures/worlds/receipts →
frame teardown. Borrowed contexts не отправлять worker после завершения request.
Unknown layer type/feature имеет explicit reject/delegate/fallback policy; не
выдавать чёрный output как correctness support. Cache key включает scene/time/
quality dependencies, не context pointer.

Persistence хранит versioned instance settings, не live device/scene pointers.
Partial init и cancellation проходят ту же таблицу owned resources; main/render
thread permission определяется exact callback/suite, не C++ class lifetime.
Artie shortcuts не становятся production ray tracer или complete scene-coverage
guarantee. [Deep contract](../14-NATIVE-INTEGRATIONS/09-ARTISAN.md) и reference
workspace остаются linked layers одной темы. Runtime renderer не заявлен.

## 1. Когда Artisan вообще нужен

Рассматривайте Artisan, если продукт должен:

- стать selectable renderer для 3D composition;
- интерпретировать камеры/свет/3D layers в рамках composition render context;
- управлять rendering/compositing path на уровне scene, а не одного effect input;
- поддерживать interactive renderer behavior, если это действительно часть продукта.

Не выбирайте Artisan только потому, что:

- эффект использует 3D math;
- нужно отрендерить собственный mesh внутри одного эффекта;
- нужен GPU;
- нужен overlay/viewport tool;
- нужно ускорить обычный render queue.

## 2. Почему API большой

`PR_Public.h` прямо говорит: Artisan получает opaque global/instance/render/query contexts и должен запрашивать остальные rendering parameters через AEGP suites.

То есть архитектура примерно:

```text
PR_RenderContextH
→ Canvas Suite: comp/time/ROI/layer contexts/textures
→ Camera/Light/Layer/Stream suites: scene attributes
→ собственная scene representation
→ renderer core
→ output/interactive buffer по host contract
```

Это renderer integration, а не замена всего AE project/render engine.

## 3. Registration

AEGP initializer задаёт:

- Artisan API version;
- product/artisan version;
- plugin id/refcon;
- UTF-8 match name;
- display name;
- `PR_ArtisanEntryPoints`.

```cpp
A_Version api{PR_ARTISAN_API_VERSION_MAJOR, PR_ARTISAN_API_VERSION_MINOR};
PR_ArtisanEntryPoints ep{};
ep.render_func = Render; // единственный обязательный entry point по sample/header

ERR(suites.RegisterSuite5()->AEGP_RegisterArtisan(
    api, artisan_version, plugin_id, refcon,
    match_name, display_name, &ep));
```

Header также имеет `AEGP_RegisterInteractiveArtisan`; это отдельный registration path, не flag у обычного effect.

## 4. Entry-point lifecycle

`PR_ArtisanEntryPoints` включает:

```text
global_setup / global_setdown / about
instance_setup / instance_setdown / flatten_instance / instance_dialog
frame_setup
render                 ← обязательный
frame_setdown
query
```

Header comments задают три уровня state:

- **global data** — общий для всех instances renderer type;
- **instance data** — instance Artisan, ассоциированный с comp;
- **render data** — frame/render-local state.

Plugin обязан освобождать свои GlobalData/InstanceData/RenderData в соответствующих setdown callbacks.

## 5. Flatten instance data

`PR_FlattenInstanceFunc` нужен для disk/copy representation instance state. Header прямо требует platform-independent flattened data и говорит не разрушать source instance handle.

Если renderer имеет user parameters/state и не реализует корректную flatten/inflate/setup-instance model, save/reopen/copy comp может стать несовместимым даже если текущий render работает.

## 6. Query callback — часть interaction semantics

`PR_QueryFunc` может вызываться после instance setup. Query types включают transform и interactive-window operations.

Header объясняет, что AE использует query information для geometry transforms/handles/mouse manipulation. Поэтому query callback нельзя рассматривать как необязательный performance hint, если renderer обещает corresponding interactive behavior.

## 7. CanvasSuite8 — scene/render context API baseline 25.6

Supplied SDK объявляет `AEGP_CanvasSuite8`, version macro 14. Он даёт renderer-у, среди прочего:

- comp/time/downsample/ROI;
- destination buffer;
- число layers to render и layer contexts;
- render opacity;
- texture/layer rendering;
- track matte context;
- render receipts/cache checks;
- bins;
- layer→world transforms;
- interactive viewport/buffer information;
- display channel/exposure/color transform;
- comp shutter and time mapping.

Старый `Artie.cpp` использует **CanvasSuite5**, LayerSuite5, ItemSuite6, StreamSuite2. Это официальный исторический sample pattern, но не current-suite signature baseline 25.6.

## 8. Textures and worlds имеют paired cleanup

Current Canvas Suite comments различают:

- textures, которые нужно освобождать через `AEGP_DisposeTexture`;
- worlds/render buffers, которые для отдельных calls должны освобождаться через World Suite;
- render receipts, которые нужно `AEGP_DisposeRenderReceipt`.

Не создавайте один generic deleter «для всего, что пришло из Canvas». Тип результата определяет paired cleanup API.

Artie sample явно вызывает `AEGP_DisposeTexture` для polygon texture и собственные scene/camera cleanup paths.

## 9. Scene enumeration

Artie показывает типичный pattern:

```text
GetNumLayersToRender
→ GetNthLayerContextToRender
→ resolve LayerH/context
→ read layer/camera/light properties at comp render time
→ optionally RenderTexture
→ build own scene
→ render
```

Но сам sample ограничивает число polygons и реализует учебный raytracer. Он **не является best-case 3D renderer**; Xcode project comment прямо предупреждает использовать sample как skeleton, а не эталон качества.

## 10. Camera and time

Artie получает comp render time/downsample/ROI через Canvas Suite и camera через Camera Suite. Он не использует current-time UI cursor как render time.

Это важный architecture rule: Artisan scene evaluation должен быть привязан к `PR_RenderContextH`, а не к глобальному project/UI state.

## 11. Layer source dimensions are not universal geometry

Старый Artie helper пытается получить source item dimensions и сам содержит комментарий, что это **не работает для text layer**, предлагая render-layer bounds/context APIs.

Это хороший пример ограничения sample-derived shortcut. Production renderer должен строить geometry from render context semantics, а не предполагать, что у каждого 3D layer есть обычный source item с raster dimensions.

## 12. RenderTexture не означает «обойти AE effects»

`AEGP_RenderTexture` / related Canvas calls позволяют Artisan попросить AE подготовить layer texture в текущем render context. Это **кооперация с host**, а не собственное исполнение arbitrary AE effects/plugins.

Если цель — написать отдельный renderer, который полностью заменит AE evaluation всего graph, наличие Artisan API этого не доказывает.

## 13. Interactive Artisan

Canvas Suite содержит interactive window/buffer/viewport/checkerboard/display-channel/exposure APIs; Register Suite имеет `AEGP_RegisterInteractiveArtisan`.

Interactive path увеличивает scope:

- window/context lifetime;
- resize/viewport transforms;
- cached/interactive buffers;
- display modes/exposure/color transform;
- mouse/line-drawing query behavior;
- final vs interactive quality consistency.

Не заявляйте interactive support только потому, что обычный Artisan render callback работает.

## 14. Error/resource strategy

Renderer state должен иметь чёткий ownership по слоям:

```text
process-global registration state
≠ PR_GlobalDataH
≠ PR_InstanceDataH
≠ PR_RenderDataH
≠ temporary AEGP texture/world/receipt
```

Primary render error не должен скрываться cleanup error-ом, но cleanup должен выполняться на partial scene/camera/texture construction.

Любой callback crossing C ABI должен возвращать `A_Err`, а не пропускать C++ exception наружу.

## 15. Performance

Artisan имеет смысл только после correctness. Отдельно измеряйте:

- scene extraction;
- texture requests into AE;
- acceleration structure build;
- shading/raster/raytrace core;
- compositing/writeback;
- interactive cache reuse.

Глобальный mutex может сделать renderer менее race-prone ценой полного уничтожения scaling, но сам по себе не доказывает корректную host/thread architecture. Product runtime claims require product-specific evidence.

## 16. Production state machine

A renderer should model state explicitly:

~~~text
registration/module state
→ PR_GlobalDataH
→ PR_InstanceDataH
→ PR_RenderDataH
→ temporary Canvas/World/Texture/Receipt resources
~~~

### Registration/module state

Long-lived product services such as logging, immutable tables, backend/device registries and shared caches with explicit shutdown.

### GlobalData

Renderer-type state shared across instances where the contract permits it.

### InstanceData

Composition/renderer-instance state: renderer settings, scene policy and persistent configuration.

### RenderData

Frame/render-local state: extracted scene, temporary acceleration structures and render scratch.

Borrowed host contexts such as PR_RenderContextH are not persistent product identity.

## 17. Persistence and flatten/inflate

If renderer instance has persistent settings:

~~~text
live InstanceData
→ FlattenInstance
→ versioned platform-independent bytes
→ project/save/copy
→ InstanceSetup
→ validate/migrate
→ reconstruct live InstanceData
~~~

Do not serialize raw pointers, AEGP refs, function-table pointers, GPU handles, mutexes, file descriptors or compiler-dependent object layout.

Flat data should include schema version and size. Unknown/corrupt versions need explicit recovery policy.

## 18. Scene extraction boundary

Keep host scene extraction separate from renderer core:

~~~text
PR_RenderContextH
→ Canvas/Camera/Light/Layer/Stream queries
→ normalized product scene
→ renderer core
→ output/writeback
~~~

This reduces host calls in hot loops and keeps borrowed host refs out of long-lived renderer state.

## 19. Layer/context identity

Layer context is render-context-specific. Do not use layer index, source-item dimensions or prior-frame context pointers as permanent identity.

If a cache needs identity, build a key from supported host identities plus render time/context/version inputs.

## 20. Track mattes and bins

Canvas exposes track-matte contexts and render bins, so production rendering cannot blindly reduce the host scene to one linear independent-layer vector.

Define product policy for track mattes, 2D/3D mixing, transparency, precomps and unsupported compositing cases.

Unsupported material scene behavior should fail/fallback explicitly rather than silently render a plausible but wrong frame.

## 21. Texture acquisition policy

Decide what a requested texture represents:

- host-rendered layer appearance;
- source-like surface for renderer shading;
- matte input;
- cacheable intermediate.

Do not assume every layer should become one texture.

Track texture, world and receipt cleanup obligations independently.

## 22. Render receipts and cache identity

Receipt is host cache evidence, not pixels.

Separate host receipt validity from product scene-cache validity and backend/device state.

Do not serialize receipts or reuse product acceleration structures merely because one host texture receipt remains valid.

## 23. Camera and light extraction

Evaluate camera, lights and layer transforms at render-context time, not UI current time.

If no camera exists, define explicit product behavior rather than inventing arbitrary projection.

## 24. Motion blur and shutter

If product claims motion blur, shutter/time sampling must be part of scene evaluation and cache identity.

Do not read transforms only at center time and call the result motion-blur support.

## 25. ROI and downsample

Respect render-context ROI/downsample. Do not assume full composition, 1:1 scale or zero origin.

## 26. Interactive renderer state

Interactive registration adds a separate view/display lifetime:

~~~text
final renderer state
≠ interactive viewport/view state
~~~

Interactive state may include viewport transforms, display channel, exposure, checkerboard/background and transient buffers.

Do not persist transient view handles inside instance data.

## 27. Query callback policy

Answer only documented query types the renderer supports.

Unsupported queries should use the appropriate unsupported/default behavior rather than fabricated transforms.

## 28. Cancellation

On cancellation:

~~~text
stop new work
→ release temporary textures/worlds/receipts
→ drop render-local caches
→ preserve global/instance state
→ return cancel/error
~~~

Do not destroy persistent renderer settings because one frame was cancelled.

## 29. Partial failure cleanup

A render may fail after camera acquisition, multiple texture checkouts and partial acceleration-structure construction.

Cleanup must release every acquired host resource and product temporary. Preserve primary render error over cleanup failures.

## 30. Unsupported scene-feature policy

Before implementation classify each feature:

| Feature | Policy |
|---|---|
| camera | supported / required / fallback |
| lights | supported / ignored / unsupported |
| text/shape | host texture / native geometry / unsupported |
| precomp | host texture / recursive handling / unsupported |
| track matte | supported / explicit limitation |
| blending | supported subset / host-assisted / unsupported |
| motion blur | supported / unsupported |
| effects | host texture path / unsupported custom path |
| 2D layers | included / host-composited / unsupported |

Never silently omit a feature that materially changes output.

## 31. Threading and external renderer cores

Do not infer Effect MFR rules.

For worker/GPU/external renderer paths:

- keep host refs/contexts on documented paths;
- copy/normalize pure data before background work;
- define cancellation and backend/device lifetime;
- avoid product mutex across opaque host calls.

## 32. Performance architecture

Measure separately:

- host scene enumeration;
- property evaluation;
- texture acquisition;
- geometry conversion;
- acceleration structure build/refit;
- renderer core;
- compositing/writeback;
- cache lookup;
- interactive reuse.

A fast shading core can still lose to expensive scene extraction.

## 33. Product validation guidance

If a concrete Artisan product claims these capabilities, useful runtime cases include:

- registration/selectability;
- no-camera and explicit-camera scenes;
- 2D + 3D mixed layers;
- footage/text/shape/precomp;
- cameras/lights;
- track mattes;
- effects through intended texture path;
- transparency/blending;
- motion blur/shutter;
- ROI/downsample;
- supported bit depth/color behavior;
- save/reopen/duplicate comp;
- instance flatten/migration;
- repeated frame/context teardown;
- cancellation/error cleanup;
- renderer switching;
- interactive/final parity if claimed;
- performance/memory profiling.

These establish product support evidence. Bible remains SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED unless a separate runtime record exists.

## 34. Production workflow

~~~text
define supported scene semantics
→ use exact Artie sample as lifecycle skeleton
→ define Global/Instance/Render state
→ implement versioned instance persistence
→ normalize one simple scene from RenderContext
→ render deterministic output
→ add textures/mattes/camera/lights deliberately
→ add cancellation/failure cleanup
→ add interactive path only if needed
→ profile/cache after correctness
~~~

Do not replace every Artie subsystem at once.

## Related chapters

- [Artisan native integration](../14-NATIVE-INTEGRATIONS/09-ARTISAN.md)
- [Lifetime / threading](../17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md)
- [Performance architecture](../01-ARCHITECTURE/05-PERFORMANCE-ARCHITECTURE.md)
- [Memory / persistence](../17-NATIVE-SUITE-COOKBOOK/12-MEMORY-UNDO-PERSISTENCE.md)
- [Testing](../10-TESTING/README.md)

## Source record

[AEIO/Artisan SDK 25.6 review](../18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).
