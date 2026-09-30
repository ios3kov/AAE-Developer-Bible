# Public SDK docs errata / verification notes

Research snapshot: **2026-09-30**

Публичный C++ SDK Guide — основной reference, но code всегда должен компилироваться против **реальных headers установленного SDK**. В HTML бывают typographical/stale-signature проблемы.

## Подтверждённые/наблюдаемые расхождения

### Project Suite

Публичная страница в одном месте отображает имя:

```text
AEGP_GetProjectProjectByIndex
```

В header-derived bindings и реальном API используется:

```text
AEGP_GetProjectByIndex
```

### Item Suite — CreateNewFolder

В части публичной HTML-документации исторически показывался лишний `AEGP_ProjectH` в сигнатуре. Header/community sample shape современных SDK:

```cpp
AEGP_CreateNewFolder(
    const A_UTF16Char* nameZ,
    AEGP_ItemH parent_folderH0,
    AEGP_ItemH* new_folderPH);
```

### Layer Suite — AddLayer

Некоторые HTML renders показывали третий argument как `A_Boolean*`. Header-derived contract:

```cpp
AEGP_AddLayer(
    AEGP_ItemH itemH,
    AEGP_CompH compH,
    AEGP_LayerH* new_layerPH);
```

## Suite version labels

Не считать заголовок старой секции документации доказательством «latest version». На 26.5 официально подтверждены новые:
- `AEGP_GuideSuite2`;
- `AEGP_ItemViewSuite2`;
- `AEGP_CompSuite13`;
- `AEGP_StreamSuite7`.

Для остальных suite generations source of truth при сборке:
1. SDK headers;
2. `AEGP_SuiteHandler` из той же SDK distribution;
3. official sample compiled from той же версии.

## Policy для Bible

Каждый executable-looking snippet:
- либо проверяется по официальному published signature;
- либо помечается `host-test-required`;
- не выдумывает undocumented struct layout;
- не заявляется binary-tested без AE host.
