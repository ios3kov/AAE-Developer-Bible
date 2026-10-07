# BlitHook — display-pipeline frame hook

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Public header in supplied SDK:** `AE_Hook.h`, hook protocol major/minor **3.0**.
**Bundled sample:** `GP/EMP` (External Monitor Preview).
**Evidence level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED.

BlitHook получает pixel buffer в момент, когда After Effects передаёт изображение display/monitoring pipeline. Это legacy/general-hook integration path, а не Effect/AEGP/AEIO/Artisan callback.

## 1. Plugin type and entry point are different

`AE_Hook.h` defines:

- `AE_HOOK_PLUGIN_TYPE = 'AEgp'`;
- major 3, minor 0;
- `AE_HookPluginEntryFunc(major, minor, file_specH, res_specH, AE_Hooks*)`.

Bundled EMP PiPL uses `Kind { AEGeneral }`, **not** `Kind { AEGP }`.

Это отдельная legacy/general integration family. Не graft-ите AEGP `EntryPointFunc(SPBasicSuite*,...)` signature в BlitHook plugin.

## 2. Hook table

`AE_Hooks` contains:

- plugin refcon;
- reserved pointers;
- death hook;
- version hook;
- `SPBasicSuite*` supplied by host;
- blit hook;
- cursor hook.

EMP sample заполняет только blit/death/version.

## 3. Pixel buffer contract

`AE_PixBuffer` in SDK 25.6:

- width / height;
- `depthL`: 32, 64 or 128 bits per pixel;
- pixel format ARGB or BGRA;
- `row_bytesL`;
- `chan_bytesL`: 4, 8 or 16;
- `plane_bytesL`: 1, 2 or 4;
- raw pixel pointer.

Header comment says current platform ordering is ARGB on Mac and BGRA on Windows **for now**. Это именно source statement; не превращайте его в вечный cross-version ABI rule.

Всегда использовать:

```text
depth + pix_format + row_bytes + plane_bytes
```

а не assumption `width*4`.

## 4. View coordinates are separate from pixel buffer size

`AE_ViewCoordinates` содержит:

- full original frame width/height;
- origin of pix buffer in frame coordinates;
- actual visible view rect.

Следовательно BlitHook может получить buffer, который представляет region/placement относительно полного frame. Не интерпретируйте `pix_buf.width/height` как единственный geometry context.

## 5. `pix_bufP0` may be null

Header explicitly says null pixel buffer means **display a blank frame**.

Callback должен иметь defined blank-frame path; dereference without check is invalid.

## 6. Rendering flag

`AE_BlitInFlag_RENDERING` tells hook the call is associated with rendering state. Это input flag, не permission to mutate AE project/render graph.

Не выводите из него, что callback is Render Queue replacement or that pixels are final encoded output.

## 7. Sync vs async

`AE_BlitOutFlag_ASYNCHRONOUS` exists; callback also receives:

- opaque `AE_BlitReceipt`;
- optional `AE_BlitCompleteFunc`.

Эти fields показывают, что protocol допускает asynchronous completion. Но supplied EMP sample **не реализует asynchronous path**: его MyBlit immediately returns success and doesn't set async flag/call completion.

Поэтому Bible не придумывает недокументированный timing/lifetime rule. Пока async behavior не квалифицировано отдельным host test/source comment, safest implementation для простого monitor consumer:

- finish/copy required pixel data synchronously before returning;
- or implement async only from verified protocol details and keep receipt/completion bookkeeping exact.

Нельзя просто сохранить `pixelsPV` и использовать его на worker после return без доказанного lifetime.

## 8. Blit callback must stay cheap

Display pipeline чувствителен к latency. В callback не следует:

- encode video synchronously;
- делать blocking network I/O;
- долго ждать GPU/worker;
- брать global mutex around heavy work;
- выполнять project traversal/mutation.

Для внешнего monitor/streamer:

```text
BlitHook
→ validate metadata
→ bounded copy / staging
→ lock-free or bounded queue
→ worker/IPC
```

При backpressure лучше заранее определить drop policy, чем бесконечно блокировать AE display.

## 9. Version hook

`AE_VersionHook` получает pointer to version output. EMP returns 1. Header-level hook protocol itself reports major/minor 3.0 at plugin entry.

Product version и hook protocol version — разные domains.

## 10. Death hook

`AE_DeathHook` is `void` and receives only hook refcon. Cleanup design должен быть non-throwing and deterministic.

Если worker/service запущен BlitHook-ом:

- stop accepting frames;
- signal worker;
- bound wait/shutdown;
- free copied buffers/queues;
- не обращаться к host pointers after teardown.

## 11. EMP sample is only a skeleton

`GP/EMP/EMP.cpp`:

- MyBlit returns success without processing;
- MyDeath only comments cleanup;
- MyVersion returns 1;
- EntryPoint assigns the three hooks.

То есть EMP доказывает call shape/registration skeleton, **не** pixels lifetime, async behavior, external monitor implementation, color correctness or performance.

