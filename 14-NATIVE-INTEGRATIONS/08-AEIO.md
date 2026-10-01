# AEIO — registration and callback lifecycle

Обновлено **2026-10-01** по supplied Adobe After Effects SDK **25.6 build 61**.

Этот раздел — contract-level companion к практической [AEIO chapter](../04-AEIO/README.md). Он описывает registration/lifecycle и границы ownership. Это не новая реализация importer/exporter.

## 1. AEIO регистрируется как AEGP module

PiPL samples `IO`/`FBIO` имеют `Kind { AEGP }` и `EntryPointFunc`. В AEGP initializer module:

1. создаёт/zero-initialize `AEIO_ModuleInfo`;
2. создаёт/zero-initialize `AEIO_FunctionBlock4`;
3. регистрирует необходимые AEGP hooks/lifetime;
4. вызывает `RegisterSuite5::AEGP_RegisterIO(plugin_id, refcon, &info, &funcs)`.

`AEGP_RegisterIO` принимает pointers на ModuleInfo/FunctionBlock, но header alone не следует трактовать как разрешение хранить stack addresses после return; sample использует stack structs во время registration. Host behavior here should be verified through normal registration tests, not by retaining those pointers yourself.

## 2. ModuleInfo и FunctionBlock — разные контракты

`AEIO_ModuleInfo` говорит **что module утверждает, что умеет**. `AEIO_FunctionBlock4` говорит **какие callbacks AE может вызвать**.

Пример согласованности:

```text
ModuleInfo.flags has INPUT
→ InitInSpec/DrawSparseFrame/etc path must be meaningful

ModuleInfo.flags has HAS_AUX_DATA
→ aux descriptor/draw/free callbacks must be coherent

ModuleInfo.flags2 has CAN_DRAW_FLOAT
→ DrawSparseFrame must correctly handle the float-capable host contract
```

Не используйте flags как substitute implementation.

## 3. FunctionBlock4: 49 slots

В SDK 25.6 `AEIO_FunctionBlock4` содержит 49 callbacks и помечен frozen since AE10. Группы:

### Input/spec state

`InitInSpecFromFile`, `InitInSpecInteractive`, `DisposeInSpec`, `FlattenOptions`, `InflateOptions`, `SynchInSpec`, `GetActiveExtent`, `GetInSpecInfo`.

### Input media delivery

`DrawSparseFrame`, `GetDimensions`, `GetDuration`, `GetTime`, `GetSound`, `InqNextFrameTime`.

### Output/spec state

`InitOutputSpec`, `GetFlatOutputOptions`, `DisposeOutputOptions`, `UserOptionsDialog`, `GetOutputInfo`, `OutputInfoChanged`, `SetOutputFile`.

### Output delivery

`StartAdding`, `AddFrame`, `EndAdding`, `OutputFrame`, `WriteLabels`, `GetSizes`, `Flush`, `AddSoundChunk`.

### Capabilities/options

`Idle`, `GetDepths`, `GetOutputSuffix`, `SeqOptionsDlg`.

### Auxiliary media/data

`GetNumAuxChannels`, `GetAuxChannelDesc`, `DrawAuxChannel`, `FreeAuxChannel`, `NumAuxFiles`, `GetNthAuxFileSpec`.

### User data/markers/detection

`CloseSourceFiles`, `CountUserData`, `SetUserData`, `GetUserData`, `AddMarker`, `VerifyFileImportable`, audio options, `AddMarker2/3`, `GetMimeType`.

## 4. IOIn/IOOut suites — current 25.6 generations

`AEGP_IOInSuite7` (version macro 8, frozen 25.3) хранит/читает InSpec metadata: path, depth, duration, dimensions, FPS, alpha, fields, audio, profiles, native timing and CICP.

`AEGP_IOOutSuite6` (version macro 9, frozen 25.2) предоставляет OutSpec configuration/readback: output options, path, dimensions, depth, duration, FPS, audio, labels/color-related data и другие output settings.

Sample IO использует older `IOInSuite4`/`IOOutSuite4`. Это legacy sample generation inside the same SDK; current signatures come from current headers.

## 5. Input options lifecycle

AEIO options — module-owned opaque state attached to host InSpec/OutSpec.

Для input sample sequence:

```text
NewMemHandle(options)
→ Lock
→ fill header/state
→ SetInSpecOptionsHandle
→ Unlock

later:
GetInSpecOptionsHandle
→ read/lock as needed

DisposeInSpec:
GetInSpecOptionsHandle
→ FreeMemHandle
```

FlattenOptions creates a **new flat/disk-safe handle**. It does not free the live non-flat options handle.

`InflateOptions` receives flat options and must construct/set the live non-flat state. Sample IO leaves this unimplemented, so sample is not persistence-complete.

## 6. Sample legacy caveat: old options replacement

IO sample contains an explicit comment telling the sample **not to free the old InSpec options handle** returned from `SetInSpecOptionsHandle`, because old AE code may byte-copy the input options to output on sync.

Bible policy:

