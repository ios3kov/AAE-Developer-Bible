# Native dockable panels

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Public contract:** `AE_GeneralPlugPanels.h`, `AEGP_PanelSuite1`, sample `Panelator`.
**Evidence level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED.

AEGP Workspace Panel — native panel tab, который After Effects может создать и встроить в workspace. Это **не Effect custom UI**, не CEP/UXP panel и не arbitrary floating OS window.

## 1. Panel Suite baseline

SDK 25.6 объявляет:

- `kAEGPPanelSuite = "AEGP Workspace Panel Suite"`;
- `kAEGPPanelSuiteVersion1 = 1`, frozen in AE 8.0;
- `AEGP_PanelSuite1`;
- `AEGP_PanelFunctions1` callback table.

Стабильный version number не означает, что platform UI code не меняется между macOS/Windows/OS versions.

## 2. Platform container

`AEGP_PlatformViewRef` в current header:

- macOS 64-bit: `NSView*`;
- Windows: `HWND`.

Create hook получает **host-owned container view**. Plug-in строит собственный native UI внутри него; не заменяет сам workspace frame.

## 3. Registration

`AEGP_RegisterCreatePanelHook` принимает:

- plugin id;
- UTF-8 **match name** — header прямо говорит *do not localize*;
- create hook;
- create-panel refcon;
- `paint_backgroundB`.

```text
AEGP initializer
→ acquire PanelSuite1
→ RegisterCreatePanelHook(stable_match_name)
→ optional Window-menu command
→ ToggleVisibility(match_name)
```

Match name — programmatic identity tab. User-visible title меняется отдельно через `AEGP_SetTitle` и может быть localized.

## 4. CreatePanelHook result

Host вызывает:

```cpp
AEGP_CreatePanelHook(
    plugin_global_refcon,
    create_refcon,
    platform_container,
    panelH,
    outFunctionTable,
    outPanelRefcon);
```

Plug-in:

1. создаёт per-panel UI/controller state;
2. сохраняет `panelH`/container only according to platform lifetime;
3. заполняет `AEGP_PanelFunctions1`;
4. возвращает `AEGP_PanelRefcon` для subsequent panel callbacks.

Per-panel refcon не равен AEGP global refcon. Один plugin может концептуально иметь разные lifecycle layers.

## 5. `AEGP_PanelFunctions1`

Таблица содержит три callbacks:

- `GetSnapSizes` — до 5 preferred snap sizes (header предупреждает не давать больше);
- `PopulateFlyout` — declarative flyout menu;
- `DoFlyoutCommand` — command callback.

Rendering/painting native child view **не происходит через эту table**: platform-specific UI code sample subclass-ит/обрабатывает NSView/HWND path.

## 6. Flyout menu contract

`AEGP_FlyoutMenuItem` содержит:

- indent;
- normal/checked/radio/separator type;
- enabled flag;
- command ID;
- UTF-8 display name.

`PopulateFlyout` получает caller buffer и in/out count. Production callback должен уважать capacity и вернуть total/actual contract так, как задаёт header/sample; нельзя без проверки писать arbitrary number items.

Panelator делает bounded copy на основе supplied capacity.

## 7. Window menu integration

Panelator отдельно:

- получает `AEGP_Command`;
- вставляет command в Window menu;
- CommandHook вызывает `AEGP_ToggleVisibility(match_name)`;
- UpdateMenuHook читает `AEGP_IsShown` и ставит checkmark.

Это пример integration UX, **не обязательная часть PanelSuite itself**. Можно проектировать panel visibility другим supported workflow, но match-name identity остаётся центральной.

## 8. `ToggleVisibility` и `IsShown`

Header описывает standard Window-menu operation:

- если tab отсутствует в workspace — создать;
- если не frontmost — вывести вперёд;
- если visible/frontmost — закрыть.

`IsShown` отдельно возвращает:

- tab shown;
- panel frontmost.

Не сводите оба состояния к одному boolean.

## 9. Unregister exists — используйте lifecycle осознанно

