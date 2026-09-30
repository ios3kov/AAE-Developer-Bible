#include "PicaSuiteRef.h"
#include "AegpOwners.h"
#include "UndoScope.h"
#include "HostCallbackGuard.h"
#include <cassert>
#include <stdexcept>
#include <utility>

static int releases = 0, disposals = 0, starts = 0, ends = 0;
static bool fail_acquire = false, fail_undo = false;
struct DummySuite { int value = 1; };
static SPErr Acquire(const char*, long, const void** out) {
    static DummySuite suite;
    *out = fail_acquire ? nullptr : &suite;
    return fail_acquire ? 7 : 0;
}
static SPErr Release(const char*, long) { ++releases; return 0; }
static A_Err Dispose(void*) { ++disposals; return 0; }
static A_Err StartUndo(const A_char*) { ++starts; return fail_undo ? 7 : 0; }
static A_Err EndUndo() { ++ends; return 0; }

int main() {
    SPBasicSuite basic{Acquire, Release};
    {
        PicaSuiteRef<DummySuite> a;
        assert(a.acquire(&basic, "Dummy", 1) == 0);
        assert(a->value == 1);
        PicaSuiteRef<DummySuite> b(std::move(a));
        assert(!a && b);
        a = std::move(b);
        assert(a && !b);
        a.reset(); a.reset();
        assert(releases == 1);
        fail_acquire = true;
        assert(a.acquire(&basic, "Dummy", 1) == 7 && !a);
    }
    assert(releases == 1);
    AEGP_StreamSuite6 streams{Dispose};
    {
        AegpStreamRefOwner a(&streams, reinterpret_cast<void*>(1));
        AegpStreamRefOwner b(&streams, reinterpret_cast<void*>(2));
        b = std::move(a);
        assert(!a.get() && b.get());
        assert(disposals == 1);
        auto raw = b.release();
        assert(raw && !b.get());
        Dispose(raw);
    }
    assert(disposals == 2);
    {
        AEGP_EffectSuite4 effects{Dispose};
        AEGP_RenderSuite4 render{Dispose};
        AEGP_MemorySuite1 memory{Dispose};
        AegpEffectRefOwner e(&effects, reinterpret_cast<void*>(3));
        AegpFrameReceiptOwner f(&render, reinterpret_cast<void*>(4));
        AegpMemHandleOwner m(&memory, reinterpret_cast<void*>(5));
    }
    assert(disposals == 5);
    AEGP_UtilitySuite6 utility{StartUndo, EndUndo};
    { AegpUndoScope undo(&utility, "ok"); assert(undo.active()); }
    assert(starts == 1 && ends == 1);
    fail_undo = true;
    { AegpUndoScope undo(&utility, "fail"); assert(!undo.active() && undo.start_error() == 7); }
    assert(starts == 2 && ends == 1);
    { AegpUndoScope undo(nullptr, "null"); assert(!undo.active() && undo.start_error()); }
    assert(GuardAeHostCallback([]() -> A_Err { throw std::runtime_error("fail"); }, 9) == 9);
    assert(GuardAeHostCallback([]() -> A_Err { throw A_Err(5); }, 9) == 5);
    assert(GuardAeHostCallback([]() -> A_Err { throw A_Err(0); }, 9) == 9);
    assert(GuardAeHostCallback([]() -> A_Err { return 3; }, 9) == 3);
}
