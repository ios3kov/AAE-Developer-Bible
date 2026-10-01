# SDK 25.6: native panels и BlitHook

Дата: **2026-10-01**. Источник — присланный Adobe After Effects SDK **25.6 build 61**.

**Результат:** переписаны native panel и BlitHook chapters по current headers и bundled Panelator/EMP samples. Это source review/documentation; новые binaries и host display/UI tests не выполнялись.

## Source identity

Принятый SDK TAR SHA-256: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`.

| Файл | SHA-256 | Рассмотренные области |
|---|---|---|
| `Examples/Headers/AE_GeneralPlugPanels.h` | `3b1d4f1c019fee8d79646ffdd05c884673b6284caa89738fb91069518fc58303` | 1–140 Panel refs, callbacks, PanelSuite1 |
| `Examples/AEGP/Panelator/Panelator.cpp` | `188260a2987b9b7b4144dfbf8bbf98f1b32f367e7acfe2d13dcd9a2a4837895e` | 25–145 registration, menu/update/create hooks |
| `Examples/AEGP/Panelator/PanelatorUI.cpp` | `81df461cc4575738d29cf9212669b2a683b6f956f9bd9e5d9346ca8dc82cbd06` | 28–138 function table, snap/flyout/title |
| `Examples/AEGP/Panelator/Panelator_PiPL.r` | `e15d2cffae67bfeb2338df099b0de51eb217b1905e7f0a8a801f6c1112bc1d4b` | 6–35 AEGP PiPL |
| `Examples/AEGP/Panelator/Mac/PanelatorUI_Plat.cpp` | `e946eb41ce7c2d5834b294fafa1f049fa4fbb85ca5bea3337907843473d9de2c` | platform UI implementation |
| `Examples/AEGP/Panelator/Win/PanelatorUI_Plat.cpp` | `1c940392a7a832cf4e705005d960a6da81ed81c272ed22e8620d7a8f2e189fdb` | platform UI/window procedure |
| `Examples/Headers/AE_Hook.h` | `8e8af18a1eac85a3d53aac4e94e27549da4c46f286213405fd3d104977fbfcfc` | 34–147 hook version, pixel/view structs, hooks/entry |
| `Examples/GP/EMP/EMP.cpp` | `430578153a2d6fd2323546aa7bf75bae33eacefee570d647f6452a9c886695a7` | 32–73 sample blit/death/version/entry |
| `Examples/GP/EMP/EMP.h` | `8451d96ef990834c2abc077e3645f02f29de502c36046aa410fbde54d909dcb1` | 29–60 hook includes/export declaration |
| `Examples/GP/EMP/EMP_PiPL.r` | `3b669db40741e058631b224dc8c2fca0d93751ea1c2d3ebfc325566c51f88c1e` | 7–36 `Kind { AEGeneral }` |

## Native Panel contract

`AEGP_PanelSuite1`, suite version 1, frozen AE8.0. Platform view type in 64-bit macOS is `NSView*`; Windows is `HWND`.

`AEGP_RegisterCreatePanelHook` takes stable non-localized UTF-8 match name, create hook/refcon and background-paint choice. Create hook receives host container, `AEGP_PanelH`, output `AEGP_PanelFunctions1` and returns panel refcon.

`AEGP_PanelFunctions1` contains only GetSnapSizes, PopulateFlyout and DoFlyoutCommand. Native drawing/window events remain platform UI code.

`AEGP_UnRegisterCreatePanelHook` exists. `SetTitle`, `ToggleVisibility`, `IsShown` operate via match-name/panel identity; header explicitly separates non-localized match name from user-visible title.

Panelator integrates Window menu command with ToggleVisibility/IsShown and populates snap/flyout callbacks. It instantiates platform-specific UI implementation.

### Panelator lifetime finding

Reviewed `Panelator.cpp` allocates global `Panelator` with `new` and registers command/update/create hooks, but does not show a destructor/unregister/death-hook teardown path in that source. This is a source limitation, **not a measured leak/crash**. A concrete native-panel product should define create/destroy/unregister/shutdown behavior explicitly. The source review itself does not claim those runtime results.

### Identity recommendation

Panelator sets match name from sample string-table name while header says match name must not be localized. Source does not establish that this table varies by locale; Bible therefore records a design recommendation, not a sample bug: use separate stable programmatic match ID and localized display title.

## BlitHook contract

`AE_Hook.h`: protocol major 3/minor 0; plugin type literal `AE_HOOK_PLUGIN_TYPE='AEgp'`. Bundled EMP PiPL uses `Kind { AEGeneral }`, not AEGP.

`AE_HookPluginEntryFunc` receives version, file/resource specs and `AE_Hooks*`; hook table includes refcon, death/version hooks, host `SPBasicSuite*`, blit and cursor hooks.

`AE_PixBuffer`: width/height, depth 32/64/128, ARGB/BGRA pixel format, row bytes, channel bytes, plane bytes, pixels pointer. Header says Mac ARGB/Windows BGRA 'for now'; Bible preserves it as versioned source statement.

`AE_ViewCoordinates` separates full frame size, buffer origin and visible view rectangle.

`AE_BlitHook` receives nullable pixel buffer (NULL means blank frame), view coordinates, receipt, optional completion callback, input flags and output flags.

`AE_BlitOutFlag_ASYNCHRONOUS` exists, but supplied EMP sample does not exercise it. Therefore no async pixel-pointer lifetime or completion timing is invented by the Bible without additional source/host evidence.

EMP sample MyBlit returns success with no pixel work; death is a cleanup comment; version returns 1. It proves skeleton shape only.

## Verification boundaries

| Check | Status |
|---|---|
| Header/sample source review | DONE |
| Documentation rewrite | DONE |
| New exact-SDK compile | NOT RUN |
| Native panel registration/dock/reopen | NOT RUN |
| Panel shutdown/unregister/failure injection | NOT RUN |
| BlitHook display callback | NOT RUN |
| Async BlitHook behavior | NOT RUN |
| Preview performance/backpressure | NOT RUN |
| macOS/Windows host matrix | NOT RUN |

Next editorial work can cover shared PICA suite providers and legacy/native boundaries; runtime/product evidence remains separate from Bible editorial readiness.

## Later Panels / BlitHook production-guidance update — 2026-10-01

A later logical block completed the production-architecture layer without changing the SDK 25.6 source baseline.

### Native Panels

The later pass adds/reconciles:

- global registration state versus per-panel controller/model versus platform child-view state;
- host-owned `AEGP_PanelH` / `AEGP_PlatformViewRef` versus product-owned child UI;
- create-hook partial-failure rollback;
- conservative child-destroy → worker-stop → unregister → global-teardown order;
- stable match-name identity separated from localized title and transient NSView/HWND;
- panel recreation/state recovery;
- worker → host/UI-safe handoff with generation rejection;
- resize/dock/workspace/HiDPI state as transient view state;
- product-validation wording consistent with `EDITORIAL-GUIDE.md`.

No Panelator source evidence was found that proves a complete teardown/unregister sequence; that limitation remains preserved.

### BlitHook

The later pass adds/reconciles:

- callback pixel pointer treated as borrowed unless a stronger verified lifetime contract exists;
- safe synchronous-copy/staging architecture for post-callback consumers;
- row-aware copy and overflow/size validation;
- explicit blank-frame handling;
- bounded queue/backpressure/drop policy;
- copied view-coordinate metadata;
- display/color boundary versus effect/render/export pixels;
- async flag/receipt/completion preserved as an under-qualified protocol path rather than inventing pointer lifetime;
- worker/IPC ownership and death-hook shutdown order;
- product-validation wording rather than mandatory Bible host testing.

The staging/backpressure design is a conservative product architecture recommendation. It is **not** presented as an Adobe-documented asynchronous BlitHook contract.

**Evidence level after this pass:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED.
