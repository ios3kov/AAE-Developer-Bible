#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"
#include "AE_Macros.h"

A_Err Bible_GetProjectAndRoot(
    SPBasicSuite* pica,
    AEGP_ProjectH* projectPH,
    AEGP_ItemH* rootPH)
{
    if (!pica || !projectPH || !rootPH) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    A_long count = 0;
    ERR(suites.ProjSuite6()->AEGP_GetNumProjects(&count));
    if (!err && count < 1) {
        err = A_Err_GENERIC;
    }

    if (!err) {
        ERR(suites.ProjSuite6()->AEGP_GetProjectByIndex(0, projectPH));
    }
    if (!err) {
        ERR(suites.ProjSuite6()->AEGP_GetProjectRootFolder(*projectPH, rootPH));
    }
    return err;
}

A_Err Bible_CountProjectItems(
    SPBasicSuite* pica,
    AEGP_ProjectH projectH,
    A_long* countPL)
{
    if (!pica || !projectH || !countPL) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    *countPL = 0;
    AEGP_ItemH itemH = nullptr;
    ERR(suites.ItemSuite9()->AEGP_GetFirstProjItem(projectH, &itemH));

    while (!err && itemH) {
        ++(*countPL);

        AEGP_ItemH nextH = nullptr;
        ERR(suites.ItemSuite9()->AEGP_GetNextProjItem(
            projectH, itemH, &nextH));
        itemH = nextH;
    }
    return err;
}
