#include "../16-WORKING-TEMPLATES/effect-state/VersionedState.h"
#include <cassert>
int main() {
    using namespace bible_state;
    State s{2500,1}, result;
    auto b = encode(s);
    assert(decode(b.data(), b.size(), result) == Decode::ok);
    assert(result.amount == 2500 && result.mode == 1);
    for (std::size_t n=0; n<b.size(); ++n)
        assert(decode(b.data(), n, result) == Decode::malformed);
    b[4]=1; b[6]=10; b.resize(10);
    assert(decode(b.data(), b.size(), result) == Decode::ok && result.mode == 0);
    b[4]=3;
    result={777,1};
    assert(decode(b.data(), b.size(), result) == Decode::unsupported);
    assert(result.amount==777 && result.mode==1);
    b[4]=1; b[8]=255; b[9]=255;
    assert(decode(b.data(), b.size(), result) == Decode::malformed);
    assert(result.amount==777);
    assert(decode(nullptr, 12, result) == Decode::malformed);
}
