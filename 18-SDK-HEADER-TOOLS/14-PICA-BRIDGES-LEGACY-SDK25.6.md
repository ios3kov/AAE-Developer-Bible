# SDK 25.6: PICA providers, Effect↔AEGP bridge and legacy boundaries

Date: **2026-10-01**. Source: user-supplied `ae25.6_61.64bit.AfterEffectsSDK`.

**Scope: source review and Bible editing.** No new plug-in build, provider/consumer load test, generic-call host run, unload/reload test, thread stress or Windows host verification was performed.

## Place in the completion plan

This review continues documentation/source-contract work. It does **not** close Gate 2, 3A, 4, 5, 6, 7 or 8. In particular, PICA provider/consumer and Effect↔AEGP remain host-pending integration families.

The SDK TAR SHA-256 was recalculated as:

`eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`

which matches the earlier accepted archive record.

## Reviewed contracts

### SPBasic acquire/release

`Headers/SP/SPBasic.h:80–101` documents name+public-version acquisition, reference-count increment and matching release/decrement. The text allows unloading when the count reaches zero; this is a suite reference-count statement, not a promise that arbitrary provider state is safe to destroy at any time.

### Low-level suite registry

`Headers/SP/SPSuites.h:116–178` distinguishes:

- suite list;
- provider/host reference;
- unique suite name;
- public API version;
- internal version;
- function-table pointer;
- returned suite reference.

Its acquire/release form differs from `SPBasicSuite` because it can specify a list and internal version.

### Sweetie provider pattern

`AEGP/Sweetie/Sweetie.cpp:23–78` publishes a static `DuckSuite1` table to `kSPRuntimeSuiteList` using `AddSuite`.

The sample demonstrates publication, not general hot replacement. It does not show an unregister/unpublish workflow for the DuckSuite, nor safe provider unloading while consumers retain suite acquisitions.

`Util/DuckSuite.h:1–13` supplies the shared name/version/table declaration.

### Checkout consumer pattern

`Effect/Checkout/Checkout.cpp:45–68` acquires `DuckSuite1` with `AEFX_SuiteScoper`, calls it and tolerates absence as a noncritical optional feature.

`Util/AEFX_SuiteHelper.h:73–116` shows the helper acquiring in construction and releasing in destruction. Release status is discarded in the destructor, so products that require cleanup-error evidence need an explicit result-preserving path.

### Current generic Effect call

`Headers/AE_GeneralPlug.h:2162–2168` declares the current `AEGP_EffectSuite4::AEGP_EffectCallGeneric` with plugin id, effect ref, layer-time value, explicit `PF_Cmd` and `void* extra`.

The header explicitly says old behavior is obtained by passing `PF_Cmd_COMPLETELY_GENERAL`.

`Headers/AE_Effect.h:1228–1236` defines that command as the general AEGP-to-effect command.

### Historical generic-call sample

`AEGP/ProjDumper/ProjDumper.cpp:142–168` uses older `EffectSuite2` syntax without the explicit command parameter.

`Effect/Shifter/Shifter.cpp:317–327,555–617` handles `PF_Cmd_COMPLETELY_GENERAL` and treats `extra` as a C string.

This pair is workflow evidence, but not a current signature template or a production binary protocol.

### Historical AEGP initializer sample

Current `AE_GeneralPlug.h:4167–4176` defines `AEGP_PluginInitFuncPrototype` as:

```text
SPBasicSuite*
driver major
driver minor
AEGP_PluginID
AEGP_GlobalRefcon*
```

Bundled `Commando.cpp:140–179` / `Commando.h:44–53` use an older shape containing file/resource path arguments and a plain global-refcon pointer.

The difference is recorded as a **version boundary/source discrepancy**. This review does not claim Commando fails to build or load in the target host because no such run was performed.

## Bible source findings

### SharedSuite.h is C-shaped, but not currently C-source-compatible

Current Bible blob before this review:

`16-WORKING-TEMPLATES/pica-shared-suite/SharedSuite.h`  
blob `5906fae542680a147dc00ab13242b62c8577c90b`

