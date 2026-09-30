# After Effects -> AEGP

AEGP имеет два этапа.

## 1. Registration

AE вызывает entry point один раз при launch:

```cpp
A_Err EntryPointFunc(
    SPBasicSuite* pica_basicP,
    A_long major_versionL,
    A_long minor_versionL,
    AEGP_PluginID aegp_plugin_id,
    AEGP_GlobalRefcon* global_refconP);
```

Здесь регистрируются hooks/специализации.

## 2. Host callbacks

После entry point AE вызывает зарегистрированные функции:

- command hook;
- update-menu hook;
- idle hook;
- death hook;
- AEIO callbacks;
- Artisan callbacks;
- panel callbacks;
- другие documented hooks.

Внутри callback plug-in обращается к AE через PICA suites.

## Load-order rule

AEGP modules не гарантируют порядок загрузки. Не acquire чужой third-party suite в entry point, если его provider мог ещё не загрузиться. Делать acquire в момент фактического использования и поддерживать отсутствие dependency.
