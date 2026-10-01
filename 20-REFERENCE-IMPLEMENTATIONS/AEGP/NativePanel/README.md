# Native AEGP panel reference path

Status: **SDK sample workspace: Panelator / host-test pending**.

Materialize the exact licensed SDK sample with scripts/materialize_sdk_examples.py and use it as the project/lifecycle shell.

## Why this is guide-only

A native workspace panel is not only a callback function. It depends on host registration, panel identity, creation callbacks, visibility/flyout handling and platform/window integration that are version-sensitive.

The Bible therefore does not invent a standalone project wrapper here.

## Source of truth

Use:

- 14-NATIVE-INTEGRATIONS/07-NATIVE-PANELS.md for architecture;
- 18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md for the supplied SDK review;
- the exact SDK Panelator sample for project/plumbing.

For SDK 25.6, the reviewed panel contract centers on AEGP_PanelSuite1 and the Panelator sample. A later SDK may differ.

## Integration sequence

~~~text
materialize exact Panelator sample
→ build/load untouched sample
→ record host behavior
→ rename product identity only
→ build/load again
→ replace panel content incrementally
→ add product state/commands
~~~

If untouched Panelator fails, stop before adding product code.

## Panel identity

Define stable product identity separately from visible localized title.

Do not use transient window handles or display strings as persistent object identity.

## Lifetime

Document:

- who owns product panel state;
- creation/destruction order;
- what is borrowed from host;
- what may be retained;
- how callbacks stop during shutdown.

Do not keep panel/window pointers beyond their documented lifetime.

## Threading

Treat panel/project manipulation as host/UI-thread work unless a specific API explicitly allows another thread.

Heavy computation belongs in a worker/service with a controlled handoff back to the host thread.

## UI → host operations

Keep panel callbacks thin:

~~~text
UI event
→ validated command
→ AEGP/project service
→ normalized result
→ UI update
~~~

Do not bury project mutation directly in platform event plumbing.

## State recovery

Test panel recreation/reopen:

- close/reopen workspace panel;
- switch workspace;
- close/open project;
- restart AE.

Panel widget state must not become the only source of project truth.

## Required host tests

- registration;
- create/open;
- resize;
- visibility;
- flyout/menu if used;
- project command;
- workspace change;
- repeated close/open;
- shutdown;
- crash-free restart.

## Verification boundary

This entry intentionally remains guide-only until the exact Panelator-derived workspace is compiled and tested. A registration snippet alone is not a working native panel.
