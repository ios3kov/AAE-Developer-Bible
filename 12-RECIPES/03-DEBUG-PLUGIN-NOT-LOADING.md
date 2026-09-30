# Recipe — plug-in does not load

## 1. File is discovered?

- correct folder;
- folder actually scanned;
- no accidental disabled folder naming convention;
- right package suffix/layout.

## 2. Architecture?

macOS:
```bash
lipo -info MyPlugin.plugin/Contents/MacOS/MyPlugin
```

Windows:
- inspect PE architecture/dependencies.

## 3. PiPL?

- resource present;
- correct entry point;
- correct architecture entry declaration;
- PiPL flags match runtime setup.

## 4. Signing?

macOS:
```bash
codesign -vvv --deep --strict MyPlugin.plugin
```

Windows:
```bat
signtool verify /pa /v MyPlugin.aex
```

## 5. Dependencies?

- missing dylib/DLL;
- wrong architecture;
- wrong runtime library;
- missing GPU assets.

## 6. Initialization crash?

Attach debugger before/at launch or inspect crash report. Minimize global constructors; defer optional subsystem init until needed.
