# Effect recipes

**Suite:** `AEGP_EffectSuite4` (compatibility-oriented documented contract)  
**Confidence:** SDK-verified + sample/community sanity check.

## Перечислить effects на layer

```cpp
A_long count = 0;
ERR(suites.EffectSuite4()->AEGP_GetLayerNumEffects(layerH, &count));

for (A_long i = 0; i < count && !err; ++i) {
    AEGP_EffectRefH effectH = nullptr;
    ERR(suites.EffectSuite4()->AEGP_GetLayerEffectByIndex(
        plugin_id, layerH, i, &effectH));

    // use effectH

    ERR2(suites.EffectSuite4()->AEGP_DisposeEffect(effectH));
}
```

`AEGP_EffectRefH` из `GetLayerEffectByIndex` — disposable reference.

---

## Найти installed effect по match name

```cpp
#include <cstring>

A_Err FindInstalledEffect(
    SPBasicSuite* pica,
    const char* wanted_match_name,
    AEGP_InstalledEffectKey* out_key)
{
    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    AEGP_InstalledEffectKey key = AEGP_InstalledEffectKey_NONE;
    ERR(suites.EffectSuite4()->AEGP_GetNextInstalledEffect(
        AEGP_InstalledEffectKey_NONE, &key));

    while (!err && key != AEGP_InstalledEffectKey_NONE) {
        A_char match_name[AEGP_MAX_EFFECT_MATCH_NAME_SIZE] = {};
        ERR(suites.EffectSuite4()->AEGP_GetEffectMatchName(key, match_name));

        if (!err && std::strcmp(match_name, wanted_match_name) == 0) {
            *out_key = key;
            return A_Err_NONE;
        }

        AEGP_InstalledEffectKey next = AEGP_InstalledEffectKey_NONE;
        ERR(suites.EffectSuite4()->AEGP_GetNextInstalledEffect(key, &next));
        key = next;
    }
    return err ? err : A_Err_GENERIC;
}
```

Использовать **match name**, не локализованный display name.

---

## Применить effect

```cpp
AEGP_InstalledEffectKey key = AEGP_InstalledEffectKey_NONE;
ERR(FindInstalledEffect(pica, "ADBE Gaussian Blur 2", &key));

AEGP_EffectRefH effectH = nullptr;
ERR(suites.EffectSuite4()->AEGP_ApplyEffect(
    plugin_id,
    layerH,
    key,
    &effectH));

// use effectH...
ERR2(suites.EffectSuite4()->AEGP_DisposeEffect(effectH));
```

Не хардкодить installed key между AE sessions. Installed effect key — host enumeration result, не ваш permanent identifier.

---

## Удалить effect

```cpp
ERR(suites.EffectSuite4()->AEGP_DeleteLayerEffect(effectH));
effectH = nullptr;
```

Не `DisposeEffect` после successful delete, если delete уже уничтожил referenced effect; следовать точному ownership контракту SDK/sample вашей версии.

---

## AEGP → ваш Effect plug-in

Если Effect специально поддерживает generic command:

```cpp
MyBridgeMessage msg{};
msg.version = 1;
msg.op = MyBridgeOp::Ping;

A_Time t{0, 1};

ERR(suites.EffectSuite4()->AEGP_EffectCallGeneric(
    plugin_id,
    effectH,
    &t,
    PF_Cmd_COMPLETELY_GENERAL,
    &msg));
```

Effect принимает это в `PF_Cmd_COMPLETELY_GENERAL`.

Обязательно:

- ABI version;
- `struct_size`;
- fixed-width integer fields;
- никаких STL/string/vector через binary boundary;
- ownership явно в протоколе.

См. `16-WORKING-TEMPLATES/effect-aegp-generic-bridge/`.
