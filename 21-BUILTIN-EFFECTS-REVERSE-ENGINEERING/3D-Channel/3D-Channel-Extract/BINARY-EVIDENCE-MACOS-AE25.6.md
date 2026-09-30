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


## PiPL → PLUG_RoutineDesc registration bridge proven

The target registration flow is implemented in:

```text
FLTp_FiltSetup(
  dvacore::classref::InterfaceRef<ML::IPiPL>,
  std::u16string const& pluginFilePath,
  dvacore::classref::InterfaceRef<ML::IPlugin>,
  AELibPluginCachedInfos*,
  boost::shared_ptr<FLT_FCSpec>
)
```

Recovered behavior shows that `FLTp_FiltSetup` reads effect metadata from the `IPiPL`, including display name/category/match-name information, populates the `FLT_FCSpec`, and then registers the callable routine.

Two registration paths are present:

```text
PLUG_RegisterRoutine(IPiPL, pluginFilePath)
PLUG_RegisterRoutine(IPiPL, IPlugin)
```

The first path is visible around `0x8e288`, and the second around `0x8e4e0`.

In both cases the returned `boost::shared_ptr<PLUG_RoutineDesc>` is copied into local storage and passed to:

```text
FLT_FCSpec::SetRoutineDescH(...)
```

After that, the already-proven `ReadyFilter()` path prepares the routine and loads `[PLUG_RoutineDesc + 0x08]` into `FLT_FCSpec + 0xD0`, which is later returned by `GetEffectProc()` and invoked by the generic host dispatch.

### Proven host-side registration chain

```text
PiPL metadata
  → FLTp_FiltSetup
  → PLUG_RegisterRoutine(...)
  → PLUG_RoutineDesc
  → FLT_FCSpec::SetRoutineDescH
  → FLT_FCSpec::ReadyFilter
  → [PLUG_RoutineDesc + 0x08]
  → FLT_FCSpec + 0xD0
  → GetEffectProc()
  → PluginDispatch
  → BLR EffectProc
```

### Remaining target-specific step

For **3D Channel Extract / ADBE AUX CHANNEL EXTRACT**, the remaining task is now inside the `PLUG_RegisterRoutine` implementation:

```text
PiPL EntryPointName = FilterMain
→ routine lookup / symbol resolution
→ PLUG_RoutineDesc + 0x08
→ concrete EffectProc address
```

Next: reverse engineer `PLUG_RegisterRoutine` in `PLUG.dylib` and identify how `FilterMain` resolves for hardcoded/bundled effects.


## PLUG registration defers entry-point resolution

Inspection of `PLUG.dylib` shows that both overloads of `PLUG_RegisterRoutine(...)` allocate a `PLUG_RoutineDescPriv` and wrap it in a `boost::shared_ptr<PLUG_RoutineDesc>`.

Observed constructors:

```text
PLUG_RoutineDescPriv(IPiPL, pluginFilePath)
PLUG_RoutineDescPriv(IPiPL, IPlugin)
```

The registration functions themselves do not directly resolve the PiPL entry-point string to a callable address. Instead, `PLUG.dylib` contains dedicated later-stage machinery:

```text
PLUG_PrepRoutine(...)
PLUGp_LoadPlatRoutine(...)
PLUG_RoutineDescPriv::GetEntryPoint(...)
```

This indicates that registration stores the PiPL/plugin metadata first, while actual routine resolution/loading is deferred until preparation.

### Updated proven chain

```text
PiPL
  → FLTp_FiltSetup
  → PLUG_RegisterRoutine(...)
  → PLUG_RoutineDescPriv(IPiPL, path/IPlugin)
  → FLT_FCSpec::SetRoutineDescH
  → FLT_FCSpec::ReadyFilter
  → PLUG_PrepRoutine
  → platform routine loading / entry-point resolution
  → PLUG_RoutineDesc + 0x08
  → FLT_FCSpec + 0xD0
  → GetEffectProc()
  → host BLR
```

### Next target

Reverse engineer:

```text
PLUG_PrepRoutine
PLUGp_LoadPlatRoutine
PLUG_RoutineDescPriv::GetEntryPoint
```

to prove how PiPL `EntryPointName = FilterMain` becomes the concrete function pointer.


## Entry-point name → callable pointer bridge proven

`PLUGp_LoadPlatRoutine(...)` calls:

```text
PLUG_RoutineDescPriv::GetEntryPoint(entryPointName)
```

and immediately stores the returned pointer into the public routine descriptor's callable slot:

```asm
bl   PLUG_RoutineDescPriv::GetEntryPoint(...)
ldr  x8, [x19]
str  x0, [x8, #0x8]
```

Therefore:

```text
PLUG_RoutineDesc + 0x08 = resolved entry-point function pointer
```

Inside `PLUG_RoutineDescPriv::GetEntryPoint(...)`, the plugin-backed path uses the plugin object held by the descriptor and invokes its virtual method at vtable offset `+0x68`. The entry-point-name argument remains in `x1` across that call, the returned function pointer arrives in `x0`, and that result is cached in `PLUG_RoutineDescPriv + 0x08`.

Recovered core:

