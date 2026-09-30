# Environment matrix

Перед началом разработки зафиксировать матрицу. Не использовать «последний Mac/Windows» как спецификацию.

| Dimension | macOS | Windows |
|---|---|---|
| IDE | Xcode | Visual Studio |
| Primary CPU | arm64 + x86_64 Universal | x64; ARM64 where supported |
| Native effect suffix/package | bundle/plugin from SDK project | `.aex` |
| Shared plug-in location | `/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/` | registry-driven installer path; common dev path under `Adobe\Common\Plug-ins\7.0\MediaCore` |
| User dev location | `~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/` | usually admin/common path or custom dev copy step |
| Debugger | Xcode / lldb | Visual Studio debugger |
| Signing | codesign + Developer ID | Authenticode / SignTool |
| Release trust | notarization + Gatekeeper | certificate reputation / Windows trust |

## Record for each project

```yaml
product: MyPlugin
min_ae: 25.x
max_tested_ae: 26.x
macos:
  min_os: TBD by product policy
  arch: [arm64, x86_64]
windows:
  arch: [x64]
  arm64: planned-or-supported
gpu:
  mac: enabled-or-none
  windows_cuda: enabled-or-none
  windows_directx: enabled-or-none
mfr: true-or-false
smartfx: true-or-false
premiere_compatible: true-or-false
```

Это становится входом для CI, test matrix и release notes.
