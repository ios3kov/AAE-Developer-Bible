#pragma once

#include <cstddef>
#include <cstring>
#include <limits>
#include <vector>

namespace bible {

// Product-side layout only. Not an Adobe ABI declaration or async receipt owner.
struct MonitorLayout {
    std::size_t width, height, pixel_bytes, row_bytes;
};

enum class MonitorCopyResult { copied, invalid_layout, over_budget };

// source_extent must be established by the caller; a host pointer alone cannot
// establish it. No host callbacks, queues or borrowed pointers retained here.
inline MonitorCopyResult copy_monitor_frame(
    const void* source, std::size_t source_extent, MonitorLayout layout,
    std::size_t byte_budget, std::vector<unsigned char>& destination)
{
    const auto max = std::numeric_limits<std::size_t>::max();
    if (!source || !layout.width || !layout.height ||
        (layout.pixel_bytes != 4 && layout.pixel_bytes != 8 && layout.pixel_bytes != 16) ||
        layout.width > max / layout.pixel_bytes) {
        return MonitorCopyResult::invalid_layout;
    }
    const auto packed_row = layout.width * layout.pixel_bytes;
    if (layout.row_bytes < packed_row || layout.height > max / packed_row ||
        (layout.height - 1) > (max - packed_row) / layout.row_bytes) {
        return MonitorCopyResult::invalid_layout;
    }
    const auto source_required = (layout.height - 1) * layout.row_bytes + packed_row;
    if (source_required > source_extent) return MonitorCopyResult::invalid_layout;
    const auto packed_size = layout.height * packed_row;
    if (packed_size > byte_budget) return MonitorCopyResult::over_budget;

    // Allocate before replacing caller state; allocation exceptions propagate to
    // the caller's C++ boundary. This reference is not allocation-free staging.
    std::vector<unsigned char> copy(packed_size);
    const auto* bytes = static_cast<const unsigned char*>(source);
    for (std::size_t row = 0; row < layout.height; ++row) {
        std::memcpy(copy.data() + row * packed_row,
                    bytes + row * layout.row_bytes, packed_row);
    }
    destination.swap(copy);
    return MonitorCopyResult::copied;
}

} // namespace bible