`AEGP_UnRegisterCreatePanelHook(match_name)` существует в PanelSuite1.

Это отличие от общих AEGP RegisterSuite hooks, где в рассмотренном RegisterSuite5 нет generic unregister для всех hook types.

Наличие unregister API не означает, что можно безопасно выгрузить native code, пока созданные panel objects/platform callbacks всё ещё живы. Сначала закройте/уничтожьте panel state по host/platform contract, затем unregister where appropriate.

## 10. Panelator sample: useful skeleton, incomplete lifetime proof

Panelator:

- регистрирует command/update hooks;
- регистрирует CreatePanelHook;
- создаёт `PanelatorUI_Plat` per panel;
- заполняет snap/flyout callbacks;
- меняет title;
- имеет separate Mac/Windows platform implementation.

Но reviewed `Panelator.cpp` не показывает destructor/unregister sequence для `Panelator` global object и CreatePanelHook. Поэтому sample **не является доказательством полного shutdown/unload lifecycle**.

Это source finding, не measured leak/crash.

## 11. Stable match name vs localized title

Header explicitly says register/unregister/toggle match name **do not localize**. `SetTitle` is where visible title can change.

Panelator sample derives `i_match_nameZ` from its string table name. В новом production code лучше иметь отдельную compile-time stable ASCII/UTF-8 identity и отдельный localized display title, чтобы localization не ломала workspace persistence.

Это design recommendation based on identity contract; сам sample не доказывает localization bug.

## 12. Platform-specific UI cost

Panelator source действительно разделяет:

- common panel controller;
- Mac `PanelatorUI_Plat.cpp`;
- Windows `PanelatorUI_Plat.cpp`.

Следовательно native panel означает поддержку platform window/event/drawing code. Это существенно дороже browser-based panel и является причиной выбирать этот API только когда tight native UI integration оправдывает стоимость.

## 13. Main-thread/project calls

То, что UI native, не разрешает вызывать arbitrary AEGP project mutations из любого worker/platform callback. Threading permission задаётся конкретным suite contract.

Практика:

- UI event → короткий state update;
- main-thread/supported AEGP callback → project mutation;
- heavy pure compute → worker;
- результат → безопасный UI invalidation.

## 14. Panel state model

A production native panel should separate at least four state scopes:

~~~text
module/global registration state
→ panel factory/create-hook state
→ per-panel controller/model state
→ platform child-view/widget state
~~~

These scopes do not necessarily begin/end together.

### Global registration state

Owns:

- stable match name;
- AEGP command IDs;
- hook registration bookkeeping;
- product services shared by panel instances.

It must outlive callbacks that depend on it.

### Per-panel state

Owns:

- controller/model;
- current normalized UI projection;
- product-owned child views/widgets;
- pending request/generation state.

It should not become the only source of project truth.

### Host-owned panel/container state

`AEGP_PanelH` and `AEGP_PlatformViewRef` are host-side context/containers.

Treat the host container as borrowed according to panel lifetime; do not destroy the host workspace container as though the product created it.

### Product-owned child UI

Cocoa/Win32 child controls/views created by the plug-in are product-owned unless the platform/container contract transfers ownership.

Document parent/child destruction order explicitly.

## 15. Create failure rollback

CreatePanelHook can fail after partial product initialization.

Recommended pattern:

~~~text
validate arguments
→ allocate controller/model
→ create platform child UI
→ connect callbacks
→ fill PanelFunctions1
→ publish panel refcon
→ success
~~~

On failure:

- destroy only product-owned child UI already created;
- release product-owned controller/model state;
- do not destroy host-owned container/panel objects;
- do not publish a partially initialized refcon.

Create failure should not leave a callable platform callback pointing to freed product state.

## 16. Destroy / unregister order

Because the source review does not prove Panelator teardown semantics, use a conservative product design:

~~~text
stop new product work
→ invalidate panel generation/callback targets
→ destroy product-owned child UI/controller state
→ ensure no worker can call the panel
→ unregister panel factory when appropriate
→ release global panel services
~~~

