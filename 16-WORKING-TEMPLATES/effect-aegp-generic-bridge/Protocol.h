#pragma once

#include <cstddef>
#include <cstdint>
#include <type_traits>

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

static_assert(std::is_standard_layout<MessageV1>::value,
              "ABI drift: MessageV1 must remain standard-layout");
static_assert(std::is_trivially_copyable<MessageV1>::value,
              "ABI drift: MessageV1 must remain trivially copyable");

static_assert(sizeof(Op) == 4, "ABI drift: Op must remain 32-bit");
static_assert(sizeof(MessageV1) == 32, "ABI drift: MessageV1 changed");

static_assert(offsetof(MessageV1, size) == 0, "ABI drift: size offset changed");
static_assert(offsetof(MessageV1, version) == 4, "ABI drift: version offset changed");
static_assert(offsetof(MessageV1, op) == 8, "ABI drift: op offset changed");
static_assert(offsetof(MessageV1, flags) == 12, "ABI drift: flags offset changed");
static_assert(offsetof(MessageV1, request_id) == 16, "ABI drift: request_id offset changed");
static_assert(offsetof(MessageV1, result_code) == 24, "ABI drift: result_code offset changed");
static_assert(offsetof(MessageV1, reserved) == 28, "ABI drift: reserved offset changed");

} // namespace bible_bridge
