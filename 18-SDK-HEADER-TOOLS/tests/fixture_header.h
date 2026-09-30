#pragma once
#define kAEGPExampleSuite "AEGP Example Suite"
#define kAEGPExampleSuiteVersion2 2

typedef struct AEGP_ExampleSuite2 {
    SPAPI A_Err (*AEGP_DoThing)(
        AEGP_ItemH itemH,
        A_long valueL);
    SPAPI A_Err (*AEGP_GetThing)(AEGP_ItemH itemH, A_long *valuePL);
} AEGP_ExampleSuite2;

typedef struct {
    A_Err (*PF_TestCallback)(PF_InData *in_data, PF_OutData *out_data);
} PF_TestSuite1;

typedef struct AEIO_FunctionBlock4 {
    A_Err (*AEIO_InitInSpecFromFile)(void *basic_dataP, void *fileP);
} AEIO_FunctionBlock4;
