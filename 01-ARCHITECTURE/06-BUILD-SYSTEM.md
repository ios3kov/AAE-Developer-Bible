# Build system strategy

## Baseline first

For the first working native plug-in, prefer the build system shipped in Adobe's SDK samples:

- Xcode project on macOS;
- Visual Studio solution/project on Windows.

This preserves PiPL/resource steps and host-specific settings.

## CMake later, not first

CMake can be valuable for a shared core library and cross-platform tests, but don't migrate the host plug-in target until you understand every sample build step.

Good split:

```text
/core          C++ library, platform-neutral, CMake-friendly
/tests         unit/golden tests
/plugin-mac    thin AE adapter/Xcode target
/plugin-win    thin AE adapter/VS target
```

or a carefully engineered unified CMake target once the native builds are proven equivalent.

## Dependencies

Every dependency gets a record:
- license;
- version;
- source/hash;
- mac architectures;
- Windows architectures;
- static/dynamic;
- redistribution requirement;
- thread-safety notes;
- GPU/runtime requirement.

Never discover a missing DLL/dylib only on the customer's machine.
