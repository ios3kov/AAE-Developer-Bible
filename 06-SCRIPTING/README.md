# ExtendScript scripting

After Effects scripting API отображает UI/project hierarchy в объектную модель: application → project → items/compositions → layers → properties/keyframes, плюс render queue и import options.

## Best use cases

- batch project construction;
- repetitive layer/property operations;
- render queue setup;
- pipeline glue;
- asset relinking/import;
- one-click artist tools;
- prototype logic before native implementation.

## Not for

- heavy per-pixel processing;
- realtime frame algorithms;
- low-level GPU work;
- unrestricted modern Node/browser assumptions.

## Script quality rules

- `app.beginUndoGroup` / corresponding end where appropriate;
- restore user state you temporarily change;
- validate active project/item/layer;
- never assume selected item type;
- protect against missing effects/fonts/files;
- use match names where localization/stability requires it;
- handle cancel cleanly;
- use progress UI only if operation genuinely long.
