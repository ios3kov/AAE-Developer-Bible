# 3D Channel Extract — macOS binary investigation

Status: **active / evidence captured**  
Host: Adobe After Effects **25.6.0 (25.6.0.101)**  
Platform: macOS, arm64  
Target: **3D Channel Extract**

## Confirmed registration evidence

After Effects ships a centralized hardcoded PiPL registry at:

`Contents/Frameworks/aelib.framework/Versions/A/Resources/txt/hardcodedpipls.txt`

The record for this effect contains:

```text
Category: 3D Channel
Entry point name: FilterMain
Match name: ADBE AUX CHANNEL EXTRACT
Display name: 3D Channel Extract
OutFlags: 33588288
OutFlags2: 134222848
ReservedInfo: 1
Virtual full path: Plug-Ins/Effects/Aux_Channel_Extract
GPUEntry: ""
```

The virtual path does **not** exist as a physical plug-in directory in the inspected AE 25.6 installation. Therefore `mFullPath` must not be treated as evidence of a standalone file.

## Internal effect subsystem evidence

The application contains:

`Contents/Frameworks/FLT.dylib`

Observed properties:

- arm64 Mach-O dylib;
- approximately 1.8 MB;
- contains a large set of native After Effects match-name strings;
- contains `ADBE AUX CHANNEL`;
- contains the related 3D-channel identifiers:
  - `ADBE DEPTH MATTE`
  - `ADBE DEPTH FIELD`
  - `ADBE FOG_3D`
  - `ADBE ID MATTE`

It also contains many other built-in effect identifiers including Gaussian Blur, Curves, Levels, Hue/Saturation, Exposure, audio effects, expression controls and many more. This establishes FLT as a major internal effect subsystem, not a module specific to one effect.

### Important identifier distinction

The hardcoded PiPL record uses:

`ADBE AUX CHANNEL EXTRACT`

FLT contains:

`ADBE AUX CHANNEL`

These are related evidence, but they are **not identical strings**. Until registration/dispatch mapping is traced, do not state that the latter alone proves the exact implementation function for 3D Channel Extract.

## Preserved build/debug metadata

`nm -a FLT.dylib` exposes extensive build metadata rather than being fully stripped.

Observed Adobe internal source/object names include:

```text
AfterEffects/src/pkg/FLT/indep/
FLT.o
FLT_Arbitrary.o
FLT_Audio.o
FLT_Blur.o
FLT_Callback.o
FLT_CompoundEffect.o
FLT_Context.o
FLT_Disk.o
FLT_ErrCallback.o
FLT_FilterCrashHandler.o
FLT_Fr.o
FLT_Host.o
FLT_Nodes.o
FLT_Parade.o
FLT_Params.o
FLT_Seq.o
FLT_SequenceData.o
FLT_Strs.o
FLT_Suites.o
FLT_UI.o
FLT_Utils.o
FLTp_AEComponentParam.o
FLTp_Callback.o
FLTp_Convert.o
FLTp_Err.o
FLTp_In.o
FLTp_NativeEffectList.o
FLTp_SeqRenderState.o
FLTp_Setup.o
FLTp_Util.o
Manager.o
GPUEffectUtils_AE.o
```

Source filenames visible in symbol metadata include:

```text
FLTp_NativeEffectList.cpp
FLT_CompoundEffect.cpp
FLT_FilterCrashHandler.cpp
GPUEffectUtils_AE.cpp
```

This is strong evidence for the internal architecture and gives useful anchors for further disassembly.

## Relevant recovered symbols

Important FLT symbols observed:

