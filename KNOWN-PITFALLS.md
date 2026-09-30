# Known pitfalls

## Native C++

- Creating a project from scratch and forgetting the PiPL build step.
- PiPL flags disagree with flags returned during `PF_Cmd_GLOBAL_SETUP`.
- Exception leaks through an `extern "C"` boundary; especially dangerous on Apple Silicon.
- Static/global mutable state makes an effect unsafe under MFR.
- Writing `sequence_data` during render without using the correct MFR-safe mechanism.
- Holding a mutex while calling host suites/checkouts — deadlock risk.
- Caching pointers/handles longer than their documented lifetime.
- Assuming rowbytes equals width × pixel size.
- Assuming 8-bpc only and then corrupting 16/32-bpc output.
- Assuming a GPU path exists just because a GPU is present.
- CPU and GPU paths diverge numerically or in edge behavior.
- Using a suite version without checking/acquiring it correctly.

## macOS

- Shipping Intel-only binary.
- Forgetting `CodeMacARM64` in PiPL.
- Unsigned plug-in no longer loads on macOS 15+ development setups.
- Modifying a bundle after signing.
- Notarizing with obsolete `altool` instead of `notarytool`.
- Attempting debugger attach to current non-Beta AE without accounting for AE 26.5+ signing restrictions.

## Windows

- Hardcoding MediaCore path instead of reading installer registry path when appropriate.
- Missing PiPL resource generation in Visual Studio custom build step.
- Forgetting `CodeWinARM64` for ARM64 build.
- Signing without explicit SHA-256 digest/timestamp parameters.
- Shipping CUDA runtime dependency that doesn't match your loading strategy.
- Forgetting DirectX assets generated next to the effect binary.

## CEP / panels

- Putting core product logic directly inside panel UI code.
- Depending on Node/CEF behavior that will not port cleanly to UXP.
- Forgetting to bump/debug the correct `CSXS.<version>` setting.
- Treating CEP's future as indefinite despite Adobe's published migration timeline.

## Release

- Testing only the newest AE version.
- Testing only one CPU architecture.
- Testing only GPU-enabled path.
- No project with extreme parameter/keyframe values.
- No MFR on/off comparison.
- No clean-machine install test.
- No uninstall/upgrade test.
