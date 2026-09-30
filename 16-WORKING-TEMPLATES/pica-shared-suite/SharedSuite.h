#pragma once
#include <cstdint>

#define BIBLE_CORE_SUITE_NAME "com.aedevbible.CoreSuite"
#define BIBLE_CORE_SUITE_VERSION 1

typedef struct BibleCoreSuite1 {
    std::int32_t (*GetApiVersion)(std::uint32_t* out_version);
    std::int32_t (*ProcessBytes)(
        const void* input,
        std::uint64_t input_size,
        void* output,
        std::uint64_t output_capacity,
        std::uint64_t* output_size);
} BibleCoreSuite1;