```text
FLT_PreLoadEffect(unsigned char const*)
FLTp_AddEffect(boost::shared_ptr<FLT_FCSpec>)
FLTp_ReadyFilter(boost::shared_ptr<FLT_FCSpec>)
FLTp_UnreadyFilter(boost::shared_ptr<FLT_FCSpec>)
FLTp_FindFilterIndex(unsigned char const*)
FLTp_IsInternalEffect(unsigned char const*)
FLTp_DispatchFilters(...)
FLT_CreateEffects(...)
FLT_CreateFilterNode(...)
FLT_EffectSupportsGPUSDK(...)
FLT_EffectCanRenderAtDepth(...)
FLT_GetNumThreadsRenderingEffects()
FLT_FCSpec::SetEffectProc(int (*)())
FLT_FCSpec::GetEffectProc() const
FLT_FCSpec::SetIsInternalEffect(bool)
FLT_FCSpec::GetIsInternalEffect() const
```

Also observed:

```text
FLTp_CheckoutDepth(...)
FLTp_BaseNode::CanRenderNativelyAtDepth(...)
FLTp_RenderNode::ComputeInputBitDepth()
AEGPURenderRequest::FixBitDepth(...)
GPUEffectMatchNameMapping()
```

## EffectProc investigation

`FLT_FCSpec::SetEffectProc` stores the function pointer at object offset `0xd0`.

Only three direct call sites to `SetEffectProc` were observed in the FLT disassembly. Their function pointers resolve to the special handlers around:

- `0x99b74`
- `0x99b58`
- `0x9a048`

The surrounding symbols/flow identify these as special Missing/Compound/Pseudo-effect registration paths, not evidence of an individual native procedure for 3D Channel Extract.

### Current architecture inference

**RECONSTRUCTED, not yet proven for this exact effect:**

```text
hardcoded PiPL
→ FLT registry / FLT_FCSpec
→ native/internal classification
→ FLTp_DispatchFilters
→ native effect index/table or equivalent dispatch mechanism
→ concrete built-in effect implementation
```

The next task is to prove the final mapping:

`ADBE AUX CHANNEL EXTRACT / ADBE AUX CHANNEL → native index/table → concrete code path`.

## String/xref investigation

Exact file offsets found in `FLT.dylib`:

```text
ADBE AUX CHANNEL  -> 0xC0BB0
ADBE DEPTH MATTE  -> 0xC9A1F
ADBE DEPTH FIELD  -> 0xC9A0E
ADBE FOG_3D       -> 0xC9BC7
```

No direct absolute 64-bit pointer to `0xC0BB0` was found in the file, and no simple direct ARM64 `ADRP + ADD` xref was identified with the initial search. This suggests the identifier may participate in runtime-built structures, relative references, relocations, or another indirection mechanism.

Do not interpret the absence of a simple xref as absence of an implementation.

## Classification status

| Field | Current status |
|---|---|
| Display name | **PROVEN:** 3D Channel Extract |
| Match name | **PROVEN:** ADBE AUX CHANNEL EXTRACT |
| PiPL registration | **PROVEN:** hardcoded registry |
| Standalone plugin path | **PROVEN absent** at recorded virtual path |
| Implementation class | **HOST-BUILTIN: strong evidence; final exact code-path mapping pending** |
| Internal subsystem | **PROVEN:** FLT is a native effect subsystem; target-family identifiers present |
| Exact implementation function | **UNKNOWN** |
| GPU entry in hardcoded PiPL | **PROVEN empty** |
| Actual runtime GPU behavior | **UNKNOWN / runtime test required** |
| Algorithm | **UNKNOWN** |

## Next investigation step

Disassemble and trace `FLTp_DispatchFilters` and its associated native effect lookup/index structures.

Goal:

```text
AUX CHANNEL identifier
→ FLT native effect record/index
→ dispatch branch/function pointer
→ concrete implementation
```

Only after that mapping is proven should algorithm reconstruction begin.


## Dispatch path evidence — FLTHost / GenericPluginDispatch

Further disassembly establishes an additional host-side dispatch layer.

### Confirmed symbols

```text
FLTp_DispatchFilter(...)                    @ 0x98494
FLTHost::DispatchFilter(...)                @ 0x38d60
FLT_FCSpec::GetEffectProc() const           @ 0x5e2f0
FLT_FCSpec::SetEffectProc(int (*)())        @ 0x5d0f8
```

