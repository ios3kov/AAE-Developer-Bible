#include "AEConfig.h"
#include "entry.h"
#include "AE_Effect.h"
#include "AE_EffectCB.h"
#include "AE_EffectSuites.h"
#include "AE_Macros.h"
#include "Param_Utils.h"
#include "AEFX_SuiteHelper.h"

#include <algorithm>

namespace {
constexpr A_long kMajor = 1;
constexpr A_long kMinor = 0;
constexpr A_long kBug   = 0;
constexpr A_long kBuild = 1;

enum ParamIndex {
    INPUT = 0,
    GAIN,
    PARAM_COUNT
};

enum ParamDiskId {
    GAIN_DISK_ID = 1
};

struct GainInfo {
    PF_FpLong gain = 1.0;
};

template <typename T, int MAX_CHAN>
static PF_Err GainPixel(void* refcon, A_long, A_long, T* inP, T* outP) {
    const auto* info = static_cast<const GainInfo*>(refcon);
    const auto scale = info ? info->gain : 1.0;
    outP->alpha = inP->alpha;
    outP->red   = static_cast<decltype(outP->red)>(std::clamp<double>(inP->red   * scale, 0.0, MAX_CHAN));
    outP->green = static_cast<decltype(outP->green)>(std::clamp<double>(inP->green * scale, 0.0, MAX_CHAN));
    outP->blue  = static_cast<decltype(outP->blue)>(std::clamp<double>(inP->blue  * scale, 0.0, MAX_CHAN));
    return PF_Err_NONE;
}

static PF_Err About(PF_OutData* out_data) {
    PF_SPRINTF(out_data->return_msg,
               "Bible Minimal Gain v%d.%d\rMinimal AE SDK effect template.",
               kMajor, kMinor);
    return PF_Err_NONE;
}

static PF_Err GlobalSetup(PF_OutData* out_data) {
    out_data->my_version = PF_VERSION(kMajor, kMinor, kBug, PF_Stage_DEVELOP, kBuild);
    out_data->out_flags = PF_OutFlag_DEEP_COLOR_AWARE;
    out_data->out_flags2 = 0; // Add capabilities only after implementing/testing them.
    return PF_Err_NONE;
}

static PF_Err ParamsSetup(PF_InData* in_data, PF_OutData* out_data) {
    PF_ParamDef def;
    AEFX_CLR_STRUCT(def);

    PF_ADD_FLOAT_SLIDERX(
        "Gain",
        0.0, 4.0,
        0.0, 4.0,
        1.0,
        PF_Precision_HUNDREDTHS,
        0,
        0,
        GAIN_DISK_ID);

    out_data->num_params = PARAM_COUNT;
    return PF_Err_NONE;
}

static PF_Err Render(PF_InData* in_data, PF_ParamDef* params[], PF_LayerDef* output) {
    GainInfo info;
    info.gain = params[GAIN]->u.fs_d.value;

    AEGP_SuiteHandler suites(in_data->pica_basicP);

    if (PF_WORLD_IS_DEEP(output)) {
        return suites.Iterate16Suite1()->iterate(
            in_data,
            0,
            output->height,
            &params[INPUT]->u.ld,
            nullptr,
            &info,
            &GainPixel<PF_Pixel16, PF_MAX_CHAN16>,
            output);
    }

    return suites.Iterate8Suite1()->iterate(
        in_data,
        0,
        output->height,
        &params[INPUT]->u.ld,
        nullptr,
        &info,
        &GainPixel<PF_Pixel8, PF_MAX_CHAN8>,
        output);
}
} // namespace

extern "C" DllExport
PF_Err EffectMain(
    PF_Cmd cmd,
    PF_InData* in_data,
    PF_OutData* out_data,
    PF_ParamDef* params[],
    PF_LayerDef* output,
    void* /*extra*/)
{
    try {
        switch (cmd) {
            case PF_Cmd_ABOUT:        return About(out_data);
            case PF_Cmd_GLOBAL_SETUP: return GlobalSetup(out_data);
            case PF_Cmd_PARAM_SETUP:  return ParamsSetup(in_data, out_data);
            case PF_Cmd_RENDER:       return Render(in_data, params, output);
            default:                  return PF_Err_NONE;
        }
    } catch (PF_Err& err) {
        return err;
    } catch (...) {
        return PF_Err_INTERNAL_STRUCT_DAMAGED;
    }
}

extern "C" DllExport
PF_Err PluginDataEntryFunction(
    PF_PluginDataPtr inPtr,
    PF_PluginDataCB inPluginDataCallBackPtr,
    SPBasicSuite* /*inSPBasicSuitePtr*/,
    const char* /*inHostName*/,
    const char* /*inHostVersion*/)
{
    return PF_REGISTER_EFFECT(
        inPtr,
        inPluginDataCallBackPtr,
        "Bible Minimal Gain",
        "com.aedevbible.MinimalGain",
        "AE Developer Bible",
        AE_RESERVED_INFO);
}
