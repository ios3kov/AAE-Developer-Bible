# Native dockable panel registration — Panelator-shaped template

Status: **registration/source template; SDK 25.6 contract-reviewed; runtime result not claimed**. Platform painting/view implementation remains macOS/Windows-specific.

Use the official SDK `Panelator` sample as the base. The reusable registration sequence is:

```cpp
// 1. command for Window menu
suites.CommandSuite1()->AEGP_GetUniqueCommand(&command);
suites.CommandSuite1()->AEGP_InsertMenuCommand(
    command, "My Native Panel", AEGP_Menu_WINDOW, AEGP_MENU_INSERT_SORTED);

// 2. Window menu click -> toggle visibility
suites.RegisterSuite5()->AEGP_RegisterCommandHook(
    plugin_id, AEGP_HP_BeforeAE, command, CommandHook, command_refcon);

// 3. update menu/checkmark
suites.RegisterSuite5()->AEGP_RegisterUpdateMenuHook(
    plugin_id, UpdateMenuHook, update_refcon);

// 4. register panel factory using AEGP_PanelSuite1
panel_suite->AEGP_RegisterCreatePanelHook(
    plugin_id,
    stable_match_name,
    CreatePanelHook,
    create_refcon,
    TRUE);
```

`CreatePanelHook` receives the host container view, panel handle and function table to fill. Keep `stable_match_name` unlocalized and unchanged across releases because AE uses it to identify the panel/workspace state.

The actual native view class is deliberately not faked here: Cocoa/AppKit and Win32/platform view code differs, so clone the matching current Panelator platform implementation and replace only your UI logic.


## Ownership model

Treat the objects separately:

~~~text
stable match name          product/global identity
AEGP_PanelH                host panel context
AEGP_PlatformViewRef       borrowed host container
panel refcon               product-owned per-panel controller/state
child NSView/HWND widgets  product-owned according to platform UI contract
~~~

Do not destroy the host workspace container from product code.

Do not use the platform pointer or localized title as persistent panel identity.

## Create hook rollback

CreatePanelHook should publish the output function table/refcon only after the product-owned panel state is coherent.

If child UI/controller creation fails:

- destroy only product-owned partial state;
- do not destroy host-owned panel/container objects;
- do not return a dangling refcon;
- keep global registration state valid for a later create attempt.

## Close / recreate

Design the panel so close/reopen constructs a fresh view/controller projection.

Persistent state belongs in:

- AE project data when it is project truth;
- product settings when it is a user/product preference;
- a long-lived product service when explicitly designed.

It should not live only in widget pointers.

## Unregister / shutdown

A conservative order:

~~~text
stop new product work
→ invalidate per-panel async generations
→ destroy product-owned child UI/controller state
→ stop workers/helpers that can target the panel
→ UnRegisterCreatePanelHook when appropriate
→ release global panel services
~~~

The existence of UnRegisterCreatePanelHook does not prove it destroys already-created child UI for the product.

## Threading

Platform UI events should hand semantic commands to a controller/service.

Heavy compute can run on workers using product-owned data, but AEGP project mutation should return through the documented host-safe path.

Do not retain borrowed NSView/HWND/AEGP refs in worker jobs without an explicit contract.

## Evidence boundary

This template captures the current registration/identity/lifecycle contract. Bible does not claim a runtime panel result for the template; a concrete product supplies runtime evidence for the behavior it promises.
