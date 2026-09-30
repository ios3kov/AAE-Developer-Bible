#include "AEConfig.h"
#include "entry.h"
#include "AE_Effect.h"
#include "AE_EffectCB.h"
#include "AE_EffectSuites.h"
#include "AE_Macros.h"
#include "Param_Utils.h"
#include "AEFX_SuiteHelper.h"

namespace {
PF_Err GlobalSetup(PF_OutData* out) {
    out->my_version = PF_VERSION(1, 0, 0, PF_Stage_DEVELOP, 1);
    out->out_flags  = PF_OutFlag_DEEP_COLOR_AWARE;
    out->out_flags2 = PF_OutFlag2_SUPPORTS_SMART_RENDER |
                      PF_OutFlag2_SUPPORTS_THREADED_RENDERING;
    return PF_Err_NONE;
}

PF_Err ParamsSetup(PF_OutData* out) {
    out->num_params = 1; // input only
    return PF_Err_NONE;
}

PF_Err SmartPreRender(PF_InData*, PF_OutData*, PF_PreRenderExtra* extra) {
    if (!extra || !extra->cb) return PF_Err_BAD_CALLBACK_PARAM;
    PF_RenderRequest req = extra->input->output_request;
    PF_CheckoutResult in_result{};
    PF_Err err = extra->cb->checkout_layer(
        extra->effect_ref, 0, 0, &req,
        extra->input->current_time,
        extra->input->time_step,
        extra->input->time_scale,
        &in_result);
    if (!err) {
        extra->output->result_rect = in_result.result_rect;
        extra->output->max_result_rect = in_result.max_result_rect;
    }
    return err;
}

PF_Err SmartRender(PF_InData*, PF_OutData*, PF_SmartRenderExtra* extra) {
    if (!extra || !extra->cb) return PF_Err_BAD_CALLBACK_PARAM;
    PF_EffectWorld* input = nullptr;
    PF_EffectWorld* output = nullptr;
    PF_Err err = extra->cb->checkout_layer_pixels(extra->effect_ref, 0, &input);
    if (!err) err = extra->cb->checkout_output(extra->effect_ref, &output);
    if (!err && input && output) {
        // Replace this with a thread-safe algorithm. Copying is intentionally left
        // to the host/sample utility appropriate to the SDK version and pixel format.
    }
    if (input) extra->cb->checkin_layer_pixels(extra->effect_ref, 0);
    return err;
}
}

extern "C" DllExport PF_Err EffectMain(
    PF_Cmd cmd, PF_InData* in, PF_OutData* out,
    PF_ParamDef*[], PF_LayerDef*, void* extra)
{
    try {
        switch (cmd) {
            case PF_Cmd_GLOBAL_SETUP:     return GlobalSetup(out);
            case PF_Cmd_PARAM_SETUP:      return ParamsSetup(out);
            case PF_Cmd_SMART_PRE_RENDER: return SmartPreRender(in, out, static_cast<PF_PreRenderExtra*>(extra));
            case PF_Cmd_SMART_RENDER:     return SmartRender(in, out, static_cast<PF_SmartRenderExtra*>(extra));
            default: return PF_Err_NONE;
        }
    } catch (PF_Err& e) { return e; }
    catch (...) { return PF_Err_INTERNAL_STRUCT_DAMAGED; }
}
