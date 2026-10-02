# Custom UI / Drawbot reference

Status: **SOURCE EXAMPLE — acquisition skeleton / RUNTIME-NOT-CLAIMED**. SDK contract basis: 25.6 build 61.

EventSkeleton.cpp intentionally stops after obtaining the drawing reference. It does not draw a path, text, icon or control.

## Purpose

The skeleton illustrates the outer event/acquisition shape; drawing and interaction remain outside this source example.

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

## Product-validation path

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

This source example stops at acquisition; it does not draw or claim host interaction. The [historical compiler record](../../../VERIFICATION.md#recorded-baseline-2026-09-30) lacks exact tested source identity and cannot establish compilation of the current skeleton. To claim drawing/resource/event behavior for a product, implement those paths and record their execution on the identified target AE build. The bounded acquisition example is valid editorial material without that product result.
