# AEGP Suite function map — native capability index

**Purpose:** быстрый указатель «какая suite / какая функция нужна».  
**Not a header replacement:** exact types, optional arguments and version macros always come from the SDK headers used for the build.

Primary baseline is supplied SDK **25.6 build 61**. This is a selected capability
index, not a per-member availability matrix. Explicit 26.5 entries are later public
research, not review of supplied proprietary 26.5 headers or runtime coverage.

| Operation family | 25.6 explanatory baseline | Companion source choice |
|---|---|---|
| Project / item / comp / layer | ProjSuite6 / ItemSuite9 / CompSuite12 / LayerSuite9 | Same generations |
| Effect / stream / dynamic stream | EffectSuite5 / StreamSuite6 / DynamicStreamSuite4 | EffectSuite5 / StreamSuite6 for implemented subset |
| Keyframes / masks / text / markers / footage | KeyframeSuite5 / MaskSuite6 / MaskOutlineSuite3 / TextDocumentSuite1 / MarkerSuite3 / FootageSuite5 | KeyframeSuite5 batch; other families have contract/design routes |
| Frame / world | RenderOptionsSuite4 / RenderSuite5 / WorldSuite3 | RenderSuite4 receipt subset, borrowed options |
| Queue / item / output | RenderQueueSuite1 / RQItemSuite4 / OutputModuleSuite4 | RQItemSuite3 subset with named enum; other two same |

These are struct generations, **not numeric AcquireSuite versions**. Use the target
header's name/version macros. Exact source boundaries and implemented functions:
[recipe index](15-RECIPE-INDEX.md), [source guide](code/README.md),
[evidence](VERIFICATION.md). CompSuite13, StreamSuite7, GuideSuite2 and ItemViewSuite2
must not silently replace the 25.6 contracts. Other families below require checking
their specific target declarations, not inference from this abbreviated table.

## Host / registration

### Memory Suite
Core:
- allocate/resize/free host memory handle;
- lock/unlock host memory;
- query size.

Use for memory handles returned by host APIs. Never `free()` an `AEGP_MemHandle`.

### Command Suite
Core:
- `AEGP_GetUniqueCommand`
- `AEGP_InsertMenuCommand`
- `AEGP_RemoveMenuCommand`
- `AEGP_EnableCommand`
- `AEGP_DisableCommand`
- `AEGP_CheckMarkMenuCommand`
- rename/set menu command name where available.

### Register Suite
Core registration families:
- command hook;
- update-menu hook;
- death hook;
- idle hook;
- AEIO registration;
- Artisan / Interactive Artisan registration;
- death/shutdown cleanup;
- other host hooks exposed by the target suite generation.

Register Suite is entry-point territory; most other suites are used later from callbacks.

---

## Project graph

### Project Suite
High-value:
- `AEGP_GetNumProjects`
- `AEGP_GetProjectByIndex`
- `AEGP_GetProjectRootFolder`
- project name/path access
- save project / save-as
- project dirty state
- project time display settings
- create/new project where host permits.

### Item Suite
High-value:
- `AEGP_GetFirstProjItem`
- `AEGP_GetNextProjItem`
- `AEGP_GetActiveItem`
- `AEGP_GetItemType`
- `AEGP_GetItemName`
- `AEGP_SetItemName`
- `AEGP_GetItemID`
- item flags / dimensions / duration / current time
- parent folder get/set
- `AEGP_CreateNewFolder`
- `AEGP_DeleteItem`
- label/proxy/comment-related access where exposed.

### Collection Suite
Use for host selection/collections:
- create/dispose collection;
- get number of collection items;
- inspect collection item type/union;
- append/set collection;
- query current selection via comp/project APIs that return collections.

### Composition Suite
High-value:
- `AEGP_GetCompFromItem`
- `AEGP_GetItemFromComp`
- comp background / flags / frame rate / work area / shutter
- `AEGP_CreateComp`
- `AEGP_CreateSolidInComp`
- `AEGP_CreateCameraInComp`
- `AEGP_CreateLightInComp`
- text/box-text creation
- vector/null creation where available
- comp marker stream
- selection collection
- AE 26.5: `AEGP_CreateParametricMeshLayerInComp`.

### Footage Suite
High-value families:
- create/new footage from path/solid;
- add footage to project;
- dispose footage not adopted by project;
- replace/relink footage;
- proxy get/set;
- interpretation options;
- solid color/dimensions;
- footage sound format.

---

## Layers / effects / property graph

