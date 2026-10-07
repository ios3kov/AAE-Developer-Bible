#include "../code/monitor_frame_copy.hpp"
#include <cassert>

int main()
{
    using namespace bible;
    unsigned char source[] = {1,2,3,4,99,99,5,6,7,8};
    std::vector<unsigned char> output{42};
    assert(copy_monitor_frame(source, sizeof(source), {1,2,4,6}, 8, output) ==
           MonitorCopyResult::copied);
    assert((output == std::vector<unsigned char>{1,2,3,4,5,6,7,8}));
    source[0] = 0;
    assert(output[0] == 1); // no borrowed storage retained
    const auto previous = output;
    assert(copy_monitor_frame(source, 9, {1,2,4,6}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    assert(copy_monitor_frame(source, 10, {1,2,4,6}, 7, output) ==
           MonitorCopyResult::over_budget);
    assert(copy_monitor_frame(nullptr, 10, {1,2,4,6}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    assert(copy_monitor_frame(source, 10, {1,2,4,3}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    assert(copy_monitor_frame(source, 10, {0,2,4,6}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    assert(copy_monitor_frame(source, 10, {1,2,3,6}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    const auto max = std::numeric_limits<std::size_t>::max();
    assert(copy_monitor_frame(source, 10, {max,2,16,6}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    assert(copy_monitor_frame(source, 10, {1,max,4,max}, 8, output) ==
           MonitorCopyResult::invalid_layout);
    assert(output == previous); // rejection does not publish partial frame
    unsigned char wide[32] = {};
    for (auto pixel_bytes : {std::size_t{8}, std::size_t{16}}) {
        assert(copy_monitor_frame(wide, sizeof(wide), {1,2,pixel_bytes,pixel_bytes},
                                  32, output) == MonitorCopyResult::copied);
        assert(output.size() == 2 * pixel_bytes);
    }
}
