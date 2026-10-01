# AEGP menu command reference

Status: **drop-in pattern / host verification remains separate**.

MenuTool.cpp forwards to the canonical implementation in 16-WORKING-TEMPLATES/aegp-menu-command. Compile this forwarding file or the canonical source, not both.

## Purpose

This reference isolates the minimum AEGP lifecycle needed for a user-facing menu command:

~~~text
AEGP initialization
→ obtain plug-in ID/refcon
→ register command
→ install command hook
→ install update-menu hook
→ command callback
→ host operation
→ shutdown/death lifecycle
~~~

The default action is deliberately harmless: report information to the user. Replace the work function only after the registration lifecycle itself is proven.

## Start from an official AEGP sample

Use the closest AEGP sample project from the exact SDK as the binary/project shell.

Preserve:

- project settings;
- PiPL/resource plumbing;
- exported initializer contract;
- SDK utility sources;
- platform architecture settings.

Do not recreate the AEGP initializer from memory or copy a historical sample signature over a newer header.

The supplied SDK review already found legacy/current initializer-shape differences, so the target header is the ABI source of truth.

## Command ID lifetime

Treat the command ID returned by the host as host-owned identity for the current plug-in lifecycle.

Do not hardcode an arbitrary numeric command ID.

Store product state/refcon only for the documented lifecycle and release it before host teardown.

## Hook behavior

Command hook should:

1. identify whether the command belongs to this plug-in;
2. return quickly for unrelated commands;
3. validate project state;
4. perform the user operation;
5. preserve host error semantics.

Update-menu hook should only compute enabled/checked/display state. Do not perform expensive project mutations from a menu update callback.

## Project mutation

For a real operation:

~~~text
validate prerequisites
→ start undo group
→ mutate project
→ end undo group
→ report structured result/log
~~~

Undo grouping is not automatic rollback. Prevalidate as much as possible before the first mutation.

See 19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md.

## Error boundary

Do not allow C++ exceptions to escape AEGP callbacks.

Use a deliberate A_Err mapping and cleanup owners for every acquired resource.

## Test sequence

### Registration

- plug-in loads;
- menu item appears once;
- restart does not duplicate it;
- update hook enables/disables as intended.

### Command

- command with no project;
- command with valid project;
- cancellation/failure path;
- repeated execution;
- undo/redo for mutations.

### Lifecycle

- project close/open;
- AE restart;
- plug-in shutdown/death hook;
- no callback touches state after teardown.

## Evidence record

Record:

- AE version/build;
- SDK version/build;
- platform/architecture;
- binary hash;
- menu location/command behavior;
- mutation/undo result;
- restart result.

## Verification boundary

The source shape follows the reviewed AEGP contracts, but documentation/source shape is not host PASS. The exact target SDK project must compile/link and the command must run inside the claimed AE matrix.