## 12. Color and display semantics

BlitHook sees display-pipeline pixels, not necessarily the same numeric buffer as:

- effect input/output world;
- pre-color-management composition linear pixels;
- encoded Render Queue file;
- GPU texture.

Do not use BlitHook capture as bit-exact reference for effect algorithm unless display/color/channel path is explicitly controlled.

## 13. Do not confuse with capture/render APIs

BlitHook useful for:

- external monitor preview;
- display observer;
- real-time screen/frame consumer tied to AE display.

Not appropriate as primary mechanism for:

- offline deterministic render output;
- file importer/exporter;
- per-layer effect processing;
- 3D composition renderer;
- arbitrary headless rendering.

Use Render Suite/aerender/AEIO/Effect/Artisan according to actual task.

## 14. Borrowed buffer lifetime

The callback receives a host pixel buffer pointer.

Without an explicit ownership/lifetime guarantee beyond the callback:

~~~text
BlitHook receives pixels
→ inspect/copy synchronously
→ return
→ original host pointer is no longer product-owned state
~~~

Do not place the raw host `pixelsPV` pointer into a worker queue.

If downstream processing needs the frame after return, copy into product-owned staging memory before the callback ends.

## 15. Staging buffer design

For an external monitor/streamer, use a bounded staging model:

~~~text
BlitHook
→ validate metadata
→ acquire/reuse product staging slot
→ bounded row-aware copy
→ enqueue product-owned frame descriptor
→ return immediately
→ worker/IPC consumes copy
~~~

Frame descriptor should contain copied metadata, not borrowed pointers:

- width/height;
- pixel format/depth;
- copied row layout;
- view origin/rect;
- timestamp/generation if product defines one;
- product-owned buffer handle/index.

## 16. Backpressure

Display pipeline must not grow an unbounded queue.

Choose product policy explicitly:

- drop newest;
- drop oldest;
- keep latest only;
- bounded wait with strict latency budget.

For preview/monitoring, keeping the latest frame is often more useful than preserving every stale frame, but this is product policy, not an Adobe guarantee.

Record dropped-frame counters so performance failures are visible.

## 17. Row copy discipline

Copy rows using source `row_bytesL` and explicit pixel metadata.

Do not assume:

~~~text
source row bytes == width * packed pixel size
~~~

If product staging uses tightly packed rows, copy each source row into the product layout deliberately.

Validate arithmetic before allocation:

- width/height;
- row bytes;
- plane/channel bytes;
- total copy size;
- integer overflow.

## 18. Blank frame semantics

`pix_bufP0 == NULL` means blank frame.

A product must define what blank means downstream:

- clear external monitor;
- publish explicit blank-frame message;
- drop previous frame and show black;
- keep last frame only if product UX explicitly chooses that behavior.

Do not accidentally reuse the previous pixels because no new buffer arrived.

## 19. View coordinates

Copied pixels and display placement are separate data.

A worker/consumer that ignores:

- full frame size;
- buffer origin;
- visible view rectangle

can place a correct pixel block at the wrong location.

Preserve the coordinate metadata with the staged frame when downstream display depends on it.

## 20. Color/display boundary

BlitHook observes the display pipeline.

Therefore downstream consumer must not infer:

- scene-linear values;
- pre-display color;
- exact Effect world semantics;
- encoded file values.

If product requires color-managed external monitoring, define the intended display/color contract explicitly and qualify it against the actual host/display path.

Do not use BlitHook as a golden pixel oracle for effect math by default.

## 21. Synchronous path

For a simple/safe implementation:

~~~text
callback
→ validate
→ bounded copy/cheap consume
→ return success
~~~

This keeps ownership obvious.

Expensive encode/network/GPU processing happens after the product owns a copy.

## 22. Asynchronous protocol boundary

### Source rereview and concrete safe route — 2026-10-07

Re-read supplied25.6build61 `AE_Hook.h` in full and `GP/EMP/EMP.cpp`.
Header declares completion with receipt/error, but contains no buffer-retention,
completion-thread, cancellation or death-hook ordering contract. EMP remains no-op.
Thus async consumer cannot be derived safely from this source alone; this is a
specific missing vendor contract, not a demand to host-test every Bible example.

A complete **synchronous-copy design** can still avoid this missing protocol:
initialize this callback's output flags to NONE; validate positive signed dimensions
and stride before converting to size_t; accept only supported format/depth/layout
combinations; copy needed rows into owned staging; publish copied metadata; return
without ASYNCHRONOUS and without invoking optional completion for later worker work.
The worker uses only the product copy, so its completion is a product queue event,
not AE_BlitCompleteFunc. Never retain receipt/view/pix-buffer pointers in that queue.

