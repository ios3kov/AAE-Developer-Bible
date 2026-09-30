# PiPL and plug-in loading

PiPL — metadata resource, который Adobe host может прочитать до исполнения plug-in code.

## Cross-platform rule

Держать **один `.r` source** для macOS и Windows. Windows sample projects пропускают `.r` через PiPL tooling/custom build step, чтобы получить ресурс для `.aex`.

Не строить Windows project «с нуля», если можно клонировать Skeleton/sample: именно PiPL build step часто забывают.

## Entry points by architecture

Mac:

```text
CodeMacARM64 {"EffectMain"}
CodeMacIntel64 {"EffectMain"}
```

Windows:

```text
CodeWinARM64 {"EffectMain"}
CodeWin64X86 {"EffectMain"}
```

Нужные строки зависят от фактических targets вашего продукта.

## Consistency

Capabilities/flags в PiPL должны быть согласованы с тем, что plug-in заявляет во время global setup. Несогласованность — источник странных load/render bugs.

## Discovery locations

Common MediaCore используется, когда plug-in должен быть доступен нескольким Adobe hosts.

macOS common:
`/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/`

macOS per-user dev location часто удобнее:
`~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/`

Windows installer должен получать common path по Adobe registry entry, а не предполагать один hardcoded путь для всех версий/конфигураций.

## Load failure checklist

1. Архитектура binary совпадает с host?
2. Bundle/.aex находится в реально сканируемой директории?
3. PiPL собран и содержит нужный entry point?
4. macOS signature валидна?
5. Runtime DLL/dylib dependencies доступны?
6. Нет ли unsupported host/API requirement?
7. Plug-in не падает в global init?