### Layer Suite
High-value:
- `AEGP_GetCompNumLayers`
- `AEGP_GetCompLayerByIndex`
- active layer
- source item / parent comp
- layer name / quality / flags
- in point / duration / offset / stretch
- transfer mode
- `AEGP_IsAddLayerValid`
- `AEGP_AddLayer`
- `AEGP_ReorderLayer`
- layer bounds / object type / 2D/3D
- time conversion comp↔layer
- `AEGP_GetLayerID`
- `AEGP_GetLayerFromLayerID`
- set parent
- `AEGP_DeleteLayer`
- `AEGP_DuplicateLayer`
- track matte get/set/remove
- layer label/sampling quality.

### Effect Suite
High-value:
- `AEGP_GetLayerNumEffects`
- `AEGP_GetLayerEffectByIndex`
- `AEGP_GetInstalledKeyFromLayerEffect`
- effect parameter metadata
- flags
- reorder
- `AEGP_ApplyEffect`
- `AEGP_DeleteLayerEffect`
- `AEGP_DuplicateEffect`
- enumerate installed effects
- `AEGP_GetEffectName`
- `AEGP_GetEffectMatchName`
- effect category
- `AEGP_EffectCallGeneric`
- `AEGP_DisposeEffect`.

### Stream Suite
High-value:
- `AEGP_IsStreamLegal`
- `AEGP_CanVaryOverTime`
- valid interpolations
- `AEGP_GetNewLayerStream`
- `AEGP_GetEffectNumParamStreams`
- `AEGP_GetNewEffectStreamByIndex`
- `AEGP_GetNewMaskStream`
- `AEGP_DisposeStream`
- stream name / units / properties / type
- `AEGP_IsStreamTimevarying`
- `AEGP_GetNewStreamValue`
- `AEGP_DisposeStreamValue`
- `AEGP_SetStreamValue`
- expression get/set/enable
- duplicate stream ref
- unique stream ID in newer generations
- AE 26.5 StreamSuite7: layer-param render-stage accessors.

### Dynamic Stream Suite
High-value:
- get grouping type / dynamic flags;
- number of children in group;
- `AEGP_GetNewStreamRefByIndex`
- `AEGP_GetNewStreamRefByMatchname`
- parent stream ref;
- match name;
- add/delete/reorder/duplicate child stream;
- set stream name;
- separation/follower operations where supported.

Structural edit → old child refs should be treated as invalid and re-queried.

---

## Animation

### Keyframe Suite
High-value:
- `AEGP_GetStreamNumKFs`
- `AEGP_GetKeyframeTime`
- `AEGP_InsertKeyframe`
- `AEGP_DeleteKeyframe`
- get/set keyframe value
- get/set interpolation
- temporal ease
- spatial tangents
- keyframe flags
- `AEGP_StartAddKeyframes`
- `AEGP_AddKeyframes`
- `AEGP_SetAddKeyframe`
- `AEGP_EndAddKeyframes`.

### Marker Suite
High-value:
- `AEGP_NewMarker`
- `AEGP_DisposeMarker`
- `AEGP_DuplicateMarker`
- marker flags;
- marker strings (comment/chapter/url/cue);
- cue-point params;
- marker duration.

### Mask Suite
High-value:
- `AEGP_GetLayerNumMasks`
- `AEGP_GetLayerMaskByIndex`
- `AEGP_DisposeMask`
- invert/mode/motion blur/feather falloff
- `AEGP_GetMaskID`
- `AEGP_CreateNewMask`
- `AEGP_DeleteMaskFromLayer`
- mask color / lock / roto-bezier
- duplicate mask.

### Mask Outline Suite
High-value:
- open/closed state;
- number of segments;
- get/set vertex info;
- create/delete vertices;
- feather count/data.

Mask geometry normally arrives through outline stream value, then Mask Outline Suite edits its structure.

### Text Document Suite
Core:
- `AEGP_GetNewText`
- `AEGP_SetText`.

### Text Layer Suite
Core families:
- request text outlines at time;
- count outlines;
- get indexed outline/path;
- dispose outline collection according to suite contract.

---

## Utility / preferences / color

### Utility Suite
High-value:
- `AEGP_ReportInfo`
- `AEGP_ReportInfoUnicode`
- driver/spec version
- quiet errors begin/end
- `AEGP_StartUndoGroup`
- `AEGP_EndUndoGroup`
- `AEGP_RegisterWithAEGP`
- main host window access where platform-relevant
- idle triggering
- scripting availability
- `AEGP_ExecuteScript`
- debug log / OS console helpers
- last-error access.