Do not unregister code while live platform callbacks can still enter unloaded/freed state.

`AEGP_UnRegisterCreatePanelHook` removes the create-hook registration; it is not proof that existing native child views are destroyed for you.

## 17. Panel identity and workspace persistence

Separate:

~~~text
stable match name
≠ localized visible title
≠ HWND / NSView pointer
≠ current workspace position
~~~

The stable match name is the product identity used by panel APIs/workspace persistence.

Do not derive persistent identity from:

- localized title;
- current platform handle;
- translated string table value;
- transient panel refcon address.

Visible title may change without changing panel identity.

## 18. UI model vs project model

Recommended architecture:

~~~text
native widgets
→ panel controller
→ semantic command
→ AEGP/project service
→ normalized result/snapshot
→ UI projection
~~~

Panel widget state is a projection.

For project-changing commands:

- resolve current project targets late;
- validate current IDs/state;
- mutate on supported host path;
- return a fresh result/snapshot.

Do not keep long-lived opaque AEGP refs simply because the panel remains open.

## 19. Worker handoff

Heavy compute may run outside the UI thread only on product-owned/pure data.

~~~text
panel event
→ immutable request
→ worker
→ result + generation
→ host/UI-safe handoff
→ discard if stale
~~~

Do not retain borrowed `NSView*`, `HWND`, panel handle or project ref on a worker unless the exact contract explicitly permits it.

## 20. Resize / HiDPI / platform lifecycle

Native panel UI must treat geometry as platform/view state.

Plan for:

- repeated resize;
- dock/undock;
- workspace switch;
- DPI/scale changes;
- child-view recreation;
- hidden/not-frontmost panel;
- multiple monitor configurations.

Do not cache pixel dimensions as permanent layout truth.

Use logical/layout units appropriate to the platform implementation and recompute render/layout resources when scale/size changes.

## 21. Flyout/menu command model

Flyout command IDs should be stable within the panel implementation and mapped to semantic actions.

Avoid direct project mutation inside low-level platform menu plumbing.

Better:

~~~text
flyout command ID
→ controller action
→ validate current project state
→ AEGP service mutation
→ refresh projection
~~~

Respect caller-provided flyout capacity/count rules.

## 22. Panel recreation

A panel can conceptually be recreated while project/product state survives.

Therefore:

- persistent user settings belong in product config;
- project truth belongs in AE/project data;
- long-running background task belongs in a service with explicit lifecycle;
- widget objects belong only to the current panel instance.

Reopening a panel should reconstruct view state from current product/project state rather than relying on old pointers.

## 23. Product validation guidance

If a concrete native-panel product claims these behaviors, useful runtime cases include:

- registration once / no duplicate identity;
- Window menu toggle/checkmark;
- create/close/recreate;
- dock/undock/resize;
- snap sizes;
- flyout commands;
- localized title with stable match name;
- workspace save/reopen;
- multiple workspaces;
- project close/open while panel exists;
- worker completion after panel recreation;
- application shutdown;
- failure during panel creation;
- macOS and Windows event/drawing behavior;
- HiDPI/Retina/scaling.

These establish product support evidence. Bible remains SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED unless a separate runtime record exists.

## 24. Anti-patterns

Avoid:

- using display title as panel identity;
- destroying the host-owned container;
- storing project truth only in widget state;
- project mutation from arbitrary worker callbacks;
- keeping stale AEGP refs for the entire panel lifetime;
- unregistering while platform callbacks can still enter product code;
- assuming close/reopen returns the same platform view pointer;
- copying Panelator lifetime omissions as production teardown policy.

## Related chapters

- [Panel architecture](../07-PANELS/README.md)
- [AEGP tools](05-AEGP-TOOLS.md)
- [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md)
- [Data ownership](../15-COMMUNICATION/09-DATA-OWNERSHIP.md)
- [Native/script/panel communication](../15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md)

## Source record

[Native panels and BlitHook SDK 25.6 review](../18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md).