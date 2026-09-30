#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"
#include "AE_Macros.h"
#include "../../19-NATIVE-CODE-FOUNDATION/code/AegpOwners.h"
#include "../../19-NATIVE-CODE-FOUNDATION/code/HostCallbackGuard.h"

A_Err Bible_WithRenderedWorld(
    SPBasicSuite* pica,
    AEGP_RenderOptionsH optionsH,
    A_Err (*consume)(AEGP_SuiteHandler&, AEGP_WorldH))
{
    return GuardAeHostCallback([&]() -> A_Err {
    if (!pica || !optionsH || !consume) {
        return A_Err_PARAMETER;
    }

    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    AEGP_FrameReceiptH receiptH = nullptr;
    ERR(suites.RenderSuite4()->AEGP_RenderAndCheckoutFrame(
        optionsH,
        nullptr,
        nullptr,
        &receiptH));
    AegpFrameReceiptOwner receipt(suites.RenderSuite4(), receiptH);

    AEGP_WorldH worldH = nullptr;
    if (!err) {
        ERR(suites.RenderSuite4()->AEGP_GetReceiptWorld(
            receiptH, &worldH));
    }

    if (!err) {
        ERR(consume(suites, worldH));
    }

    if (receiptH) {
        A_Err checkin_err =
            suites.RenderSuite4()->AEGP_CheckinFrame(receipt.release());
        if (!err) {
            err = checkin_err;
        }
    }
    return err;
    }, A_Err_GENERIC);
}
