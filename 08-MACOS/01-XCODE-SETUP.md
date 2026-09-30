# macOS — Xcode setup

## Start from SDK sample

Для effect plug-in клонировать Skeleton или ближайший sample из After Effects SDK. Это сохраняет:
- include/library configuration;
- resource/PiPL generation;
- bundle settings;
- host-compatible entry point/export setup;
- architecture config.

## Development output

SDK Guide рекомендует удобный per-user MediaCore path для development:

```text
~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/
```

Это позволяет не писать каждый build внутрь `/Applications` или system `/Library`.

## Xcode scheme

Для Run scheme executable выбрать установленный After Effects. Тогда Build & Run может:
1. собрать plug-in;
2. положить его в dev plug-in location;
3. запустить AE под debugger.

Но debugger attach behavior зависит от версии AE и signing; см. `03-DEBUGGING.md`.

## Build configurations

Рекомендуется минимум:

- `Debug` — symbols, assertions/logging, dev signing;
- `RelWithDebInfo` или `Release-DebugSymbols` — production optimization + symbols archive;
- `Release` — shipping binary.

Хранить `.dSYM` для каждого shipped build по exact build id/version.

## Deployment target

Не выбирать минимальный macOS на глаз. Он должен совпадать с product support policy и реально поддерживаемыми AE versions.

## Warnings

Включать строгие compiler warnings постепенно, но third-party/Adobe headers изолировать так, чтобы warning debt SDK не заставлял отключать warnings во всём собственном коде.
