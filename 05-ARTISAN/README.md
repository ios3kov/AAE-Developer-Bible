# Artisan — custom composition 3D renderer

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Core API:** `PR_ArtisanEntryPoints`, `AEGP_RegisterArtisan` / `AEGP_RegisterInteractiveArtisan`, `AEGP_CanvasSuite8`, `AEGP_ArtisanUtilSuite1` plus camera/light/layer/world suites.
**Verification level:** SDK source-reviewed; no new Artisan build or host render in this editorial iteration.

Artisan — это не «GPU effect» и не callback, который получает один layer image. Artisan регистрируется как **renderer implementation для 3D composition rendering path** и через render context запрашивает scene information у After Effects.

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

Глобальный mutex может сделать renderer thread-safe ценой полного уничтожения scaling; threading model нужно доказать конкретными host tests, а не только inspection.

## 16. Acceptance matrix

- registration + renderer visible/selectable;
- comp without camera / explicit camera;
- 2D + 3D mixed layers;
- text/shape/precomp/footage layers;
- cameras/lights;
- track mattes;
- effects before texture/render;
- transparency/blending;
- motion blur/shutter;
- ROI/downsample;
- 8/16/32-bpc and color management as applicable;
- save/reopen/duplicate comp/instance flattening;
- repeated render/context teardown;
- cancellation/errors;
- interactive/final parity if interactive claimed;
- performance/memory profiling.

До этого Artisan chapter source-reviewed, а не host-verified.

## Source record

[AEIO/Artisan SDK 25.6 review](../18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).