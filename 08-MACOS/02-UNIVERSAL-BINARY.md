# macOS — Apple Silicon / Universal binary

After Effects SDK Guide указывает, что Universal build требует arm64 + Intel slice и соответствующие PiPL entry declarations.

## PiPL

Для одного entry point:

```text
#if defined(AE_OS_MAC)
  CodeMacARM64 {"EffectMain"},
  CodeMacIntel64 {"EffectMain"},
#endif
```

Использовать фактический entry point вашего sample/project.

## Build

Xcode target должен собирать `arm64` и `x86_64` для Universal artifact, если оба заявлены.

Проверка:

```bash
lipo -info /path/to/MyPlugin.plugin/Contents/MacOS/MyPlugin
```

Ожидается список обеих architectures для Universal release.

## Apple Silicon exception boundary

SDK Guide отдельно предупреждает: не позволять C++ exception пройти через C entry point. На Apple Silicon это может закончиться `terminate()`.

Правило:

```cpp
extern "C" PF_Err EffectMain(...) {
    try {
        return Dispatch(...);
    } catch (...) {
        return ConvertToPfError();
    }
}
```

## Third-party libraries

Каждая linked static/dynamic dependency также должна иметь нужный architecture slice. Universal plug-in с x86_64-only dylib всё равно сломан на arm64.

Проверять:
- `lipo -info`;
- `otool -L`;
- actual load on clean Apple Silicon machine.

## Intel deprecation policy

Если в будущем Intel support убирается:
- поднять major/minor support statement;
- явно предупредить пользователей;
- не оставлять `CodeMacIntel64` в PiPL, если binary больше не содержит slice;
- сохранить последний Intel-compatible installer в archive policy, если бизнес этого требует.
