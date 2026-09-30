# Native dockable panel registration — Panelator-shaped template

Status: **registration drop-in**. Platform painting/view implementation remains macOS/Windows-specific.

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
