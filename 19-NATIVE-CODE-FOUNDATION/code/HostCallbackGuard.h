#pragma once

#include <utility>
#include "A.h"

// Supply the project's chosen fallback A_Err. This helper deliberately does not
// invent a generic AE error constant that may differ between SDK contexts.
template <typename Fn>
A_Err GuardAeHostCallback(Fn&& fn, A_Err fallback_err) noexcept {
    try {
        return std::forward<Fn>(fn)();
    } catch (...) {
        return fallback_err;
    }
}
