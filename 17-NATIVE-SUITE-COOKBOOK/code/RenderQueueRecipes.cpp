#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"
#include "AE_Macros.h"

A_Err Bible_AddCompAndSetFirstOutputPath(
    SPBasicSuite* pica,
    AEGP_CompH compH,
    const A_char* initial_pathZ,
    const A_UTF16Char* final_pathZ)
{
    if (!pica || !compH || !initial_pathZ || !final_pathZ) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    // Adding to the queue invalidates previous RQ refs.
    ERR(suites.RenderQueueSuite1()->AEGP_AddCompToRenderQueue(
        compH, initial_pathZ));

    A_long item_count = 0;
    ERR(suites.RQItemSuite3()->AEGP_GetNumRQItems(&item_count));
    if (!err && item_count < 1) {
        return A_Err_GENERIC;
    }

    AEGP_RQItemRefH rq_itemH = nullptr;
    ERR(suites.RQItemSuite3()->AEGP_GetRQItemByIndex(
        item_count - 1, &rq_itemH));

    A_long outmod_count = 0;
    ERR(suites.RQItemSuite3()->AEGP_GetNumOutputModulesForRQItem(
        rq_itemH, &outmod_count));
    if (!err && outmod_count < 1) {
        return A_Err_GENERIC;
    }

    AEGP_OutputModuleRefH outmodH = nullptr;
    ERR(suites.OutputModuleSuite4()->AEGP_GetOutputModuleByIndex(
        rq_itemH, 0, &outmodH));

    ERR(suites.OutputModuleSuite4()->AEGP_SetOutputFilePath(
        rq_itemH, outmodH, final_pathZ));

    // RQItemSuite3 takes AEGP_RenderItemStatusType, not A_Boolean.
    ERR(suites.RQItemSuite3()->AEGP_SetRenderState(
        rq_itemH, AEGP_RenderItemStatus_QUEUED));

    AEGP_RenderItemStatusType actual_state = AEGP_RenderItemStatus_NONE;
    ERR(suites.RQItemSuite3()->AEGP_GetRenderState(
        rq_itemH, &actual_state));

    if (!err && actual_state != AEGP_RenderItemStatus_QUEUED) {
        err = A_Err_GENERIC;
    }

    return err;
}
