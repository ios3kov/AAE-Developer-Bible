#include "AEConfig.h"
#include "AE_Effect.h"
#include "AE_EffectSuites.h"
#include "AEGP_SuiteHandler.h"
#include "AE_EffectUI.h"
#include "adobesdk/DrawbotSuite.h"
#include "../../../19-NATIVE-CODE-FOUNDATION/code/HostCallbackGuard.h"

PF_Err HandleCustomUIEvent(PF_InData* in_data, PF_EventExtra* event_extra) {
    return static_cast<PF_Err>(GuardAeHostCallback([&]() -> A_Err {
    if (!in_data || !event_extra) return PF_Err_BAD_CALLBACK_PARAM;
    if (event_extra->e_type != PF_Event_DRAW) return PF_Err_NONE;

    AEGP_SuiteHandler suites(in_data->pica_basicP);
    auto* custom_ui = suites.EffectCustomUISuite1();
    if (!custom_ui) return PF_Err_BAD_CALLBACK_PARAM;

    DRAWBOT_DrawRef draw_ref = nullptr;
    PF_Err err = custom_ui->PF_GetDrawingReference(event_extra->contextH, &draw_ref);
    if (err || !draw_ref) return err;

    // From here acquire the Drawbot supplier/surface/path suites matching your SDK
    // and perform drawing. Keep Drawbot object lifetimes inside this callback.
    return PF_Err_NONE;
    }, PF_Err_INTERNAL_STRUCT_DAMAGED));
}
