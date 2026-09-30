#pragma once
#include <cstdint>

namespace bible_bridge {
constexpr std::uint32_t kVersion = 1;

enum class Op : std::uint32_t {
    Ping = 1,
    ReloadResources = 2,
    GetStatus = 3
};

struct MessageV1 {
    std::uint32_t size = sizeof(MessageV1);
    std::uint32_t version = kVersion;
    Op op = Op::Ping;
    std::uint32_t flags = 0;
    std::uint64_t request_id = 0;
    std::int32_t result_code = 0;
    std::uint32_t reserved = 0;
};

static_assert(sizeof(MessageV1) == 32, "ABI drift: MessageV1 changed");
}