[Portable row-copy reference](https://github.com/ios3kov/AAE-Developer-Bible/blob/main/19-NATIVE-CODE-FOUNDATION/code/monitor_frame_copy.hpp)
demonstrates checked products/offsets, padded-source to packed-destination copying,
byte budget and publish-only-on-success. It preserves channel bytes unchanged;
no swizzle/color transform or enum inference. Its caller must establish readable
source extent from a valid layout/host contract; inventing extent from an unchecked
pointer cannot make it safe. Negative strides and unsupported layouts are rejected
by the adapter policy, not claimed impossible in all hosts. Blank-frame null pointer
is handled before calling this helper (explicit blank message), not a copy error.

[Portable tests](../19-NATIVE-CODE-FOUNDATION/tests/test_monitor_frame_copy.cpp)
cover padding, independent copied storage, truncation, budget, null, short rows,
zero/unsupported layouts and overflow, plus8/16-byte pixels. Example command:

```sh
c++ -std=c++17 -Wall -Wextra -Werror \
  19-NATIVE-CODE-FOUNDATION/tests/test_monitor_frame_copy.cpp \
  -o /path/to/product-build/test_monitor_frame_copy
/path/to/product-build/test_monitor_frame_copy
```

This reference allocates per successful copy; real monitoring should use a bounded
preallocated pool and nonblocking saturation policy. Allocation exceptions must be
caught by the host callback boundary. It is not an exported BlitHook plugin, queue
implementation or performance/AE runtime proof. Death hook must stop/join all
product workers before freeing state or unloading code; a timeout does not authorize
detaching a worker into unloaded plugin code.

The header exposes asynchronous flag + receipt + completion callback, but the supplied sample does not establish the complete pointer/receipt timing model.

Bible therefore does not invent it.

If a concrete product implements asynchronous completion, its design must be derived from verified protocol details and explicitly define:

- which data must be copied;
- receipt lifetime;
- completion exactly-once behavior;
- cancel/shutdown interaction;
- callback-after-shutdown prevention.

Until qualified, prefer the synchronous-copy model.

## 23. Worker / IPC ownership

After staging:

~~~text
product owns frame copy
→ worker or helper owns/borrows according to product protocol
→ release slot/buffer after consumer completion/drop
~~~

Cross-process transport passes copied bytes/shared-memory ownership metadata, never AE process pointers.

## 24. Shutdown / death hook

Recommended order:

~~~text
mark shutting_down
→ stop accepting/enqueueing new product work
→ wake/cancel worker/transport
→ prevent late UI/IPC callbacks into AE
→ drain/drop queued product-owned frames by policy
→ join/stop worker with bounded policy
→ establish no remaining worker/callback can reach staging or hook state
→ free staging buffers
→ return from death hook
~~~

Death hook is `void`; do not throw.

Do not wait indefinitely for remote/network consumers during AE shutdown.
An expired wait budget alone does not make freeing still-reachable state safe.
Keep the simple synchronous-copy route distinct from the unqualified async protocol.

## 25. Reentrancy and state

Keep callback state minimal:

- atomic/locked shutdown flag;
- bounded queue;
- product-owned buffer pool;
- counters/diagnostics.

Do not traverse/mutate AE project from the blit callback.

Do not hold a global product mutex while calling opaque host APIs elsewhere if worker/panel paths can re-enter.

## 26. Performance budget

A display hook has a latency budget.

Measure:

- callback copy time;
- staging allocation/reuse;
- queue contention;
- dropped frames;
- consumer latency;
- preview FPS with hook disabled/enabled.

A functionally correct hook that blocks display playback is not a useful monitor architecture.

## 27. Product validation guidance

If a concrete BlitHook product claims these behaviors, useful runtime cases include:

- callback registration/load;
- blank-frame null buffer;
- 32/64/128 depth;
- ARGB/BGRA handling for the supported host versions;
- non-tight rowbytes;
- view origin/rect;
- rendering/non-rendering flags;
- repeated playback/scrub/cache hits;
- queue saturation/drop policy;
- consumer disconnect;
- shutdown with pending frames;
- macOS + Windows where claimed;
- async path only when based on qualified protocol details.

Measure preview latency/FPS and dropped-frame behavior.

These establish product support evidence. Bible remains SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED unless a separate runtime record exists.

## 28. Anti-patterns

Avoid:

- enqueueing raw `pixelsPV` for later use;
- assuming tight RGBA rows;
- treating null buffer as “reuse previous frame” accidentally;
- blocking network/video encode inside hook;
- unbounded frame queues;
- treating rendering flag as final-render guarantee;
- using BlitHook for deterministic offline render/export;
- inventing async pointer lifetime from the existence of the async flag.

## Related chapters

- [Host call flows](02-HOST-CALL-FLOWS.md)
- [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md)
- [Data ownership](../15-COMMUNICATION/09-DATA-OWNERSHIP.md)
- [Performance architecture](../01-ARCHITECTURE/05-PERFORMANCE-ARCHITECTURE.md)
- [Render frames](../17-NATIVE-SUITE-COOKBOOK/10-RENDER-FRAMES.md)

## Source record

[Native panels and BlitHook SDK 25.6 review](../18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md).
