# Standalone JSX tool

Дополнительные source lessons (AE execution NOT_RUN):

- [build-demo-rig.jsx](build-demo-rig.jsx): comp/null/text, slider, expression,
  keys/interpolation, mask/marker, own-comp-only compensation.
  Opacity keys are 0→100; slider50 adds to animated `value` with 0…100 clamp.
  Thus expected evaluated opacity at t=0 is50 and t=1 is100; disabling expression
  restores keyed 0→100. This is a declared expectation, not an observed host result.
- [import-and-queue.jsx](import-and-queue.jsx): один visual file, новая comp,
  disabled output queue, exact template и path readback; не запускает render.

Запускать на disposable project. Scripts используют host APIs; Node syntax check
не доказывает ExtendScript/AE support. User files и существующие queue items не
удаляются. Undo grouping не atomic rollback.

Status: **SOURCE EXAMPLE — complete command source / RUNTIME-NOT-CLAIMED**.

rename-selected-layers.jsx is intentionally small enough to audit as one complete Script-menu command.

## Behavior

The command:

1. requires an open project;
2. requires active item to be a composition;
3. requires at least one selected layer;
4. opens one undo group;
5. prefixes selected layer names with Bible_index_;
6. always ends the undo group through finally;
7. catches top-level errors and reports them.

## Why validation happens first

The script validates project, composition and selection before opening the undo group.

This reduces empty undo entries and partial work.

For a more complex command, do as much non-mutating validation as possible before the first edit.

## Undo boundary

~~~text
validate
→ beginUndoGroup
→ all related mutations
→ finally endUndoGroup
~~~

Undo group is user history, not automatic rollback after an exception.

A production command with multiple failure-prone mutations may still need explicit cleanup.

## Selection references

The source reads selectedLayers once and immediately performs a simple rename that does not restructure the layer collection.

For structural operations such as add/remove/reorder, do not assume every stored host reference remains valid. Reacquire where required.

## Naming collision

This example intentionally demonstrates mechanics, not a production naming policy.

Repeated execution adds another prefix.

A real renamer should define:

- idempotency;
- duplicate names;
- numbering;
- localization;
- illegal/path-sensitive characters if names leave AE;
- undo expectation.

## Installation

Use the Scripts location appropriate to the target AE installation/user policy.

If you want a dockable ScriptUI panel instead of a one-shot script, use 20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel.

## Test cases

- no project;
- active footage/folder instead of comp;
- comp with no selection;
- one selected layer;
- many selected layers;
- Unicode names;
- repeated execution;
- undo;
- redo;
- save/reopen.

## Turning this into a reusable command

Separate:

~~~text
UI/entry wrapper
→ renameSelectedLayers command
→ AE scripting DOM
→ plain result
~~~

Then the same command logic can be called from ScriptUI or a CEP dispatcher without copying mutation logic.

The separate [ScriptUI reference](../../20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/README.md)
implements a widget-independent synchronous rename command with partial counts and
Undo-close diagnostics. It sets `Layer_1`, etc.; this standalone IIFE instead prefixes
old names and reports only success count/top-level alert. Do not conflate them.
The import lesson prompts for a template after creating its disabled queue item,
inside Undo; readback verifies only output path, not output settings/format. Fixed
comp duration/framerate and filename-extension checks remain user inspection work.

## Verification boundary

The source is directly runnable in principle, but the repository only records host verification after the exact AE/OS run and expected project changes are captured.