### Confirmed call chain

Inside `FLTp_DispatchFilter`, execution reaches:

```text
FLTHost::DispatchFilter(...)
```

Inside `FLTHost::DispatchFilter`, the host:

1. obtains data from the `IFilterSpec` through virtual methods;
2. constructs `U_GenericPluginDispatch<FLTHost::PluginDispatch>`;
3. obtains effect metadata used for dispatch/reporting, including match name, display name and effect version;
4. marks execution through `FLT_FilterCrashHandler::NotifyExecutingPluginCode`;
5. invokes `DispatchWithOptionalMachineExceptionSupport(...)`;
6. reports completion through `NotifyDoneExecutingPluginCode`.

Relevant diagnostic literals in this path include:

```text
effectMatchName
effectDisplayName
effectVersion
selector
```

This proves that the native FLT route is wrapped in the same generic plugin-dispatch/error-containment infrastructure before the concrete effect code is executed.

### Important correction to earlier working hypothesis

No direct call to `FLT_FCSpec::GetEffectProc()` was observed inside the recovered body of `FLTHost::DispatchFilter`.

Therefore the currently supported path is:

```text
hardcoded PiPL / effect registration
    ↓
FLT registry / FLT_FCSpec
    ↓
FLTp_DispatchFilter
    ↓
FLTHost::DispatchFilter
    ↓
U_GenericPluginDispatch<FLTHost::PluginDispatch>
    ↓
DispatchWithOptionalMachineExceptionSupport
    ↓
[concrete PluginDispatch/native callback resolution — NEXT TARGET]
```

Do **not** yet claim that `FLTHost::DispatchFilter` itself directly calls the stored `EffectProc`.

### Next reverse-engineering target

Recover `FLTHost::PluginDispatch` and the generic dispatcher call operator to determine exactly where the concrete native callback is selected/invoked.

Goal remains:

```text
ADBE AUX CHANNEL / ADBE AUX CHANNEL EXTRACT
→ FLT effect record
→ concrete native callback
→ implementation
```


## Concrete generic-dispatch invocation recovered

Further ARM64 disassembly identifies the actual indirect invocation performed by `U_GenericPluginDispatch<FLTHost::PluginDispatch>`.

### Machine-exception path

Inside `DispatchWithMachineExceptionSupport_Impl`:

```asm
0x3b51c  ldr x8, [x21]
0x3b520  ldr w0, [x21, #0x8]
0x3b524  ldp x1, x2, [x21, #0x10]
0x3b528  ldp x3, x4, [x21, #0x20]
0x3b52c  ldr x5, [x21, #0x30]
0x3b530  blr x8
```

### Crash-info path

Inside `DispatchWithCrashInfo_Impl`:

```asm
0x3b8cc  ldr x8, [x19]
0x3b8d0  ldr w0, [x19, #0x8]
0x3b8d4  ldp x1, x2, [x19, #0x10]
0x3b8d8  ldp x3, x4, [x19, #0x20]
0x3b8dc  ldr x5, [x19, #0x30]
0x3b8e0  blr x8
```

This proves that the generic dispatch wrapper stores a callable target in the first machine word of its `PluginDispatch` payload and invokes it indirectly with six arguments reconstructed from the payload.

### Correction

The previously inspected lambda at `0x3d4b0` is **not** the effect callback. It builds crash diagnostic context (`U_GenericPluginDispatch.h`, `crash`, `Crashed with context`).

### Updated proven chain

```text
hardcoded PiPL / FLT registration
→ FLTp_DispatchFilter
→ FLTHost::DispatchFilter
→ U_GenericPluginDispatch<FLTHost::PluginDispatch>
→ optional machine-exception / crash-context wrapper
→ indirect callable invocation via BLR
```

### Remaining unknown

The `BLR` target above is the callable stored in the `PluginDispatch` payload. We still need to trace **where that first word is initialized** and determine whether it is:

1. `FLTHost::PluginDispatch::operator()` / an equivalent static thunk, which then resolves `FLT_FCSpec::GetEffectProc()`; or
2. the concrete effect procedure itself.

