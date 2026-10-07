# macOS — Apple Silicon / Universal binary

A macOS Universal plug-in contains both arm64 and x86_64 machine-code slices in the native executable.

Ship both only if the product still claims both Apple Silicon and Intel support.

## PiPL and binary must agree

For an effect with one entry point, the resource commonly declares both architectures:

~~~text
#if defined(AE_OS_MAC)
  CodeMacARM64 {"EffectMain"},
  CodeMacIntel64 {"EffectMain"},
#endif
~~~

Use the actual entry point of the project.

The resource declaration is not a substitute for the slice. These must agree:

~~~text
PiPL says arm64     <-> executable contains arm64
PiPL says x86_64    <-> executable contains x86_64
~~~

A mismatch is a packaging defect even if compilation succeeded.

## Build

Configure the Xcode target to build arm64 and x86_64 for the release configuration when both are claimed.

Check the finished executable, not only Xcode settings:

~~~bash
lipo -info "/path/to/MyPlugin.plugin/Contents/MacOS/MyPlugin"
~~~

For a Universal release, the expected result contains both arm64 and x86_64.

## Verify the staged artifact

Для конкретного `Products/Skeleton.plugin` используйте
[Skeleton build/inspection route](09-PRODUCTION-BUILD-PIPELINE.md).
`ARCHS='arm64 x86_64' ONLY_ACTIVE_ARCH=NO` задаёт намерение сборки; проверяйте
оба slice, exports, PiPL output и зависимости в произведённом bundle. `nm -gU`
может показать slices раздельно: наличие entry только в одном не закрывает второй.
Повторите inspection после final signing на shipping copy. Resource presence
сама по себе не подтверждает корректность его полей или AE discovery.

Run architecture inspection on the exact bundle that will be signed and packaged.

Do not validate one build directory and then release a separately rebuilt copy.

A useful release manifest records:

~~~json
{
  "platform": "macOS",
  "architectures": ["arm64", "x86_64"],
  "binary_sha256": "...",
  "git_sha": "..."
}
~~~

## Third-party libraries

Every native dependency must support the architectures you claim.

Inspect:

~~~bash
lipo -info path/to/dependency.dylib
otool -L "/path/to/MyPlugin.plugin/Contents/MacOS/MyPlugin"
~~~

Questions to answer:

- is each dependency present for arm64?
- is each dependency present for x86_64 if Intel is claimed?
- are runtime paths valid after packaging?
- is the dependency embedded or expected from the system?
- is every nested code object signed?

A Universal outer bundle containing an x86_64-only dependency is not a working Universal product.

## Avoid accidental architecture loss

Common causes:

- a package manager provides one architecture only;
- a local prebuilt static library is Intel-only;
- a custom build script overwrites a fat binary with one slice;
- release CI builds only the runner's native architecture;
- a post-build helper is missing one slice.

The release gate should inspect the finished artifact recursively where needed.

## Apple Silicon exception boundary

Do not let a C++ exception escape through an exported C host callback.

Conceptually:

~~~cpp
extern "C" PF_Err EffectMain(...) {
    try {
        return Dispatch(...);
    } catch (...) {
        return ConvertToPfError();
    }
}
~~~

The SDK guidance specifically calls out the exception boundary on Apple Silicon. Independently of architecture, containing exceptions at host ABI boundaries is a safer design.

## CPU architecture is not GPU architecture

Universal CPU slices do not prove GPU parity.

Test separately:

- CPU render arm64;
- GPU render arm64;
- CPU render x86_64 if claimed;
- GPU render x86_64 if claimed;
- fallback when a backend is unavailable.

Do not derive GPU support from lipo output.

## Intel deprecation policy

If Intel support is removed:

1. update the support matrix;
2. remove the x86_64 build lane;
3. remove CodeMacIntel64 if the resource no longer has an Intel binary;
4. communicate the last Intel-compatible release;
5. preserve rollback/archive artifacts according to product policy.

Never leave an Intel declaration in PiPL as a historical decoration.

## Verification boundary

The exact final architecture matrix must be proven on the finished signed artifact and loaded in the claimed AE/macOS combinations. Compiler acceptance of both slices alone is insufficient.
