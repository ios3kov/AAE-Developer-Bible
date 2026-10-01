# Recipe — panel + native core

## Goal

Build a hybrid product where the panel is replaceable, native code handles the work that belongs natively, and no layer depends on undocumented shared state.

## Architecture

~~~text
UI shell
  CEP today / future AE UXP
       |
       | versioned plain command
       v
Bridge adapter
       |
       +---- project automation ---> ExtendScript / supported host API
       |
       +---- native control -------> Effect params / AEGP / PICA / helper IPC
                                      |
                                      v
                                 compute core
~~~

Use the simplest bridge that fits the operation.

## 1 — define commands before transport

Example:

~~~json
{
  "protocol": 1,
  "requestId": "123",
  "command": "analyzeFrame",
  "payload": {
    "layerId": "product-stable-id",
    "time": 1.25
  }
}
~~~

Response:

~~~json
{
  "ok": true,
  "requestId": "123",
  "result": {
    "jobId": "job-44"
  }
}
~~~

Do not expose raw pointers/AE handles.

## 2 — prefer project state when enough

If the panel only needs to control an effect:

~~~text
panel
→ JSX dispatcher
→ find effect by match name
→ set normal parameter
→ AE persists/animates it
~~~

This is preferable to inventing custom IPC for values that naturally belong in the project.

## 3 — choose native bridge only for native need

Use AEGP/PICA/helper IPC when you need:

- high-performance compute;
- native service lifecycle;
- data not suitable for effect parameters;
- integration unavailable to scripting.

Document why the extra bridge exists.

## 4 — control plane vs data plane

Panel/JSX messages carry:

- commands;
- IDs;
- options;
- progress/status;
- small summaries.

Large frames/buffers stay native/helper-side.

Do not JSON-serialize megabytes of pixels through evalScript.

## 5 — request lifecycle

Define:

~~~text
created
→ accepted
→ running
→ completed | failed | cancelled
~~~

Panel must know what happens if:

- user closes panel;
- project changes;
- helper restarts;
- AE quits;
- a late response arrives;
- user starts a newer request.

Use request IDs/revisions to drop stale replies.

## 6 — threading

Worker/helper thread:

- pure compute;
- product-owned buffers;
- filesystem/network if designed there.

Host-side command:

- resolve AE objects;
- call documented suites;
- mutate project.

Do not touch project handles from arbitrary worker threads.

## 7 — backpressure

Pick a policy:

- reject while busy;
- cancel previous;
- coalesce to latest;
- bounded queue.

Never create an unbounded queue because a slider fires faster than analysis completes.

## 8 — security

Reject:

- unknown protocol versions;
- unknown commands;
- oversized payloads;
- arbitrary executable paths;
- arbitrary JSX strings;
- invalid file traversal.

Treat local IPC as input, not trusted memory.

## 9 — CEP today

Centralize all evalScript calls in one adapter.

Adobe's CEP documentation states host JSX runs on the host main thread, so split long commands and avoid polling.

## 10 — UXP migration

When AE UXP is actually available, implement a new AeBridge adapter only after its AE-specific API is verified.

Do not rewrite the domain model just to change panel runtime.

## Acceptance

Test:

- normal command;
- invalid payload;
- native/helper unavailable;
- cancellation;
- stale response;
- project switch;
- panel reload;
- AE restart;
- version mismatch.

A UI demo that only completes the happy path is not a finished hybrid protocol.
