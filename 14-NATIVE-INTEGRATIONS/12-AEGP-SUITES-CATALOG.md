# AEGP suites catalog — After Effects 26.5 snapshot

Это dated public-guide capability inventory, **не exact SDK26.5 header inventory**
и не runtime coverage. Точный compile-time contract всегда проверять в headers
того SDK, которым собирается plug-in. Таблица сохраняет guide headings: например,
EffectSuite4/KeyframeSuite3 ниже не заменяют reviewed SDK25.6 EffectSuite5/KeyframeSuite5.
Baseline/current-source distinctions: [function map](../17-NATIVE-SUITE-COOKBOOK/16-SUITE-FUNCTION-MAP.md)
и [legacy review](11-LEGACY-NATIVE.md). Later Guide2/ItemView2/Comp13/Stream7 notes
основаны на dated public documentation, не новой proprietary SDK26.5 сверке.

> **Важно:** номер suite в заголовке публичного guide не всегда равен «самому новому struct version в любых bindings». Для AE 26.5 официально подтверждены как новые `GuideSuite2`, `ItemViewSuite2`, `CompSuite13`, `StreamSuite7`. Остальные version-sensitive номера проверяются в headers конкретного SDK. См. [`13-DOCS-ERRATA.md`](13-DOCS-ERRATA.md).

| Suite | Public-guide heading / dated note | Что контролирует |
|---|---:|---|
| Memory | `AEGP_MemorySuite1` | host-managed memory handles |
| Command | `AEGP_CommandSuite1` | menu commands |
| Register | `AEGP_RegisterSuite5` | hooks, AEIO, Artisan, idle/death registration |
| Project | `AEGP_ProjSuite6` | project lifecycle/data |
| Time Display | `AEGP_TimeDisplay2` | time display settings |
| Item | `AEGP_ItemSuite9` | project items |
| Guide | `AEGP_GuideSuite2` | guides; 26.5 current generation |
| Item View | `AEGP_ItemViewSuite2` | guide visibility/snap/lock per view |
| Collection | `AEGP_CollectionSuite2` | selection/collections |
| Composition | `AEGP_CompSuite13` | comps, solids, current 26.5 parametric mesh creation |
| Footage | `AEGP_FootageSuite5` | footage/import interpretation |
| Layer | `AEGP_LayerSuite9` | layers and layer timing/object type |
| Effect | `AEGP_EffectSuite4` | effects on layers + generic calls |
| Stream | `AEGP_StreamSuite7` | property/effect streams; 26.5 render-stage control for layer param |
| Dynamic Stream | `AEGP_DynamicStreamSuite4` | dynamic stream hierarchy |
| Keyframe | `AEGP_KeyframeSuite3` | keyframes/interpolation/ease |
| Marker | `AEGP_MarkerSuite2` | markers |
| Mask | `AEGP_MaskSuite6` | masks |
| Mask Outline | `AEGP_MaskOutlineSuite3` | mask path geometry/feather data |
| Text Document | `AEGP_TextDocumentSuite1` | text document data |
| Text Layer | `AEGP_TextLayerSuite1` | text outlines |
| Utility | `AEGP_UtilitySuite6` | undo, reporting, scripting, registration helpers |
| Persistent Data | `AEGP_PersistentDataSuite4` | AE preferences/persistent plug-in data |
| Color Settings | `AEGP_ColorSettingsSuite5` | project/AE color management info |
| Render Options | `AEGP_RenderOptionsSuite4` | render option objects |
| Layer Render Options | `AEGP_LayerRenderOptionsSuite1` | layer-specific render options |
| Render | `AEGP_RenderSuite4` | request/render frames/audio |
| World | `AEGP_WorldSuite3` | allocate/query image worlds |
| Composite | `AEGP_CompositeSuite2` | host compositing/transfer/matte operations |
| Sound Data | `AEGP_SoundDataSuite1` | audio data |
| Render Queue | `AEGP_RenderQueueSuite1` | queue-level operations |
| Render Queue Item | `AEGP_RQItemSuite4` | render queue items |
| Render Queue Monitor | `AEGP_RenderQueueMonitorSuite1` | render queue monitoring callbacks/data |
| Output Module | `AEGP_OutputModuleSuite4` | output modules |
| PF Interface | `AEGP_PFInterfaceSuite1` | bridge used by effects into AEGP world |
| Iterate | `AEGP_IterateSuite1` | host parallel iteration for AEGP workloads |
| File Import Manager | `AEGP_FIMSuite3` | file/project importer registration |

## Capability groups

### Project graph
`Proj` → `Item` → `Comp` → `Layer` → `Stream` / `DynamicStream`.

### Animation
`Stream` + `Keyframe` + `Marker` + `Mask` + `Text`.

### Effects
`EffectSuite4` finds/adds/removes effects and can issue generic calls to prepared Effect plug-ins.

### Render
`RenderOptions` + `LayerRenderOptions` + `RenderSuite` + `World` + `Composite` + `SoundData`.

### Delivery
`RenderQueue` + `RQItem` + `OutputModule` + `RenderQueueMonitor`.

### Host integration
`Command` + `Register` + `Utility` + `PersistentData` + panel APIs.

## Suite acquisition rule

Do not encode “suite version 7 exists everywhere” into product logic. Acquire with
the exact suite-name/public-version macros. An older fallback needs its own typed
table and explicit semantic limits; never cast a table. Required-suite absence
fails before mutation. This index promises neither a standalone implementation nor
availability of every listed capability in the SDK25.6 baseline or an installed host.
