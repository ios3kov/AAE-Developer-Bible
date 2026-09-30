# AEGP keyframer reference

Status: **sample-derived / host-test-required**.

`KeyframeRecipes.cpp` is the verified-shape recipe layer used by the native suite cookbook. The surrounding AEGP registration/menu shell is the same as `../MenuTool`. Combine them rather than creating a second lifecycle implementation.

Key idea: obtain a stream, start an undo group, use the keyframe suite's add/insert/set calls, dispose temporary stream refs, then end undo. Never retain host-owned refs beyond their documented lifetime.