- preserve this as historical sample evidence;
- do not generalize it to every custom AEIO state replacement;
- do not silently free it in a copied sample without understanding sync behavior;
- for new production code, create a documented options ownership state machine and host-test save/sync/reload paths.

## 7. Default callback result is semantic

`AEIO_Err_USE_DFLT_CALLBACK` is not ordinary `A_Err_NONE`. It explicitly delegates to host behavior.

Therefore:

```text
return A_Err_NONE
≠
return AEIO_Err_USE_DFLT_CALLBACK
≠
return AEIO_Err_UNIMPLEMENTED
```

Choose based on the callback contract. Sample uses default for many metadata/simple operations; a real format may need to implement them.

## 8. Sparse video callback

`AEIO_DrawSparseFrame` receives:

- `AEIO_InSpecH`;
- quality;
- rational scale;
- time and duration;
- required region;
- interrupt functions;
- output `PF_EffectWorld`;
- drawing flags.

All coordinates are documented in scaled coordinate system. Empty required_region means full. Module flags can additionally declare it cannot clip, in which case capability and implementation must agree.

`AEIO_DFlags_DID_DEINT` and `DID_ALPHA_CONV` tell host what transformations module already performed. Setting them without actually performing conversion is a correctness bug.

## 9. Auxiliary channel lifetime

`DrawAuxChannel` returns `PF_ChannelChunk`. `FreeAuxChannel` is the module callback responsible for paired release. This is **different** from consumer-side `PF_ChannelSuite` checkout/checkin.

Architecture:

```text
AEIO importer produces semantic auxiliary channel
    GetAuxChannelDesc + DrawAuxChannel
             ↓
AE host exposes it to effects
             ↓
PF_ChannelSuite consumer checks it out
```

These are two sides of one pipeline with different ownership callbacks.

## 10. Output state machine

Container/sequence writer should model output explicitly:

```text
UNINITIALIZED
→ OPTIONS_READY
→ FILE_SELECTED
→ ADDING
→ FINALIZED
```

`StartAdding` is where sample reads output dimensions/depth/audio/path and conceptually opens/writes header. `AddFrame`/`AddSoundChunk` append media. `EndAdding` finalizes/close.

On error or cancel, cleanup must be idempotent enough to close file handles and detach temporary state even when normal EndAdding path was not reached.

## 11. Input/output options handles are not raw malloc blocks

Sample allocates them through `AEGP_MemorySuite1`; lock/unlock is explicit. A relocatable handle means:

- cached raw pointer valid only while locked;
- unlock before returning control where required;
- free through Memory Suite, not `free/delete`;
- preserve primary error over cleanup error.

## 12. CICP/ICC in 25.6

Current IOInSuite7 has explicit CICP input color-space setup in addition to ICC profile APIs. This is version-sensitive metadata introduced after the old IO sample's suite generation.

Bible should not teach old IOInSuite4 as complete color-management baseline for AE 25.6.

## 13. Spec state ownership

Treat host spec and module state separately:

```text
AEIO_InSpecH / AEIO_OutSpecH
= host-owned identity/context

module options/private state
= module-owned resource attached through IO suites
```

Do not free the host spec itself.

Do free/close product-owned state according to the callback/options contract.

A useful private-state record tracks:

- initialization phase;
- options schema version;
- file/decoder owner;
- cache owner;
- cancellation generation;
- cleanup-completed flag.

This makes repeated/error disposal idempotent.

## 14. Flatten / inflate boundary

Flat options are persistence/transport representation, not live-state alias.

They must not contain:

- raw pointers;
- file descriptors;
- mutex objects;
- STL object layout;
- process-specific handles.

Inflate validates version/size before reconstructing live state.

If a product changes options schema, migration belongs here.

## 15. Random/sparse callback assumptions

The importer adapter must not assume monotonic frame requests unless the exact format/contract forces that architecture and the module implements seeking/caching.

Treat time, scale, region and quality as explicit request inputs.

If decoder needs temporal dependencies, keep that logic in decoder/index/cache state rather than inventing hidden AE frame-order guarantees.

## 16. Callback cancellation and idempotent cleanup

Any long callback should poll the provided interrupt/cancel mechanism at bounded intervals.

On cancel:

- stop creating new work;
- release callback-local resources;
- leave InSpec/OutSpec in a state that later Dispose/End cleanup can safely handle;
- return cancellation distinctly from corrupt/unsupported data.

Cleanup callbacks should tolerate partial initialization.

## 17. Registration/refcon lifetime

`AEGP_RegisterIO` receives module refcon that can connect callbacks to module-global services.

That refcon must outlive every callback that uses it and be invalidated before product-global teardown.

Do not point refcon at stack/local initialization storage.

## 18. Verification boundary

Source review can prove callback names, signatures and documented ownership. It cannot prove:

- module is discovered;
- extension conflict resolution;
- host chooses expected importer;
- decoder pixels are correct;
- output files are interoperable;
- cancellation closes resources;
- color management is correct in actual project;
- thread behavior/performance.

Those require product-specific runtime evidence only if a developer wants to claim those results; they are not Bible completion requirements.

## Source record

[AEIO/Artisan SDK 25.6 review](../18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).