```asm
ldr  x0, [x19, #0x48]    ; plugin object/interface
ldr  x8, [x0]
ldr  x8, [x8, #0x68]
blr  x8                  ; x1 = requested entry-point name
str  x0, [x19, #0x08]   ; cache resolved function pointer
```

### End-to-end host-side chain now proven

```text
PiPL EntryPointName
  → PLUG_RoutineDescPriv::GetEntryPoint(name)
  → plugin/module entry-point lookup
  → resolved function pointer
  → PLUG_RoutineDesc + 0x08
  → FLT_FCSpec::ReadyFilter
  → FLT_FCSpec + 0xD0
  → GetEffectProc()
  → PluginDispatch[0]
  → BLR
```

For the target PiPL:

```text
ADBE AUX CHANNEL EXTRACT
EntryPointName = FilterMain
```

the remaining target-specific problem is no longer host dispatch. It is to identify which module/plugin object handles this hardcoded PiPL and what concrete address its entry-point lookup returns for `FilterMain`.


## PiPL EntryPointName retrieval proven

The `PLUG_RoutineDescPriv` vtable is located at `0x14920`. Its first virtual method entries resolve as:

```text
vptr + 0x00 → PLUG_RoutineDescPriv::GetKind() const
vptr + 0x08 → PLUG_RoutineDescPriv::GetName() const
vptr + 0x10 → PLUG_RoutineDescPriv::GetMatchName() const
vptr + 0x18 → PLUG_RoutineDescPriv::GetCategory() const
vptr + 0x20 → PLUG_RoutineDescPriv::GetEntryPointName() const
```

The `+0x20` slot points to `0xDEA0`, which is exactly:

```text
PLUG_RoutineDescPriv::GetEntryPointName() const
```

Recovered implementation shows that `GetEntryPointName()` dereferences the stored PiPL interface at `RoutineDescPriv + 0x30/+0x38` and tail-calls the PiPL virtual method at vtable offset `+0x50`.

Therefore the entry-point name used later by `PLUGp_LoadPlatRoutine()` is sourced directly from the PiPL metadata, not synthesized elsewhere.

### Proven target path

For the hardcoded target PiPL:

```text
MatchName      = ADBE AUX CHANNEL EXTRACT
EntryPointName = FilterMain
```

the proven host-side chain is now:

```text
PiPL
  → PLUG_RoutineDescPriv::GetEntryPointName()
  → "FilterMain"
  → PLUG_RoutineDescPriv::GetEntryPoint("FilterMain")
  → resolved function pointer
  → PLUG_RoutineDesc + 0x08
  → FLT_FCSpec::ReadyFilter
  → FLT_FCSpec + 0xD0
  → GetEffectProc()
  → PluginDispatch
  → BLR
```

### Remaining target-specific task

The remaining question is no longer how `FilterMain` is obtained or propagated. It is to identify the **specific module/plugin object backing ADBE AUX CHANNEL EXTRACT** and the exact function address returned for `FilterMain`.

Next: trace the plugin/module object stored in `PLUG_RoutineDescPriv +0x48/+0x50` for the hardcoded 3D Channel Extract PiPL.


## Backing plugin object for RoutineDesc proven

The constructors of `PLUG_RoutineDescPriv` show exactly how fields `+0x48/+0x50` are populated.

### IPiPL + plugin path constructor

For:

```text
PLUG_RoutineDescPriv(IPiPL, pluginFilePath)
```

the constructor:

1. Stores the PiPL interface in the descriptor.
2. Calls `ML::Plugin::CreateClassRef()`.
3. Queries/casts that object to `ML::PluginImpl`.
4. Stores the resulting plugin object/interface at `PLUG_RoutineDescPriv + 0x48/+0x50`.
5. Calls `ML::PluginImpl::SetFullPath(pluginFilePath)`.

Recovered core includes:

```asm
bl   ML::Plugin::CreateClassRef
...
blr  <query/cast to ML::PluginImpl>
...
str  x0, [x19, #0x48]
str  q0, [x19, #0x50]
...
bl   ML::PluginImpl::SetFullPath(...)
```

### IPiPL + IPlugin constructor

For:

```text
PLUG_RoutineDescPriv(IPiPL, IPlugin)
```

the constructor receives an existing plugin object, queries/casts it to `ML::PluginImpl`, and again stores the backing object/interface at `+0x48/+0x50`.

### Consequence for entry-point resolution

The previously recovered `GetEntryPoint(name)` path calls the virtual method at `ML::PluginImpl` vtable offset `+0x68`, so the final symbol resolution is performed by the backing MediaCore/ML plugin object.

Updated chain:

```text
PiPL EntryPointName = "FilterMain"
  → PLUG_RoutineDescPriv
  → backing ML::PluginImpl (+0x48/+0x50)
  → plugin entry-point lookup
  → concrete function pointer
  → PLUG_RoutineDesc +0x08
  → FLT_FCSpec +0xD0
  → host dispatch
```

### Remaining target-specific question

For `ADBE AUX CHANNEL EXTRACT`, determine which `FLTp_FiltSetup` branch is used:

```text
IPiPL + pluginFilePath
or
IPiPL + existing IPlugin
```

and identify the backing module/path that resolves `FilterMain`.
