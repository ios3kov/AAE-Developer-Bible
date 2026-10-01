#include "../16-WORKING-TEMPLATES/effect-aegp-generic-bridge/Protocol.h"
#include "../16-WORKING-TEMPLATES/pica-shared-suite/SharedSuite.h"

#include <cstdint>
#include <type_traits>

static_assert(std::is_standard_layout<bible_bridge::MessageV1>::value, "bridge ABI");
static_assert(std::is_trivially_copyable<bible_bridge::MessageV1>::value, "bridge ABI");
static_assert(sizeof(bible_bridge::MessageV1) == 32, "bridge ABI size");
static_assert(sizeof(BibleCoreSuite1) == sizeof(void*) * 2, "suite function table size");

int main() {
    bible_bridge::MessageV1 message{};
    BibleCoreSuite1 suite{};
    return (
        message.version == bible_bridge::kVersion &&
        suite.GetApiVersion == nullptr &&
        suite.ProcessBytes == nullptr
    ) ? 0 : 1;
}
