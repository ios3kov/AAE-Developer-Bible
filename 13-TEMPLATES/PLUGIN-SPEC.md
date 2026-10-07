# Plug-in specification template

## 1. Product identity

Filled [Gain specification/evidence pack](examples/WORKED-EXAMPLE.md): actual
8/16-bpc source, disk ID1, no sequence/arbitrary state, no float/MFR/GPU claim.
Reader release identities and host observations remain NOT_RUN.

- Name:
- Codename:
- Version target:
- Owner:
- Repository:
- Primary user:
- Release channel:

## 2. Problem

What artist/user problem is solved?

What is explicitly out of scope?

## 3. Extension architecture

Select all shipped components:

- [ ] Effect
- [ ] AEGP
- [ ] AEIO
- [ ] Artisan
- [ ] Native panel
- [ ] ExtendScript
- [ ] ScriptUI
- [ ] CEP
- [ ] UXP when AE support is verified
- [ ] Helper/service
- [ ] Hybrid

Why is each component needed?

~~~text
UI
→ automation/bridge
→ native/core
→ After Effects
~~~

Document the actual flow.

## 4. Support matrix

### After Effects

- Minimum supported:
- Newest tested GA:
- Beta observations:
- Unsupported:

### macOS

- Minimum OS:
- arm64:
- x86_64:
- Rosetta behavior if relevant:
- GPU backends:

### Windows

- Minimum OS:
- x64:
- ARM64:
- GPU backends:

Every tested claim must eventually map to a compatibility-matrix evidence record.

## 5. SDK/toolchain baseline

- Adobe SDK:
- Xcode:
- macOS SDK/deployment target:
- Visual Studio:
- MSVC toolset:
- Windows SDK:
- C++ language level:
- Third-party dependency lock/version policy:

## 6. Entry/registration

For native component:

- plug-in family/kind:
- entry point:
- PiPL architecture declarations:
- category/display name:
- stable match name:
- suite generations required:
- fallback if a suite is absent:

## 7. Render contract

- 8-bpc:
- 16-bpc:
- 32-bpc:
- alpha semantics:
- SmartFX:
- ROI/origin behavior:
- temporal dependencies:
- auxiliary channels:
- audio if any:
- CPU fallback:

## 8. MFR/threading

- MFR claimed:
- mutable globals:
- global_data writes:
- sequence_data use:
- Compute Cache:
- thread-local/frame-local scratch:
- locks:
- third-party thread-safety evidence:
- host calls made while locks held:
- cancellation behavior:

## 9. GPU

- backends:
- capability flags:
- gpu_data owner/lifetime:
- setup/setdown:
- CPU oracle:
- comparison tolerance:
- fallback:
- device-loss/error policy:

## 10. Persistent state

- parameter IDs:
- parameter semantics:
- sequence/arbitrary data schema:
- current schema version:
- migration from:
- corrupt/unknown version behavior:
- cache vs persistent truth:

Never use compiler-dependent raw C++ objects as a persistence format.

## 11. Communication/protocol

For panel/native/helper products:

- protocol version:
- minimum compatible version:
- request ID:
- generation/stale-response rule:
- error envelope:
- max message size:
- command allowlist:
- control plane:
- data plane:
- cancellation:
- timeout/liveness:

## 12. UI

- standard effect params:
- custom effect UI/Drawbot:
- native panel:
- ScriptUI:
- CEP:
- future UXP migration boundary:
- localization:
- accessibility/key navigation:

## 13. Files/network/security

- filesystem access:
- network endpoints:
- downloaded data:
- downloaded executable code:
- helper IPC:
- secrets:
- update trust/signature policy:
- telemetry/privacy policy:

## 14. Licensing

- entitlement states:
- offline policy:
- server outage behavior:
- render farm/headless policy:
- render hot-path dependency: must be none unless explicitly justified and safe
- user-facing recovery:

## 15. Performance budget

Define target workloads before optimization.

- target frame/resolution:
- target median:
- p95:
- memory peak:
- cache budget:
- panel latency:
- regression threshold:

## 16. Failure behavior

Define expected behavior for:

- unsupported host;
- missing suite;
- unsupported GPU;
- allocation failure;
- corrupt project state;
- missing helper;
- component version mismatch;
- network unavailable;
- license unavailable;
- cancellation;
- AE shutdown during work.

## 17. Build/distribution

### macOS

- architectures:
- Developer ID identity:
- notarization:
- package:
- install path policy:
- dSYM archive:

### Windows

- architectures:
- Authenticode:
- package/installer:
- install path/registry policy:
- PDB archive:

## 18. Test plan

- pure unit:
- adapter/contract:
- native compile/link:
- PiPL/resource:
- golden render:
- bit depths:
- alpha:
- ROI/origins:
- MFR stress:
- GPU equivalence:
- save/reopen:
- migration:
- panel/bridge:
- installer fresh/upgrade/uninstall:
- cross-version/platform:
- crash/recovery:
- performance:

## 19. Acceptance criteria

A capability is accepted only when:

~~~text
claim
→ named test
→ exact artifact/environment
→ observable assertion
→ retained evidence
~~~

List release-blocking gates here.

## 20. Open risks / unknowns

| Risk/unknown | Evidence needed | Owner | Blocking? |
|---|---|---|---|
| | | | |

Do not hide unknowns inside optimistic support statements.
