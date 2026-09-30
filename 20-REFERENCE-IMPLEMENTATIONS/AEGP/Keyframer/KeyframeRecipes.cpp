#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"

A_Err Bible_AddOneDKeyframes(
    SPBasicSuite* pica,
    AEGP_PluginID plugin_id,
    AEGP_StreamRefH streamH,
    const A_Time* times,
    const A_FpLong* values,
    A_long count)
{
    if (!pica || !streamH || !times || !values || count < 0) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    AEGP_StreamType stream_type = AEGP_StreamType_NO_DATA;
    ERR(suites.StreamSuite7()->AEGP_GetStreamType(
        streamH, &stream_type));

    if (!err && stream_type != AEGP_StreamType_OneD) {
        return A_Err_PARAMETER;
    }

    AEGP_AddKeyframesInfoH addH = nullptr;
    ERR(suites.KeyframeSuite3()->AEGP_StartAddKeyframes(
        streamH, &addH));

    for (A_long i = 0; !err && i < count; ++i) {
        AEGP_StreamValue2 value{};
        A_Boolean have_valueB = FALSE;
        ERR(suites.StreamSuite7()->AEGP_GetNewStreamValue(
            plugin_id,
            streamH,
            AEGP_LTimeMode_CompTime,
            &times[i],
            TRUE,
            &value));

        if (!err) {
            have_valueB = TRUE;
            value.val.one_d = values[i];

            A_long key_index = 0;
            ERR(suites.KeyframeSuite3()->AEGP_AddKeyframes(
                addH,
                AEGP_LTimeMode_CompTime,
                &times[i],
                &key_index));

            if (!err) {
                ERR(suites.KeyframeSuite3()->AEGP_SetAddKeyframe(
                    addH,
                    key_index,
                    &value));
            }
        }

        if (have_valueB) {
            ERR2(suites.StreamSuite7()->AEGP_DisposeStreamValue(&value));
        }
    }

    if (addH) {
        const A_Boolean commitB = err ? FALSE : TRUE;
        const A_Err end_err =
            suites.KeyframeSuite3()->AEGP_EndAddKeyframes(
                commitB, addH);
        if (!err) {
            err = end_err;
        }
    }
    return err;
}