Next target: trace construction/copy of `FLTHost::PluginDispatch` into `U_GenericPluginDispatch` and identify the value placed at payload offset `+0x0`.


## EffectProc dispatch chain proven end-to-end

The `FLT_FCSpec` vtable is located at `0xD5C70`. After the Itanium C++ ABI vtable header and destructor entries, the virtual slot used by `FLTHost::DispatchFilter` resolves to:

```text
0x5E2F0  FLT_FCSpec::GetEffectProc() const
```

Recovered implementation:

```asm
0x5e2f0  add  x8, x0, #0xd0
0x5e2f4  ldar x0, [x8]
0x5e2f8  ret
```

Therefore `GetEffectProc()` atomically loads the stored effect procedure pointer from `FLT_FCSpec + 0xD0`.

Earlier disassembly of `FLTHost::DispatchFilter` showed the virtual call result being placed into the first word of the `PluginDispatch` payload. `U_GenericPluginDispatch` copies that payload unchanged, and its protected dispatch paths later execute the first word through `BLR`.

### Proven chain

```text
FLT_FCSpec
  → virtual GetEffectProc()
  → atomic load [FLT_FCSpec + 0xD0]
  → PluginDispatch[0]
  → U_GenericPluginDispatch copies PluginDispatch unchanged
  → machine-exception / crash-context wrapper
  → BLR PluginDispatch[0]
  → concrete EffectProc
```

This closes the previously unknown host-dispatch bridge.

### What remains unknown

This proves **how After Effects invokes the concrete effect procedure**, but does not yet identify the procedure stored at `+0xD0` specifically for **3D Channel Extract / ADBE AUX CHANNEL EXTRACT**.

Next target:

```text
ADBE AUX CHANNEL EXTRACT
→ its FLT_FCSpec instance
→ value stored at FCSpec + 0xD0
→ concrete EffectProc address
→ disassembly / algorithm reconstruction
```


## RoutineDesc → EffectProc mapping proven

`FLT_FCSpec::ReadyFilter()` establishes exactly how the concrete effect procedure is populated.

Relevant recovered flow:

```asm
0x5cf1c  ldp  x21, x20, [x19, #0xc0]   ; shared_ptr<PLUG_RoutineDesc>
...
0x5cf9c  add  x0, sp, #0x8
0x5cfa0  bl   PLUG_PrepRoutine(...)
...
0x5d020  ldp  x8, x20, [x19, #0xc0]    ; x8 = PLUG_RoutineDesc*
...
0x5d034  ldr  x8, [x8, #0x8]           ; routine entry pointer
0x5d038  add  x10, x19, #0xd0
0x5d03c  swpal x8, x8, [x10]            ; store EffectProc atomically
```

The same direct load/store path is used when there is no shared_ptr control block.

### Proven structure relationship

```text
FLT_FCSpec + 0xC0
  → PLUG_RoutineDesc*
PLUG_RoutineDesc + 0x08
  → concrete routine entry pointer
FLT_FCSpec::ReadyFilter()
  → PLUG_PrepRoutine(RoutineDesc)
  → loads [RoutineDesc + 0x08]
  → stores it atomically at [FLT_FCSpec + 0xD0]
FLT_FCSpec::GetEffectProc()
  → returns [FLT_FCSpec + 0xD0]
FLTHost dispatch
  → invokes that pointer through BLR
```

This closes the full host-side path from a prepared `PLUG_RoutineDesc` to the actual effect callback.

### Remaining target-specific gap

For **3D Channel Extract**, we still need to map:

```text
hardcoded PiPL:
  MatchName = ADBE AUX CHANNEL EXTRACT
  EntryPointName = FilterMain
→ PLUG_RoutineDesc instance
→ [RoutineDesc + 0x08]
→ concrete EffectProc address
```

Next step: trace where `FLT_FCSpec + 0xC0` / `SetRoutineDescH()` is populated during registration/loading.
