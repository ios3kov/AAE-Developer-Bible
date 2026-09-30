#include "PicaSuiteRef.h"
#include "AegpOwners.h"
#include "UndoScope.h"
#include "HostCallbackGuard.h"

static SPErr Acquire(const char*, long, const void** out) { static int suite = 1; *out = &suite; return 0; }
static SPErr Release(const char*, long) { return 0; }
static A_Err DisposeStream(AEGP_StreamRefH) { return 0; }
static A_Err DisposeEffect(AEGP_EffectRefH) { return 0; }
static A_Err Checkin(AEGP_FrameReceiptH) { return 0; }
static A_Err FreeMem(AEGP_MemHandle) { return 0; }
static A_Err StartUndo(const A_char*) { return 0; }
static A_Err EndUndo() { return 0; }
struct DummySuite { int value; };

int main() {
    SPBasicSuite basic{Acquire, Release};
    PicaSuiteRef<DummySuite> s;
    if (s.acquire(&basic, "Dummy", 1) != 0 || !s) return 1;
    s.reset();

    AEGP_StreamSuite7 ss{DisposeStream};
    AEGP_EffectSuite4 es{DisposeEffect};
    AEGP_RenderSuite4 rs{Checkin};
    AEGP_MemorySuite1 ms{FreeMem};
    AEGP_UtilitySuite6 us{StartUndo, EndUndo};
    AegpStreamRefOwner so(&ss, reinterpret_cast<void*>(1));
    AegpEffectRefOwner eo(&es, reinterpret_cast<void*>(2));
    AegpFrameReceiptOwner fo(&rs, reinterpret_cast<void*>(3));
    AegpMemHandleOwner mo(&ms, reinterpret_cast<void*>(4));
    AegpUndoScope undo(&us, "Test");
    return GuardAeHostCallback([]() -> A_Err { return 0; }, 9);
}
