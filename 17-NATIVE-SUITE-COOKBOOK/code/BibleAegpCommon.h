#pragma once

#include "AEConfig.h"
#include "AE_GeneralPlug.h"
#include "AEGP_SuiteHandler.h"

namespace bible {

class UndoGroup final {
public:
    UndoGroup(AEGP_SuiteHandler& suites, const char* name)
        : utility_(suites.UtilitySuite6())
    {
        active_ =
            (utility_->AEGP_StartUndoGroup(name) == A_Err_NONE);
    }

    ~UndoGroup()
    {
        if (active_) {
            // Destructors must not throw. Production caller may prefer
            // an explicit Close() if EndUndoGroup errors must be surfaced.
            utility_->AEGP_EndUndoGroup();
        }
    }

    UndoGroup(const UndoGroup&) = delete;
    UndoGroup& operator=(const UndoGroup&) = delete;

private:
    const AEGP_UtilitySuite6* utility_;
    bool active_ = false;
};

} // namespace bible
