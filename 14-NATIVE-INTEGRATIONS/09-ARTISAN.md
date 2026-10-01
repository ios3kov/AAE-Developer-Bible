# Artisan — registration, contexts and render contract

Обновлено **2026-10-01** по supplied Adobe After Effects SDK **25.6 build 61**.

Это contract-level companion к [Artisan chapter](../05-ARTISAN/README.md). Source review не является новой renderer implementation или host render.

## 1. Artisan is an AEGP-registered renderer

`PR_Public.h` прямо определяет plugin renderers as **artisans**: AEGP modules register with render manager at program startup. Entry points получают opaque context + plugin data; остальное renderer запрашивает через AEGP suites.

PiPL sample Artie имеет `Kind { AEGP }` и `EntryPointFunc`; registration происходит позже через Register Suite.

## 2. API version and registration identity

`PR_ARTISAN_API_VERSION_MAJOR=1`, minor=0 in supplied header.

`AEGP_RegisterArtisan` / `AEGP_RegisterInteractiveArtisan` принимают:

- API version;
- artisan/product version;
- AEGP plugin id;
- refcon;
- UTF-8 match name;
- display name;
- `PR_ArtisanEntryPoints`.

Match name — programmatic renderer identity; display name — user-visible name. Не локализуйте match name как UI text.

## 3. `PR_ArtisanEntryPoints` ownership/lifecycle map

| Callback | State level | Основная обязанность |
|---|---|---|
| GlobalSetup | renderer type | optional global data allocation |
| GlobalSetdown | renderer type | dispose plugin global data |
| InstanceSetup | comp/renderer instance | build instance data, optionally from flat data |
| InstanceSetdown | instance | dispose plugin instance data |
| FlattenInstance | persistence/copy | platform-independent flat representation |
| DoInstanceDialog | instance UI | mutate settings and report changed/no-change |
| FrameSetup | render/frame | allocate render data |
| Render | render/frame | main render — единственный mandatory slot |
| FrameSetdown | render/frame | dispose render data |
| Query | interaction/geometry | transforms/interactive queries |

Суффикс `0` в fields означает optional в Artie comment; `render_func` — mandatory.

## 4. Data handles are plugin-owned when header says so

`PR_GlobalDataH`, `PR_InstanceDataH`, `PR_RenderDataH` являются opaque PR handles for plugin-private data. Header comments у setdown callbacks говорят plugin должен dispose allocated data.

Не путать:

- PR plugin data handles;
- opaque context handles (`GlobalContextH`, `InstanceContextH`, `RenderContextH`, `QueryContextH`);
- AEGP MemorySuite handles;
- AEGP World/Texture/Receipt handles.

Каждая группа имеет свой lifetime.

## 5. Context conversion via ArtisanUtilSuite1

`AEGP_ArtisanUtilSuite1` позволяет получить:

- GlobalContext из InstanceContext;
- InstanceContext из RenderContext;
- InstanceContext из QueryContext;
- Global/Instance/Render data из соответствующих contexts.

Это bridge между callback context и plugin state. Он не делает context persistent beyond host-defined lifetime.

## 6. CanvasSuite8 is the render-context toolbox

Current SDK 25.6 declaration: `AEGP_CanvasSuite8`, macro version 14.

Ключевые categories:

```text
render context → comp/time/ROI/downsample
render context → layers-to-render + layer contexts
layer context → opacity/bounds/transforms/track matte
layer context → host-rendered texture/world
render → receipt/cache validation
interactive → viewport/window/buffers/display/exposure
```

В production code suite generation надо брать из target SDK; old Artie uses CanvasSuite5.

## 7. RenderTexture/RenderLayer ownership

Canvas functions возвращают разные resource kinds:

- texture — paired `AEGP_DisposeTexture`;
- WorldH from calls documented as owned — World Suite disposal;
- RenderReceiptH — `AEGP_DisposeRenderReceipt`.

`RenderTextureWithReceipt` может вернуть и receipt, и world. Caller обязан сохранить cleanup для обоих даже если subsequent scene build/render failed.

## 8. Receipts are cache evidence, not pixels

Render receipt позволяет сравнить, можно ли reuse previous layer render in changed/current context. `CheckRenderReceipt` принимает current render/layer contexts, old receipt, geometry-check flag и number of effects.

Это host cache identity mechanism. Receipt не является serializable image, world, или доказательством unchanged external state outside its contract.

## 9. Bins and renderer ordering