uses `std::int32_t/std::uint64_t`. Therefore the data layout is intentionally simple, but the header is C++-oriented and cannot be advertised as directly includable C source without adaptation.

The README was corrected; the header was not changed in this editorial pass.

### Generic-bridge template lacked the explicit current command/time emphasis

The template documentation was updated to require current `EffectSuite4` call semantics: explicit `PF_Cmd_COMPLETELY_GENERAL` for the historical path, and time in the target layer timebase.

No new host call was made.

## Legacy/native boundary rule

The 25.6 archive itself contains old-generation sample calls next to newer current headers. Therefore:

```text
sample workflow ≠ current ABI signature
```

The exact header used for compilation remains the signature source of truth. Samples remain valuable for call order, ownership clues, UI behavior and historical context.

The review also checked the top-level `Examples/` families. No separate top-level ADM/FPF/Keyframer family was found by those names in the supplied archive. This absence is **not** proof that every historical host capability is removed; it only limits what this archive directly supports as current sample evidence.

## Source identity

| File | SHA-256 |
|---|---|
| `Examples/Headers/SP/SPBasic.h` | `a1258cfd57eedbe5ecbfcebf2bc7df8a3826f495f8e3cc549dce55e60e73395b` |
| `Examples/Headers/SP/SPSuites.h` | `5defdc896c4eee8adee2086faec46660b160804861a74cc077dd9d8db58c5cd3` |
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` |
| `Examples/Headers/AE_Effect.h` | `5432df9bb447cefce2f96c1477d6beccd4686b7236d460c803beab76dae1d537` |
| `Examples/AEGP/Sweetie/Sweetie.cpp` | `f0d87314a2ab983a43c867f8bfa0726d39171428183d024b3c5fdc82c7724e50` |
| `Examples/AEGP/Sweetie/Sweetie.h` | `b0a600cfc6ab4927f6411839c853056055d1be09bdcb4f58b6be0ce55ce33955` |
| `Examples/Util/DuckSuite.h` | `544f9048a2c9dbdbf034ee203b6524469d7fba090c981f8aeaf3de92155408d5` |
| `Examples/Effect/Checkout/Checkout.cpp` | `1e3e4f1813fddae634fcf0048a3a15bfadcd8f64798841434367e3ac85e6d546` |
| `Examples/Util/AEFX_SuiteHelper.h` | `c8773e1eea64a4273bc8744e805324d4dd2f122c87c54c105529a3c61b46a513` |
| `Examples/AEGP/ProjDumper/ProjDumper.cpp` | `99913472c3a0161fe18590e8247beb5b647e692c2a2823bc92e8821c663f9fd8` |
| `Examples/Effect/Shifter/Shifter.cpp` | `e54baa08a5fe1975187fad00455d4ef076d98e4d1e0a66657361e9cf0b79e283` |
| `Examples/AEGP/Commando/Commando.cpp` | `dac982d425b2e79913f9748fb121d8c0bb641e34fe1d405ecfb3cb1678154f04` |
| `Examples/AEGP/Commando/Commando.h` | `ec84ae3aca1127d1603b9daaa5cbefe4c3e9a14b585c1e28ce45d6aca2811302` |

## Documentation changed in this review

- `14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md`
- `14-NATIVE-INTEGRATIONS/11-LEGACY-NATIVE.md`
- `15-COMMUNICATION/03-AEGP-TO-EFFECT.md`
- `15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md`
- `16-WORKING-TEMPLATES/pica-shared-suite/README.md`
- `16-WORKING-TEMPLATES/effect-aegp-generic-bridge/README.md`

## Verification boundary

This review establishes source-backed contracts and discrepancies only.

NOT RUN in this iteration:

- provider registration inside AE;
- effect-side acquire of Bible suite;
- missing/wrong-version behavior in AE;
- refcount/unload behavior;
- generic call to a Bible effect;
- timebase host test;
- provider/consumer concurrency;
- restart/shutdown stress;
- exact-SDK compilation of the two Bible bridge templates;
- Windows host behavior.

These are optional future implementation/runtime evidence areas, not Bible completion requirements.
