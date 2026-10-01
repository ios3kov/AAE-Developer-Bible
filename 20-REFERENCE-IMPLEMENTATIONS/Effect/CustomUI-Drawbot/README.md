# Custom UI / Drawbot reference

Status: **acquisition skeleton / SDK 25.6 macOS syntax-checked / runtime result not claimed**.

EventSkeleton.cpp intentionally stops after obtaining the drawing reference. It does not draw a path, text, icon or control.

## Purpose

The skeleton proves the outer event/acquisition shape without pretending a partial Drawbot implementation is finished.

~~~text
PF_Cmd_EVENT
→ validate PF_EventExtra
→ accept PF_Event_DRAW
→ acquire EffectCustomUISuite
→ PF_GetDrawingReference
→ obtain Drawbot service objects
→ draw
→ release created Drawbot resources
~~~

The last drawing/resource steps are still to be implemented.

## Start from the correct SDK shell

Use Adobe Custom ECW UI / Drawbot-capable sample code from the target SDK for the full event/PiPL/UI setup.

The supplied SDK review uses Custom_ECW_UI and CCU as evidence sources.

Do not bolt EventSkeleton into an arbitrary effect and assume the necessary custom UI flags/parameter UI configuration exist.

## Event filtering

The skeleton returns immediately for non-draw events.

A real UI may need to handle:

- mouse/down/up/move;
- cursor;
- key events;
- click/drag;
- draw;
- update/invalidations.

Handle only the event types the feature actually needs.

## Drawbot ownership

Separate:

- borrowed draw/context references from AE;
- acquired Drawbot suites;
- product-created path/brush/pen/font/image objects.

Created Drawbot objects need the matching supplier/resource release API.

Do not cache per-event surface/path handles globally.

## Async manager boundary

The SDK source review documents an async-manager requirement around supported custom UI async behavior.

Do not start background UI work and later touch event-scoped Drawbot references from another thread.

If worker computation is needed:

~~~text
worker computes plain immutable data
→ host/UI callback receives result
→ reacquire current draw context
→ draw
~~~

## Coordinate/state

Before drawing define:

- effect controls window vs comp/layer context;
- coordinate conversion;
- clipping;
- device scale/HiDPI behavior;
- parameter hit regions;
- invalidation/redraw triggers.

Do not infer coordinates from one display setup.

## Acceptance path

Implement incrementally:

1. untouched sample loads;
2. drawing callback observed;
3. draw one fixed line/rectangle;
4. draw parameter-dependent shape;
5. resize/HiDPI;
6. mouse interaction if needed;
7. invalidation;
8. repeated open/close;
9. MFR render remains unaffected.

## Verification boundary

Syntax checking only proves declarations/types. This remains a skeleton until it visibly draws and its resource/event lifecycle passes in the target AE host.
