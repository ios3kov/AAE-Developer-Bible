# Threading boundaries

Обновлено **2026-10-01**. В After Effects нельзя делать вывод C++ = можно с любого thread. Thread safety определяется конкретным callback/suite contract.

## 1. Conservative matrix

| Context | Assume |
|---|---|
| Effect render under MFR | may run concurrently |
| host iteration pixel callback | may be parallel depending on suite/path |
| AEGP project/UI manipulation | main-thread-only unless explicitly documented otherwise |
| CEP evalScript host script | host main thread |
| CEP event dispatch involving host | host main-thread scheduling |
| external worker/helper | no AE handles/suites without supported handoff |

~~~text
if documentation does not explicitly promise thread safety,
do not invent it.
~~~

## 2. Effect render

MFR means multiple frames/instances may be processed concurrently.

Избегайте mutable process globals вроде shared scratch/current frame unless synchronization/lifetime deliberately designed.

Prefer callback-local state, immutable tables, host-supported compute cache patterns и explicit per-frame/thread scratch.

## 3. Pixel iteration

Если iteration suite распараллеливает pixels, callback не зависит от order.

~~~text
pixel N writes state
pixel N+1 expects it
~~~

так делать нельзя. Pixel callback должен быть re-entrant.

## 4. AEGP host calls

AEGP API в целом не считать generic thread-safe API.

Project graph, UI, menus, handles, suites и mutations вызывайте из documented host/main-thread path.

## 5. Explicit cross-thread exception example

Public AEGP Utility Suite docs отдельно отмечают AEGP_CauseIdleRoutinesToBeCalled как safe для вызова не с main thread; вызов asynchronous.

При этом получение function pointer через suite API не thread-safe, поэтому pointer нужно acquire/cache на main thread.

~~~text
one function explicitly thread-safe
≠ whole suite thread-safe
~~~

## 6. CEP / ExtendScript

Adobe CEP cookbook указывает:

- evalScript script выполняется в host ExtendScript engine на host main thread;
- CEP event dispatch зависит от host main-thread scheduling;
- long script стоит делить, чтобы event получил шанс быть scheduled.

Поэтому не poll host tight loop, не делайте heavy compute в JSX и batch related mutations.

## 7. Worker → host handoff

~~~text
worker
  pure compute / IO
  produces immutable result
        ↓
thread-safe queue
        ↓
host/main-thread callback
  validates generation
  touches AE APIs
~~~

Worker не сохраняет callback-scoped AE pointer для позднего использования.

## 8. No product mutex across host call

~~~text
lock(product_mutex)
→ call AE suite
→ host re-enters product
→ second path wants mutex
→ deadlock
~~~

Лучше snapshot under lock, unlock, call host, затем отдельно publish result.

## 9. Reentrancy

Защитите:

- shutdown while work pending;
- nested notifications;
- callback after generation changed;
- cancellation while worker finishing;
- render while UI changes non-render product state.

## 10. Generation tokens

~~~text
generation 17 starts compute
user change → generation 18
generation 17 finishes
→ discard stale result
~~~

## 11. Lock ordering

Если locks несколько, задайте единый order и не нарушайте его. Лучше уменьшать число одновременно удерживаемых locks.

## 12. Shutdown

~~~text
stop accepting new work
→ signal cancellation
→ stop transport
→ finish required product workers
→ release product resources
→ release host acquisitions on allowed thread
~~~

Worker после teardown не должен обращаться к unloaded code/host handle.

## 13. Diagnostics

В debug log полезны thread ID, selector/callback, requestId, generation, lock wait duration, shutdown state.

## 14. Product validation cases

- MFR on/off;
- repeated multi-frame stress;
- concurrent UI changes;
- cancel while worker active;
- project close during work;
- AE shutdown during work;
- panel reload;
- long CEP call + event;
- race tooling where applicable.

## Verification boundary

Глава объединяет source-reviewed MFR/AEGP/CEP contracts и conservative architecture guidance. Явно thread-safe функция не расширяет thread safety на соседние calls.

Перечисленные runtime cases относятся к concrete product support claims. Bible не требует собственного host stress run, если не заявляет такой observed result.
