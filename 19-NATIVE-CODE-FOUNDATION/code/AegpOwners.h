#pragma once

#include "AE_GeneralPlug.h"

// These owners are intentionally explicit rather than a single generic deleter:
// each AE resource has a different host release contract.

class AegpStreamRefOwner final {
public:
    AegpStreamRefOwner() = default;
    AegpStreamRefOwner(const AEGP_StreamSuite6* suite, AEGP_StreamRefH h) : suite_(suite), h_(h) {}
    ~AegpStreamRefOwner() { reset(); }
    AegpStreamRefOwner(const AegpStreamRefOwner&) = delete;
    AegpStreamRefOwner& operator=(const AegpStreamRefOwner&) = delete;
    AegpStreamRefOwner(AegpStreamRefOwner&& o) noexcept : suite_(o.suite_), h_(o.release()) {}
    AegpStreamRefOwner& operator=(AegpStreamRefOwner&& o) noexcept {
        if (this != &o) { reset(); suite_ = o.suite_; h_ = o.release(); }
        return *this;
    }
    AEGP_StreamRefH get() const noexcept { return h_; }
    AEGP_StreamRefH release() noexcept { auto h = h_; h_ = nullptr; return h; }
    void reset(AEGP_StreamRefH h = nullptr) noexcept {
        if (h_ && suite_) { (void)suite_->AEGP_DisposeStream(h_); }
        h_ = h;
    }
private:
    const AEGP_StreamSuite6* suite_ = nullptr;
    AEGP_StreamRefH h_ = nullptr;
};

class AegpEffectRefOwner final {
public:
    AegpEffectRefOwner() = default;
    AegpEffectRefOwner(const AEGP_EffectSuite4* suite, AEGP_EffectRefH h) : suite_(suite), h_(h) {}
    ~AegpEffectRefOwner() { reset(); }
    AegpEffectRefOwner(const AegpEffectRefOwner&) = delete;
    AegpEffectRefOwner& operator=(const AegpEffectRefOwner&) = delete;
    AegpEffectRefOwner(AegpEffectRefOwner&& o) noexcept : suite_(o.suite_), h_(o.release()) {}
    AegpEffectRefOwner& operator=(AegpEffectRefOwner&& o) noexcept {
        if (this != &o) { reset(); suite_ = o.suite_; h_ = o.release(); }
        return *this;
    }
    AEGP_EffectRefH get() const noexcept { return h_; }
    AEGP_EffectRefH release() noexcept { auto h = h_; h_ = nullptr; return h; }
    void reset(AEGP_EffectRefH h = nullptr) noexcept {
        if (h_ && suite_) { (void)suite_->AEGP_DisposeEffect(h_); }
        h_ = h;
    }
private:
    const AEGP_EffectSuite4* suite_ = nullptr;
    AEGP_EffectRefH h_ = nullptr;
};

class AegpFrameReceiptOwner final {
public:
    AegpFrameReceiptOwner() = default;
    AegpFrameReceiptOwner(const AEGP_RenderSuite4* suite, AEGP_FrameReceiptH h) : suite_(suite), h_(h) {}
    ~AegpFrameReceiptOwner() { reset(); }
    AegpFrameReceiptOwner(const AegpFrameReceiptOwner&) = delete;
    AegpFrameReceiptOwner& operator=(const AegpFrameReceiptOwner&) = delete;
    AegpFrameReceiptOwner(AegpFrameReceiptOwner&& o) noexcept : suite_(o.suite_), h_(o.release()) {}
    AegpFrameReceiptOwner& operator=(AegpFrameReceiptOwner&& o) noexcept {
        if (this != &o) { reset(); suite_ = o.suite_; h_ = o.release(); }
        return *this;
    }
    AEGP_FrameReceiptH get() const noexcept { return h_; }
    AEGP_FrameReceiptH release() noexcept { auto h = h_; h_ = nullptr; return h; }
    void reset(AEGP_FrameReceiptH h = nullptr) noexcept {
        if (h_ && suite_) { (void)suite_->AEGP_CheckinFrame(h_); }
        h_ = h;
    }
private:
    const AEGP_RenderSuite4* suite_ = nullptr;
    AEGP_FrameReceiptH h_ = nullptr;
};

class AegpMemHandleOwner final {
public:
    AegpMemHandleOwner() = default;
    AegpMemHandleOwner(const AEGP_MemorySuite1* suite, AEGP_MemHandle h) : suite_(suite), h_(h) {}
    ~AegpMemHandleOwner() { reset(); }
    AegpMemHandleOwner(const AegpMemHandleOwner&) = delete;
    AegpMemHandleOwner& operator=(const AegpMemHandleOwner&) = delete;
    AegpMemHandleOwner(AegpMemHandleOwner&& o) noexcept : suite_(o.suite_), h_(o.release()) {}
    AegpMemHandleOwner& operator=(AegpMemHandleOwner&& o) noexcept {
        if (this != &o) { reset(); suite_ = o.suite_; h_ = o.release(); }
        return *this;
    }
    AEGP_MemHandle get() const noexcept { return h_; }
    AEGP_MemHandle release() noexcept { auto h = h_; h_ = nullptr; return h; }
    void reset(AEGP_MemHandle h = nullptr) noexcept {
        if (h_ && suite_) { (void)suite_->AEGP_FreeMemHandle(h_); }
        h_ = h;
    }
private:
    const AEGP_MemorySuite1* suite_ = nullptr;
    AEGP_MemHandle h_ = nullptr;
};
