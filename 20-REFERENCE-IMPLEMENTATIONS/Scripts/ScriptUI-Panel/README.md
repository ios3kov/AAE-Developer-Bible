# ScriptUI panel reference source

Status: **SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED**.

Copy AEDeveloperBiblePanel.jsx into the After Effects ScriptUI Panels folder for the target installation, restart AE when required, then open the panel from the Window menu.

The source demonstrates:

- one reusable command function independent of the widgets;
- validation before opening the undo group;
- one undo group around actual mutations;
- dockable Panel vs standalone palette construction;
- resize handling;
- non-modal status reporting instead of an alert for normal command errors.

`renameSelectedLayers(prefix)` validates and snapshots immediate targets, then
returns `{ok, changed, total, error, cleanupError}`. The button uses `Layer_` numbering;
partial setter failures retain completed count, Undo close errors are separate,
and controls are re-enabled in finally. Both Panel/Window receive initial layout.
No progress/cancel scheduler, persistent target IDs, collision policy or rollback
implementation is included. See [deferred-job design](../../../06-SCRIPTING/02-SCRIPTUI.md#concrete-synchronous-command-and-deferred-job-design).

Portable fake-host tests in `scripts/test_scriptui_command.js` cover validation,
success, setter failure, Undo-start/close failure and UI restoration. They do not
emulate ScriptUI painting, docking, host object invalidation or ExtendScript engines.

Communication path:

~~~text
ScriptUI event
→ command function
→ ExtendScript DOM
→ After Effects project model
→ plain command result/status
~~~

The file is intentionally small. Bible does not claim a host-observed result for this source example; a reader may validate it in the target product/environment if needed.
