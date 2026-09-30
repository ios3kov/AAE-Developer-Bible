#include "AEConfig.h"
#include "entry.h"
#include "AE_Effect.h"
#include "AE_EffectCB.h"
#include "AE_EffectSuites.h"
#include "AE_Macros.h"
#include "Param_Utils.h"
#include "AEGP_SuiteHandler.h"

namespace {
PF_Err GlobalSetup(PF_OutData* out) {
    out->my_version = PF_VERSION(1, 0, 0, PF_Stage_DEVELOP, 1);
    out->out_flags  = PF_OutFlag_DEEP_COLOR_AWARE;
    // Enable MFR only after concurrent-frame host validation of the final effect.
    out->out_flags2 = PF_OutFlag2_SUPPORTS_SMART_RENDER |
                      PF_OutFlag2_FLOAT_COLOR_AWARE;
    return PF_Err_NONE;
}

PF_Err ParamsSetup(PF_OutData* out) {
    out->num_params = 1; // input only
    return PF_Err_NONE;
}

PF_Err SmartPreRender(PF_InData* in, PF_OutData*, PF_PreRenderExtra* extra) {
    if (!in || !extra || !extra->input || !extra->output || !extra->cb)
        return PF_Err_BAD_CALLBACK_PARAM;
    PF_RenderRequest req = extra->input->output_request;
    PF_CheckoutResult in_result{};
    PF_Err err = extra->cb->checkout_layer(
        in->effect_ref, 0, 1, &req,
        in->current_time,
        in->time_step,
        in->time_scale,
        &in_result);
    if (!err) {
        extra->output->result_rect = in_result.result_rect;
        extra->output->max_result_rect = in_result.max_result_rect;
    }
    return err;
}

PF_Err SmartRender(PF_InData* in, PF_OutData*, PF_SmartRenderExtra* extra) {
    if (!in || !extra || !extra->cb) return PF_Err_BAD_CALLBACK_PARAM;
    AEGP_SuiteHandler suites(in->pica_basicP);
    const auto* transform = suites.WorldTransformSuite1();
    PF_EffectWorld* input = nullptr;
    PF_EffectWorld* output = nullptr;
    PF_Err err = extra->cb->checkout_layer_pixels(in->effect_ref, 1, &input);
    const bool checked_out = !err;
    if (!err) err = extra->cb->checkout_output(in->effect_ref, &output);
    if (!err && (!input || !output)) err = PF_Err_BAD_CALLBACK_PARAM;
    if (!err) err = transform->copy(in->effect_ref, input, output, nullptr, nullptr);
    if (checked_out) {
        const PF_Err checkin_err = extra->cb->checkin_layer_pixels(in->effect_ref, 1);
        if (!err) err = checkin_err;
    }
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
            case PF_Cmd_PARAMS_SETUP:     return ParamsSetup(out);
            case PF_Cmd_SMART_PRE_RENDER: return SmartPreRender(in, out, static_cast<PF_PreRenderExtra*>(extra));
            case PF_Cmd_SMART_RENDER:     return SmartRender(in, out, static_cast<PF_SmartRenderExtra*>(extra));
            default: return PF_Err_NONE;
        }
    } catch (PF_Err& e) { return e; }
    catch (...) { return PF_Err_INTERNAL_STRUCT_DAMAGED; }
}

extern "C" DllExport PF_Err PluginDataEntryFunction(
    PF_PluginDataPtr inPtr, PF_PluginDataCB callback,
    SPBasicSuite*, const char*, const char*)
{
    PF_Err result = PF_Err_NONE;
    PF_REGISTER_EFFECT(inPtr, callback, "Bible SmartFX Copy",
                       "com.aedevbible.SmartCopy", "AE Developer Bible", AE_RESERVED_INFO);
    return result;
}
