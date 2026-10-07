# Panels: CEP now, UXP transition

Panels are the UI/application layer of many After Effects tools. They should not become the place where project/render truth is accidentally stored.

## Dated platform status

On the Bible research snapshot, Adobe has announced UXP for After Effects and a transition away from CEP. The detailed dates/source are recorded in [UXP transition](02-UXP-TRANSITION.md).

Treat roadmap dates as dated facts, not permanent API contracts.

## Architecture first

Recommended structure:

```text
UI shell
   ↓
commands / application services
   ↓
AE bridge adapter
   ↓
After Effects
```

Today the shell may be CEP; later it may be UXP. Domain/application logic should survive the shell change.

## Source of truth

Do not make panel DOM/state the only source of truth for:

- layer identity;
- effect parameters;
- project structure;
- render-affecting state.

Panel state is a projection/cache.

After Effects project model or an explicitly owned external model is the authoritative state.

## CEP model

CEP commonly has two worlds:

```text
HTML/JS/CEF side
↕ evalScript/events
ExtendScript host side
↕
After Effects scripting DOM
```

Centralize this boundary.

## Command dispatcher

Prefer:

```text
UI button
→ dispatch("renameLayers", payload)
→ host adapter
→ known command implementation
```

over arbitrary `evalScript("...")` strings generated across components.

## Request/response

Use versioned envelope with:

- protocol/version;
- request ID;
- command;
- payload;
- structured success/error.

Async responses should be rejectable when stale. Rejection/timeout does not cancel
host mutation; unknown outcome must be reconciled before retrying. Actual teaching
contract is `protocol/requestId/command/payload`; see [CEP bridge](../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md).

## State refresh

Panel may refresh by:

- explicit user action;
- host/event notification;
- bounded polling fallback;
- command result carrying fresh state.

Polling is not automatically wrong, but cost/visibility/staleness must be explicit.

Do not continuously serialize entire large projects without measuring cost.

## Long operations

For long task:

```text
UI starts request
→ UI remains responsive
→ native/helper/background service works
→ progress/status
→ completion/error
```

Never assume `evalScript` is a good transport for huge binary payload.

## Control plane vs data plane

Panel bridge is good for:

- commands;
- IDs;
- options;
- small snapshots;
- progress/errors.

Heavy pixels/audio/tensors belong in native/helper/file/shared-memory data path.

## File and network access

Abstract filesystem/network behind app services.

Why:

- CEP and UXP security models differ;
- permissions differ;
- testability improves;
- migration is localized.

Do not let business logic depend directly on `window.cep` or CEF-specific filesystem behavior.

## Native integration

Hybrid product:

```text
panel
→ versioned command
→ native helper/AEGP/effect service
→ AE
```

Keep raw host pointers/handles out of JS protocol.

## Failure model

Handle:

- host bridge unavailable;
- malformed result;
- protocol mismatch;
- request timeout;
- stale response;
- project changed meanwhile;
- helper process unavailable;
- panel reloaded;
- unsupported host version.

UI should recover without forcing AE restart where possible.

## Panel reload

CEP/UXP UI can reload independently of AE project.

Therefore persistent operation state cannot live only in JS memory if it must survive reload.

Decide explicitly what state belongs to:

- project;
- product settings;
- native/helper process;
- ephemeral UI.

## Security

Do not expose unrestricted local command execution through panel bridge.

Use allowlisted commands and validate payloads.

External helper IPC should have explicit local trust/authentication assumptions.

## Native panel vs CEP/UXP

Choose native Workspace Panel when:

- tight native UI integration is required;
- OS-native widget/event work is acceptable;
- platform-specific maintenance is justified.

Choose CEP/UXP when rich cross-platform UI/product UX matters more.

## Migration-friendly design

Avoid:

- domain model in React/Vue component state;
- direct `evalScript()` everywhere;
- filesystem calls embedded in UI components;
- CEP-specific events as business events.

Prefer:

```text
UI components
→ app commands
→ interfaces
→ CEP adapter today
→ UXP adapter later
```

## Packaging boundary

Panel distribution may include:

- extension manifest;
- HTML/JS/CSS assets;
- ExtendScript host code;
- optional native/helper components;
- licenses/config/assets.

Version these components as one product release when they must interoperate.

## Diagnostics

Log enough identity:

- panel/product version;
- AE version/build;
- bridge protocol version;
- request ID;
- helper/native version where applicable.

Do not log full sensitive project paths/content without a support reason.

## Product test areas

For a panel product consider:

- install/discovery;
- dock/resize;
- reload;
- project open/close;
- no active comp;
- bridge failure;
- stale response;
- long operation/cancel;
- multi-monitor/scale;
- offline/network failure if relevant;
- migration compatibility.

Bible documents these areas; it does not need to execute every panel source example.

## Read next

- [AE UXP host API and concrete project command](03-UXP-HOST-API.md)

- [CEP](01-CEP.md)
- [UXP transition](02-UXP-TRANSITION.md)
- [CEP → ExtendScript](../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md)
- [Native ↔ script/panel](../15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md)
- [Communication architecture](../01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md)

## Evidence boundary

Platform transition dates are dated source-review facts. Architecture guidance is designed to remain useful even as the UI runtime changes.
