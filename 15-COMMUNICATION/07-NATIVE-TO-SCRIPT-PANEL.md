# Native ↔ script/panel: архитектура гибридного продукта

Обновлено **2026-10-01**. UI, host automation и heavy native compute — разные слои. Связь между ними должна быть явной, versioned и малой по объёму.

## 1. Recommended layers

~~~text
UI shell
  CEP now / UXP later
        |
        | versioned commands + JSON
        v
Automation layer
  ExtendScript dispatcher
        |
        +---- project edits ------> AE scripting DOM
        |
        +---- control request ----> native rendezvous
                                   |
                                   v
Native layer
  Effect / AEGP / helper
        |
        +---- PICA suites -------> AE C++ APIs
        +---- shared suite ------> sibling native module
        +---- external IPC ------> helper/service
~~~

Business logic не должна знать concrete panel runtime.

## 2. Control plane vs data plane

**Control:** commands, IDs, paths, small settings, progress, status/error, invalidation.

**Data:** frames, pixel buffers, audio, ML tensors, large caches/assets.

CEP/ExtendScript JSON bridge подходит для control plane. Heavy data должен оставаться native/external.

## 3. Выбор bridge

### Panel → AE project

ExtendScript/host-supported panel API для layers/items, properties/keyframes, import/render queue и project automation.

### AEGP → конкретный Effect

AEGP_EffectCallGeneric — маленький synchronous request/response к конкретному effect instance, если это лучший documented bridge. Не скрытая render dependency.

### Native → native

Published PICA suite — in-process versioned service между native modules.

### Native → scripting DOM

AEGP_ExecuteScript — редкий bridge к scripting-only capability.

### Process → process

Использовать явный IPC:

- named pipe / Unix domain socket;
- localhost socket с security model;
- child-process stdin/stdout;
- temp file + atomic rename для large batch;
- shared memory только после profiling и с explicit ownership.

Undocumented AE internal IPC не считать product API.

## 4. Heavy binary не через JSX

Плохо:

~~~text
native pixels
→ Base64
→ ExtendScript string
→ evalScript
→ CEP JS
~~~

Цена: copying, encoding, temporary memory, main-thread pressure.

UI должен отправлять control request и получать compact metadata/progress.

## 5. Version handshake

~~~json
{
  "protocol": 3,
  "uiVersion": "2.4.1",
  "nativeApi": 5,
  "capabilities": [
    "preview-v2",
    "cancel-v1"
  ]
}
~~~

Panel, native plug-in и helper могут оказаться разных версий после partial update/rollback, поэтому package version недостаточно.

## 6. Compatibility rule

~~~text
same protocol major
+ larger message size
+ unknown optional field
→ old peer may ignore extension
~~~

Если изменился meaning поля, ownership или required call order — новая protocol/API version.

## 7. Native → panel notification

Не хранить direct pointer на UI.

~~~text
native state changes
→ small notification/invalidation
→ scripting/panel bridge
→ panel requests fresh state
~~~

UI должен уметь восстановиться explicit refresh.

## 8. Persistent state

| State | Typical owner |
|---|---|
| effect render parameters | AE project/effect params |
| panel layout/preferences | panel/product preferences |
| large transient cache | native/helper runtime |
| external asset index | product database/cache |
| current selected AE object | AE host; query/revalidate |

Render-affecting state не хранить только в panel DOM или global singleton.

## 9. Liveness

Panel reload, helper crash, missing plug-in/provider, closed project, removed effect и AE shutdown — нормальные failure states.

~~~text
starting
ready
busy
canceling
failed
stopped
~~~

Молчание peer не равно infinite busy.

## 10. Cancellation

~~~text
start(requestId)
→ progress(requestId)
→ cancel(requestId)
→ canceled(requestId) / completed(requestId)
~~~

Late completion старой generation не должен менять новый UI state.

## 11. Security

- identify peer where needed;
- do not expose external interface without need;
- validate message size before allocation;
- allowlist opcodes;
- normalize paths;
- never execute arbitrary command strings from panel/network;
- не передавать secrets через visible command line/logs.

## 12. Failure taxonomy

Различайте UI validation, panel transport, scripting, native bridge, native operation, helper transport, protocol mismatch, cancellation и stale result.

## 13. Observability

Логируйте timestamp, requestId, protocol, component, operation, state transition, duration и result/error code. Не логируйте secrets и huge payloads.

## 14. Acceptance checklist

- panel without native;
- native without panel;
- wrong protocol;
- helper killed mid-request;
- project closed;
- effect removed/reordered;
- panel reload;
- repeated start/stop;
- cancel + late completion;
- partial update;
- rollback;
- clean shutdown;
- crash restart.

## Verification boundary

Глава задаёт production architecture pattern поверх public bridges. Generic call/PICA exact-SDK boundaries описаны в source review 25.6; end-to-end hybrid проверки остаются отдельными acceptance tests.
