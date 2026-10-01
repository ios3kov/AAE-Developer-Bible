# AEGP menu command working template

Status: **drop-in source pattern / host verification pending**.

MenuTool.cpp is intended to replace the implementation layer inside an official AEGP sample project from the exact target SDK.

Keep the Adobe project, PiPL/resource/export plumbing and SDK utility files.

## What this source implements

The template contains:

- product state stored through the AEGP global refcon;
- command ID acquisition;
- Window-menu insertion;
- command hook;
- update-menu hook;
- death hook;
- exception containment around host callbacks;
- partial-initialization policy.

Default command behavior only reports that the tool is alive.

## Initialization order

The source deliberately resolves suite access before installing callbacks where possible.

Then:

~~~text
register death hook
→ publish global refcon/state
→ get unique command
→ insert menu command
→ register command hook
→ register update-menu hook
~~~

This order matters because AE does not provide a generic rollback/unregister path for every hook after partial registration.

## Partial initialization

If initialization fails after the death hook/global state is already live, the source does not delete state and return an arbitrary failure that could leave registered callbacks pointing at freed memory.

Instead it:

- keeps the state resident;
- disables/zeros the command;
- reports initialization failure;
- lets DeathHook own final state cleanup.

This is a deliberate safety policy, not proof that every failure mode is recoverable.

## Command hook

The callback ignores:

- missing state;
- zero command;
- commands already handled;
- unrelated command IDs.

It marks the command handled only after DoWork succeeds.

When replacing DoWork with project mutation, validate all target objects before starting edits.

## Update hook

Current behavior enables the command.

A real product should compute command availability quickly from current host state.

Do not perform expensive work, network calls or project mutation from the update-menu hook.

## Death hook

DeathHook deletes ToolState.

Therefore no other product worker/callback may use ToolState after shutdown begins.

If the real product owns workers/helpers/resources, extend shutdown order before deleting state.

## Adding project mutation

Recommended pattern:

~~~text
CommandHook
→ validate project/selection
→ acquire required suites/resources
→ AegpUndoScope
→ mutate
→ release owners
→ return result
~~~

Use the ownership and undo helpers in 19-NATIVE-CODE-FOUNDATION where their exact contracts fit.

## SDK version boundary

The supplied SDK review found historical AEGP initializer signatures that differ from the current 25.6 header.

Do not copy an old sample initializer declaration literally into a new SDK project.

Compile against the exact target header.

## Tests before calling it working

- command appears once;
- restart does not duplicate;
- update hook state works;
- command executes;
- unrelated commands ignored;
- no-project/invalid-selection path;
- undo/redo for real mutations;
- partial initialization failure;
- shutdown/death cleanup;
- repeated AE restart.

## Verification boundary

The source has architecture and safety intent, but it is not a standalone build. Host PASS requires grafting it into the exact SDK AEGP project, compiling/linking and exercising it in After Effects.
