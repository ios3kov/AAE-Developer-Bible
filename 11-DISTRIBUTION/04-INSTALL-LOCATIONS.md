# Install locations cheat sheet

## Native C++ — macOS

Common MediaCore:

```text
/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/
```

Per-user development:

```text
~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/
```

AE-specific:

```text
/Applications/Adobe After Effects [version]/Plug-ins/
```

## Native C++ — Windows

Installer should use Adobe registry path guidance:

```text
HKLM\SOFTWARE\Adobe\After Effects\[version]\CommonPluginInstallPath
```

Typical common dev path:

```text
C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\
```

## CEP — macOS

System:

```text
/Library/Application Support/Adobe/CEP/extensions
```

User:

```text
~/Library/Application Support/Adobe/CEP/extensions
```

## CEP — Windows

System:

```text
C:\Program Files (x86)\Common Files\Adobe\CEP\extensions
```

User:

```text
%AppData%\Roaming\Adobe\CEP\extensions
```

Paths are version/platform sensitive. Installer code should prefer official registry/platform rules over string guessing.