### Persistent Data Suite
Families:
- section/key existence;
- get/set typed values;
- strings;
- blobs/data;
- delete key/section where available.

Use for preferences, not live host handles.

### Color Settings Suite
Families:
- working space / project color settings;
- color profile descriptions/transforms;
- OCIO-related queries in newer generations.

Color API is version-sensitive: acquire the generation you actually require.

---

## Render / pixels / audio

### Render Options Suite
High-value:
- create render options from item;
- duplicate/dispose;
- time;
- time step;
- field render;
- world/pixel type;
- downsample factor;
- ROI/matte/channel related options where exposed.

### Layer Render Options Suite
Families:
- create from layer / upstream of effect;
- time/time step;
- world type;
- downsample;
- matte mode;
- duplicate/dispose.

### Render Suite
High-value:
- `AEGP_RenderAndCheckoutFrame`
- `AEGP_RenderAndCheckoutLayerFrame`
- `AEGP_CheckinFrame`
- `AEGP_GetReceiptWorld`
- `AEGP_GetRenderedRegion`
- rendered-frame sufficiency
- timestamp/change tests
- item sound render.

### World Suite
Families:
- create/dispose world;
- world type;
- dimensions;
- rowbytes;
- base address 8/16/float;
- convert effect world ↔ AEGP world where supported.

### Composite Suite
Families:
- copy/blit;
- transfer/composite;
- matte operations;
- transform/composite host helpers.

### Sound Data Suite
Families:
- allocate/dispose/access sound data;
- lock/unlock samples;
- number of samples;
- sound format.

---

## Render Queue

### Render Queue Suite
- `AEGP_AddCompToRenderQueue`
- `AEGP_SetRenderQueueState`
- `AEGP_GetRenderQueueState`.

### RQ Item Suite
High-value:
- `AEGP_GetNumRQItems`
- `AEGP_GetRQItemByIndex`
- `AEGP_GetNextRQItem`
- output module count;
- render enable state;
- started/elapsed time;
- log type;
- remove output module;
- comment;
- comp from RQ item;
- `AEGP_DeleteRQItem`.

### Render Queue Monitor Suite
Callback/listener families:
- register listener;
- job started/ended;
- item started/updated/ended;
- frame events;
- query job/item/frame/output-module properties;
- thumbnails.

### Output Module Suite
High-value:
- `AEGP_GetOutputModuleByIndex`
- embedding options;
- post-render action;
- enabled video/audio;
- output channels;
- stretch;
- crop;
- sound format;
- `AEGP_GetOutputFilePath`
- `AEGP_SetOutputFilePath`
- `AEGP_AddDefaultOutputModule`
- extra output module info.

---

## Effect ↔ AEGP bridge / parallel work / import

### PF Interface Suite
For Effect plug-ins:
- `AEGP_GetEffectLayer`
- `AEGP_GetNewEffectForEffect`
- effect-time → comp-time conversion
- effect camera
- camera matrix/context.

### Iterate Suite
Host-assisted parallel iteration for AEGP workloads. Use only callbacks that obey the suite's thread-safety contract; do not mutate project state from worker iterations.

### File Import Manager Suite
Registration/callback surface for file/project importers. This is not the same as simply importing ordinary footage via Footage Suite.

---

## AE 26.5 UI guide APIs

### Guide Suite2
Families:
- enumerate/read guides;
- add/update/delete;
- orientation;
- pixel/percentage position;
- color;
- edge pinning.

### Item View Suite2
- playback/current view time;
- guides visible;
- guides snap;
- guides locked.

---

## Как этим пользоваться

1. Найти operation здесь.
2. Перейти в recipe в `17-NATIVE-SUITE-COOKBOOK/`.
3. Для exact signature открыть header целевого SDK: baseline Bible — 25.6;
   later feature требует своего version/source gate, не автоматического перехода на 26.5.
4. Для lifecycle посмотреть ближайший официальный Adobe sample.
5. Добавить ownership + invalidation + undo.
6. Только потом писать business logic.

---

## Полный список функций конкретного SDK

Этот файл — human-oriented capability map, а не попытка вручную продублировать все headers. Для **полного exact inventory Suite → every function → signature** используйте `18-SDK-HEADER-TOOLS/tools/ae_sdk_inventory.py` на той версии Adobe SDK, которой реально собирается проект.
