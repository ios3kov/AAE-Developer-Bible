#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"

A_Err Bible_CreateComp(
    SPBasicSuite* pica,
    AEGP_ItemH parent_folderH,
    const A_UTF16Char* nameZ,
    AEGP_CompH* compPH)
{
    if (!pica || !nameZ || !compPH) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    A_Ratio par{1, 1};
    A_Time duration{10, 1};
    A_Ratio fps{25, 1};

    ERR(suites.CompSuite13()->AEGP_CreateComp(
        parent_folderH,
        nameZ,
        1920,
        1080,
        &par,
        &duration,
        &fps,
        compPH));
    return err;
}

A_Err Bible_GetLayerIds(
    SPBasicSuite* pica,
    AEGP_CompH compH,
    AEGP_LayerIDVal* ids,
    A_long capacity,
    A_long* writtenPL)
{
    if (!pica || !compH || !ids || !writtenPL || capacity < 0) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    A_long count = 0;
    ERR(suites.LayerSuite9()->AEGP_GetCompNumLayers(compH, &count));

    *writtenPL = 0;
    for (A_long i = 0; !err && i < count && i < capacity; ++i) {
        AEGP_LayerH layerH = nullptr;
        ERR(suites.LayerSuite9()->AEGP_GetCompLayerByIndex(
            compH, i, &layerH));

        if (!err) {
            ERR(suites.LayerSuite9()->AEGP_GetLayerID(
                layerH, &ids[*writtenPL]));
        }
        if (!err) {
            ++(*writtenPL);
        }
    }
    return err;
}