Canvas Suite имеет `GetNumBinsToRender`, `SetNthBin`, `GetBinType`. Это означает, что Artisan render order может включать host-defined bins/types; нельзя предполагать один linear список layers как полный compositing contract.

Artie sample builds a bounded list of layer contexts for its own educational scene, но это не доказательство, что все productions can flatten scene semantics в один vector without bin/track-matte/host rules.

## 10. Camera, light and layer evaluation use render time

Camera Suite receives render context/time; Canvas gives `GetCompRenderTime`; layer transforms/opacity should be evaluated in this render context.

Не используйте UI current time or cached transform from another frame.

## 11. Artie sample generation mismatch

Artie bundled with SDK 25.6 uses several older suites:

- CanvasSuite5 while current header has CanvasSuite8;
- LayerSuite5 vs current LayerSuite9;
- ItemSuite6 vs current ItemSuite9;
- StreamSuite2 vs current StreamSuite6.

Sample remains highly useful for renderer flow, but **current signatures and ownership comments come from current headers**.

Concrete sample caveat: `Artie_GetSourceLayerSize` itself notes source item dimensions do not work for text layer and suggests render-context bounds/downsample APIs. Bible keeps this as evidence against copying raster-source assumptions into all layer types.

## 12. Global/instance/frame callbacks in Artie are mostly skeleton stubs

Viewed Artie functions `GlobalSetup`, `GlobalSetdown`, `SetupInstance`, `SetdownInstance`, `FlattenInstance`, `FrameSetup`, `FrameSetdown`, `Query` mostly return success without real state.

Therefore Artie cannot be cited as proof of production persistence, instance options, frame-cache lifecycle or query implementation. Its main value is scene/render skeleton.

## 13. Artie registration source finding

At registration Artie sets:

`artisan_version.majorS = Artie_MAJOR_VERSION` and `artisan_version.minorS = Artie_MAJOR_VERSION`.

That may be intentional or a sample typo; source alone does not establish desired minor version. Bible records the literal source without silently correcting it.

## 14. Registration + DeathHook ordering

Artie calls RegisterArtisan and then RegisterDeathHook. Like other AEGP registrations, there is no basis here to assume generic rollback/unregister of already registered renderer on a later initialization failure.

A robust product should design partial-init state explicitly. If it claims recovery from such failures, that behavior needs product-specific runtime evidence.

## 15. Interactive registration is a separate contract

`AEGP_RegisterInteractiveArtisan` has the same parameter shape but interactive Canvas/query behavior adds separate runtime obligations.

Do not register the interactive variant unless the product actually implements the interactive callback/buffer/query contract. Runtime support claims require product-specific evidence.

## 16. Relation to independent render engine idea

Artisan can replace/render AE 3D composition behavior through supported render contexts. It still depends on host-provided scene/layer/effect texture services and AE project model.

Thus it may be a foundation for a custom 3D renderer, but **не является API, который автоматически позволяет независимо от AE быстро отрендерить произвольную composition со всеми native/third-party effects/expressions**.

That distinction matters for architecture decisions in the Bible.

## 17. Render-context ownership graph

A production implementation should make ownership visible:

~~~text
PR_RenderContextH              borrowed host context
  ↓
LayerContext / QueryContext    borrowed host contexts
  ↓
Canvas texture                 DisposeTexture
WorldH                         cleanup per call/World Suite contract
RenderReceiptH                 DisposeRenderReceipt
  ↓
normalized product scene       product-owned
  ↓
renderer/GPU resources         product-owned
~~~

Never attach borrowed render/query/layer context handles directly to long-lived product caches.

## 18. Instance persistence boundary

`FlattenInstance` should produce platform-independent state and leave the source live instance intact.

On setup from flat data:

- validate size/version;
- migrate known schemas;
- reject/recover malformed data deliberately;
- recreate runtime-only resources;
- never deserialize raw pointers or host refs.

## 19. Interactive/final separation

Interactive Canvas state is view/session state. Final render state is composition/render state.

Keep separate:

- viewport/display settings;
- interactive buffers;
- persistent renderer options;
- final frame scene/cache state.

Do not persist transient viewport handles inside instance data.

## 20. Verification boundary

Source review establishes entry-point/lifecycle/suite contracts. A developer calling a concrete Artisan implementation ready should additionally verify:

- actual registration/selectability;
- state save/reopen;
- scene correctness across layer kinds;
- effects/mattes/camera/light;
- resource cleanup/receipts;
- interactive behavior if claimed;
- performance and memory;
- crash/cancel/error paths.

## Source record

[AEIO/Artisan SDK 25.6 review](../18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).