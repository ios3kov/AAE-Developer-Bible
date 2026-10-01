#pragma once
#include "A.h"
using AEGP_StreamRefH = void*;
using AEGP_EffectRefH = void*;
using AEGP_FrameReceiptH = void*;
using AEGP_MemHandle = void*;
struct AEGP_StreamSuite6 { A_Err (*AEGP_DisposeStream)(AEGP_StreamRefH); };
struct AEGP_EffectSuite5 { A_Err (*AEGP_DisposeEffect)(AEGP_EffectRefH); };
struct AEGP_RenderSuite4 { A_Err (*AEGP_CheckinFrame)(AEGP_FrameReceiptH); };
struct AEGP_MemorySuite1 { A_Err (*AEGP_FreeMemHandle)(AEGP_MemHandle); };
struct AEGP_UtilitySuite6 {
    A_Err (*AEGP_StartUndoGroup)(const A_char*);
    A_Err (*AEGP_EndUndoGroup)();
};
