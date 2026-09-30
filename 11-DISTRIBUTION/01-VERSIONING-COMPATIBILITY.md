# Versioning and compatibility

## Semantic product version

Recommended:

```text
MAJOR.MINOR.PATCH+build
```

Отдельно хранить:
- marketing version;
- binary/build number;
- schema/sequence-data version;
- bridge protocol version, если panel ↔ native.

## Project compatibility

Если старый project содержит effect instance:
- parameter IDs/order должны интерпретироваться правильно;
- sequence data versioned;
- migration deterministic;
- downgrade expectations documented.

## Compatibility statement

Писать:

> Tested with After Effects 25.x and 26.x on macOS arm64 and Windows x64.

а не:

> Works with all After Effects versions.

## Beta versions

Beta smoke tests полезны для раннего detection, но не заменяют GA validation и не должны автоматически менять official support matrix.
