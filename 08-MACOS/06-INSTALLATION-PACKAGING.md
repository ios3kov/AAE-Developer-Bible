# macOS — installation and packaging

## Common location

Для plug-ins, которые должны быть доступны совместимым Adobe video hosts:

```text
/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/
```

CC использует historical `7.0` directory convention.

## AE-only location

Если plug-in принципиально AE-specific:

```text
/Applications/Adobe After Effects [version]/Plug-ins/
```

Но installer, привязанный к app bundle/version path, требует больше maintenance при нескольких AE versions.

## User dev path

Для development удобно:

```text
~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/
```

Release installer обычно использует system-level policy продукта.

## Packaging choices

- `.pkg` — хороший системный installer path;
- signed/notarized `.dmg` как delivery container;
- zip — только если manual install действительно является product decision.

## Installer rules

- no hidden destructive cleanup;
- upgrade keeps user presets/license data unless explicitly intended;
- uninstall removes only files owned by your product;
- support side-by-side old/new only if designed;
- log install result/path/version;
- verify architecture and supported OS before install where appropriate.
