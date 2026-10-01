# BlitHook — display-pipeline frame hook

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Public header in supplied SDK:** `AE_Hook.h`, hook protocol major/minor **3.0**.
**Bundled sample:** `GP/EMP` (External Monitor Preview).
**Verification level:** SDK source-reviewed; no new display-hook host run.

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

## 14. Host acceptance matrix

- callback registration/load;
- blank-frame null buffer;
- 32/64/128 depth;
- ARGB/BGRA handling;
- non-tight rowbytes;
- region origin/view rect;
- rendering/non-rendering flags;
- repeated preview playback;
- scrub/cache hits;
- external consumer backpressure;
- app shutdown;
- async path only if implemented from verified contract;
- macOS + Windows.

Measure preview FPS/latency with hook enabled and disabled. A display hook that is correct but causes dropped frames is not production-ready.

## Source record

[Native panels and BlitHook SDK 25.6 review](../18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md).