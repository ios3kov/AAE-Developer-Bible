#include <cstring>

#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"

A_Err Bible_FindInstalledEffect(
    SPBasicSuite* pica,
    const char* match_nameZ,
    AEGP_InstalledEffectKey* keyP)
{
    if (!pica || !match_nameZ || !keyP) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    *keyP = AEGP_InstalledEffectKey_NONE;

    AEGP_InstalledEffectKey key = AEGP_InstalledEffectKey_NONE;
    ERR(suites.EffectSuite4()->AEGP_GetNextInstalledEffect(
        AEGP_InstalledEffectKey_NONE, &key));

    while (!err && key != AEGP_InstalledEffectKey_NONE) {
        A_char current[AEGP_MAX_EFFECT_MATCH_NAME_SIZE] = {};
        ERR(suites.EffectSuite4()->AEGP_GetEffectMatchName(
            key, current));

        if (!err && std::strcmp(current, match_nameZ) == 0) {
            *keyP = key;
            return A_Err_NONE;
        }

        AEGP_InstalledEffectKey next = AEGP_InstalledEffectKey_NONE;
        ERR(suites.EffectSuite4()->AEGP_GetNextInstalledEffect(
            key, &next));
        key = next;
    }

    return err ? err : A_Err_GENERIC;
}

A_Err Bible_ApplyEffect(
    SPBasicSuite* pica,
    AEGP_PluginID plugin_id,
    AEGP_LayerH layerH,
    const char* match_nameZ)
{
    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    AEGP_InstalledEffectKey key = AEGP_InstalledEffectKey_NONE;
    ERR(Bible_FindInstalledEffect(pica, match_nameZ, &key));

    AEGP_EffectRefH effectH = nullptr;
    if (!err) {
        ERR(suites.EffectSuite4()->AEGP_ApplyEffect(
            plugin_id, layerH, key, &effectH));
    }

    if (effectH) {
        ERR2(suites.EffectSuite4()->AEGP_DisposeEffect(effectH));
    }
    return err;
}

A_Err Bible_SetStaticOneD(
    SPBasicSuite* pica,
    AEGP_PluginID plugin_id,
    AEGP_StreamRefH streamH,
    A_FpLong x)
{
    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    A_Boolean varyingB = FALSE;
    ERR(suites.StreamSuite7()->AEGP_IsStreamTimevarying(
        streamH, &varyingB));

    if (!err && varyingB) {
        return A_Err_GENERIC; // use KeyframeSuite instead
    }

    A_Time t{0, 1};
    AEGP_StreamValue2 v{};
    A_Boolean have_valueB = FALSE;

    ERR(suites.StreamSuite7()->AEGP_GetNewStreamValue(
        plugin_id,
        streamH,
        AEGP_LTimeMode_CompTime,
        &t,
        TRUE,
        &v));

    if (!err) {
        have_valueB = TRUE;
        v.val.one_d = x;
        ERR(suites.StreamSuite7()->AEGP_SetStreamValue(
            plugin_id, streamH, &v));
    }

    if (have_valueB) {
        ERR2(suites.StreamSuite7()->AEGP_DisposeStreamValue(&v));
    }
    return err;
}
