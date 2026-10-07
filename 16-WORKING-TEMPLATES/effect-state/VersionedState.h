#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>

// Portable wire-format lesson, not an Adobe arbitrary callback implementation.
// v1: BSTA, version:u16LE, length:u16LE, amount:u16LE.
// v2 adds mode:u16LE. Amount is thousandths; no native struct is persisted.
namespace bible_state {
struct State { std::uint16_t amount = 1000; std::uint16_t mode = 0; };
enum class Decode { ok, malformed, unsupported };
inline std::uint16_t read16(const std::uint8_t* p) {
    return std::uint16_t(p[0] | (std::uint16_t(p[1]) << 8));
}
inline void put16(std::vector<std::uint8_t>& b, std::uint16_t v) {
    b.push_back(std::uint8_t(v)); b.push_back(std::uint8_t(v >> 8));
}
inline std::vector<std::uint8_t> encode(const State& s) {
    std::vector<std::uint8_t> b{'B','S','T','A'};
    put16(b, 2); put16(b, 12); put16(b, s.amount); put16(b, s.mode);
    return b;
}
inline Decode decode(const std::uint8_t* b, std::size_t n, State& output) {
    if (!b || n < 8 || b[0]!='B' || b[1]!='S' || b[2]!='T' || b[3]!='A')
        return Decode::malformed;
    auto version = read16(b + 4);
    if (version != 1 && version != 2) return Decode::unsupported;
    const std::size_t expected = version == 1 ? 10 : 12;
    if (n != expected || read16(b + 6) != expected) return Decode::malformed;
    State candidate{read16(b + 8), std::uint16_t(version == 1 ? 0 : read16(b + 10))};
    if (candidate.amount > 4000 || candidate.mode > 1) return Decode::malformed;
    output = candidate; // Publish only after complete validation.
    return Decode::ok;
}
} // namespace bible_state
