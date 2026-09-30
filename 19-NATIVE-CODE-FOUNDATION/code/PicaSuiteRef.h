#pragma once

#include "SPBasic.h"

// Lifetime rule: destroy/reset this object while SPBasicSuite is still valid.
// Do not rely on a process-global static destructor after the AE host tears down.
template <typename SuiteT>
class PicaSuiteRef final {
public:
    PicaSuiteRef() = default;
    ~PicaSuiteRef() { reset(); }

    PicaSuiteRef(const PicaSuiteRef&) = delete;
    PicaSuiteRef& operator=(const PicaSuiteRef&) = delete;

    PicaSuiteRef(PicaSuiteRef&& other) noexcept { move_from(other); }
    PicaSuiteRef& operator=(PicaSuiteRef&& other) noexcept {
        if (this != &other) {
            reset();
            move_from(other);
        }
        return *this;
    }

    SPErr acquire(const SPBasicSuite* basic, const char* suite_name, long suite_version) noexcept {
        reset();
        if (!basic || !suite_name) {
            return static_cast<SPErr>(-1);
        }
        const void* raw = nullptr;
        const SPErr err = basic->AcquireSuite(suite_name, suite_version, &raw);
        if (err || !raw) {
            return err ? err : static_cast<SPErr>(-1);
        }
        basic_ = basic;
        name_ = suite_name;
        version_ = suite_version;
        suite_ = static_cast<const SuiteT*>(raw);
        return 0;
    }

    void reset() noexcept {
        if (suite_ && basic_ && name_) {
            (void)basic_->ReleaseSuite(name_, version_);
        }
        suite_ = nullptr;
        basic_ = nullptr;
        name_ = nullptr;
        version_ = 0;
    }

    const SuiteT* get() const noexcept { return suite_; }
    const SuiteT* operator->() const noexcept { return suite_; }
    explicit operator bool() const noexcept { return suite_ != nullptr; }

private:
    void move_from(PicaSuiteRef& other) noexcept {
        basic_ = other.basic_;
        name_ = other.name_;
        version_ = other.version_;
        suite_ = other.suite_;
        other.basic_ = nullptr;
        other.name_ = nullptr;
        other.version_ = 0;
        other.suite_ = nullptr;
    }

    const SPBasicSuite* basic_ = nullptr;
    const char* name_ = nullptr;
    long version_ = 0;
    const SuiteT* suite_ = nullptr;
};
