# Recipe — panel + native core

## Architecture

```text
UI (CEP today / UXP later)
       ↓ JSON-like command contract
Bridge adapter
       ↓
Native service / effect / AEGP
       ↓
After Effects + compute core
```

## Protocol rules

Every command:
- `version`;
- `type`;
- request id;
- validated payload;
- success/error response.

Example conceptual payload:

```json
{
  "version": 1,
  "type": "analyzeFrame",
  "requestId": "123",
  "payload": {"layerId": 42, "time": 1.25}
}
```

## Why

UXP migration then replaces `CepBridge`, not product domain logic.

## Avoid

- arbitrary code strings;
- panel directly poking native memory/state;
- one giant unversioned command;
- synchronous blocking UI for long native jobs.
