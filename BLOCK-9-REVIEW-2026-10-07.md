# Block 9 — bounded UI/audio walkthroughs

Draw route checked against SDK 25.6 Custom_ECW_UIUI.cpp:95–209: borrowed drawing
supplier/surface, created path/brush, AddRect/FillPath and ReleaseObject cleanup.
Hit/drag model separates transient gesture from persisted parameter and render.
Functional delivery/readback/pixels/Undo/latency are distinct product claims.

Audio gains a concrete 480-frame stereo/float32 DSP example with count/bytes,
gain and finite-input policy. It is not an AUDIO_RENDER implementation; no invented
host scheduling or IIR guarantee. Async UI remains explicitly limited. No host run.
