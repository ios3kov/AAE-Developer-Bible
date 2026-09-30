#pragma once

#include "AE_GeneralPlug.h"

class AegpUndoScope final {
public:
    AegpUndoScope(const AEGP_UtilitySuite6* suite, const A_char* nameZ) noexcept
        : suite_(suite) {
        if (suite_) {
            start_err_ = suite_->AEGP_StartUndoGroup(nameZ);
            active_ = (start_err_ == A_Err_NONE);
        }
    }
    ~AegpUndoScope() {
        if (active_ && suite_) {
            (void)suite_->AEGP_EndUndoGroup();
        }
    }
    AegpUndoScope(const AegpUndoScope&) = delete;
    AegpUndoScope& operator=(const AegpUndoScope&) = delete;
    A_Err start_error() const noexcept { return start_err_; }
    bool active() const noexcept { return active_; }
private:
    const AEGP_UtilitySuite6* suite_ = nullptr;
    A_Err start_err_ = A_Err_NONE;
    bool active_ = false;
};
