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

Communication path:

~~~text
ScriptUI event
→ command function
→ ExtendScript DOM
→ After Effects project model
→ plain command result/status
~~~

The file is intentionally small. Bible does not claim a host-observed result for this source example; a reader may validate it in the target product/environment if needed.
