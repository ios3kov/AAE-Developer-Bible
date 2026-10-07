# Render frame → pixels

**Primary Bible baseline:** Adobe After Effects SDK **25.6 build 61**.

**Current suites:** `AEGP_RenderOptionsSuite4`, `AEGP_RenderSuite5`, `AEGP_WorldSuite3`.

The existing `RenderRecipes.cpp` source example uses the older-compatible `RenderSuite4` subset. Treat that as compatibility-shaped source, not current-suite authority.

## Core pipeline

Companion [`RenderRecipes.cpp`](code/RenderRecipes.cpp) implements the middle of
this pipeline only: it borrows already configured options, obtains a receipt,
calls a consumer with its borrowed world and checks the receipt in. It neither
creates/disposes options nor inspects/copies pixels. Its cancel callback is null,
so the cancellation design below is not implemented by this helper. The consumer
must not dispose the world or retain it/base pointers after return. Receipt RAII
protects exception paths; ordinary explicit checkin preserves primary error, but
does not separately report a secondary checkin failure.

```text
ItemH
→ RenderOptions.NewFromItem
→ configure time / field / world / downsample / ROI
→ RenderAndCheckoutFrame
→ FrameReceiptH
→ GetReceiptWorld
→ borrowed read-only WorldH
→ inspect type/size/rowbytes/base address
→ copy/consume pixels
→ CheckinFrame
→ Dispose RenderOptions
```

## Render options are product-owned

`NewFromItem` creates render options that the caller owns and must dispose through the matching RenderOptions suite.

Do not confuse:

- RenderOptionsH ownership;
- FrameReceiptH checkout;
- borrowed WorldH from receipt.

They have different cleanup.

## Defaults are not your intent

`NewFromItem` creates a defined initial configuration, but a production feature should set/read the values it depends on explicitly.

Consider:

- time;
- time step;
- field mode;
- world type;
- downsample;
- ROI;
- matte/render-guide options where relevant.

Do not let current UI state silently choose render semantics unless feature explicitly wants that.

## ROI sentinel

In the reviewed RenderOptions contract, ROI `{0,0,0,0}` means full area, not empty result.

Do not copy sentinel semantics from unrelated APIs.

## Checkout frame

```cpp
AEGP_FrameReceiptH receiptH = nullptr;

ERR(suites.RenderSuite5()->AEGP_RenderAndCheckoutFrame(
    render_optionsH,
    cancel_callbackP0,
    cancel_refconP0,
    &receiptH));
```

`receiptH` is not pixel memory. It represents the checked-out render result/lifetime.

## Receipt world

```cpp
AEGP_WorldH worldH = nullptr;
ERR(suites.RenderSuite5()->AEGP_GetReceiptWorld(receiptH, &worldH));
```

The reviewed contract describes this world as borrowed/read-only within receipt lifetime.

Do **not** dispose it through World Suite as if you allocated it.

## Pixel access

Through `WorldSuite3` inspect:

- type;
- dimensions;
- rowbytes;
- typed base address: 8/16/32.

Never assume:

```text
rowbytes == width * sizeof(pixel)
```

Never select pixel type from project settings alone; inspect returned world type.

## Copy if data must outlive receipt

If worker/helper needs pixels after host callback:

```text
while receipt valid
→ inspect metadata
→ copy required rows into product-owned buffer
→ CheckinFrame
→ hand copied buffer to worker
```

Do not keep base-address pointer after checkin.

Before comparing the owned copy with an exported file, calibrate both paths with
identity/ramp/impulse controls and record actual world type versus decoded file
precision, alpha/profile/transforms. A 32-bpc project exported as unsigned RGBA16
does not validate native HDR or NaN preservation. Use the
[pixel calibration route](../02-EFFECT-PLUGINS/06-COLOR-PIXELS.md) and
[worked NOT_RUN evidence plan](../13-TEMPLATES/examples/WORKED-EXAMPLE.md);
the receipt helper does not implement this calibration or decoder.

## Checkin is mandatory

```cpp
ERR2(suites.RenderSuite5()->AEGP_CheckinFrame(receiptH));
receiptH = nullptr;
```

Receipt release participates in host cache/resource lifecycle.

Use cleanup even if pixel consumer fails.

## Preserve primary error

Pattern:

```text
render succeeds
→ consumer fails
→ checkin also fails
```

Report consumer/primary error as primary cause, while logging cleanup failure separately.

Do not overwrite the real error accidentally with cleanup status.

## Rendered region

`AEGP_GetRenderedRegion` can describe the useful rendered region.

Do not assume whole world contains newly-computed full-frame output for every caching/partial-render scenario.

## Do not mutate receipt world

If algorithm needs writable pixels, allocate/copy into your own buffer/world.

Borrowed cached world is not scratch memory.

## Layer render boundaries

Layer render options can represent different boundaries:

- normal layer with configured effects-to-render;
- upstream of effect;
- downstream of effect.

These are not equivalent to:

- final composition frame;
- UI viewer pixels;
- Render Queue encoded output.

Document which boundary your feature needs.

## RenderSuite5 async layer rendering

Current SDK 25.6 RenderSuite5 includes async layer-frame request/cancel APIs.

Async architecture requires:

- request ID;
- refcon lifetime;
- cancellation state;
- callback result;
- shutdown behavior.

Header notes callback guarantee has shutdown exception. Therefore do not design cleanup assuming callback always arrives during AE shutdown.

## UI-thread blocking

Current source comments steer long UI workflows toward async behavior, with only narrow cases appropriate for synchronous UI-thread render.

Do not put synchronous render checkout in every panel refresh/paint event.

## Cancellation

For synchronous APIs with cancel callback:

- keep callback cheap;
- make product consumer abortable;
- still release receipt/options correctly.

Cancel is not permission to leak checked-out resources.

## Recursive render danger

Be careful if a plug-in requests rendering of content whose dependency graph can call back into the requesting plug-in.

Potential outcomes:

- recursive render;
- cycle;
- deadlock;
- huge repeated work.

Model dependency boundary explicitly.

## Current RenderSuite5 vs source recipe RenderSuite4

The SDK 25.6 header exposes current `AEGP_RenderSuite5`.

`RenderRecipes.cpp` uses `RenderSuite4` for a smaller compatibility-shaped receipt/world/checkin pattern.

Do not cast suite generations.

For new current-baseline documentation use Suite5; when reading the recipe, read its declared Suite4 dependency literally.

## Cache-related APIs

Render Suite also includes timestamp/change/usefulness/checkin-rendered-frame functionality.

Do not confuse:

- `CheckinFrame(receipt)` — release checked-out frame;
- `CheckinRenderedFrame(...)` — submit/adopt a separately rendered platform world.

Similar names, different ownership semantics.

## Product workflow

1. Decide item/layer render boundary.
2. Create owned render options.
3. Set explicit time/format/ROI.
4. Render/checkout.
5. Validate receipt/world/type.
6. Copy data if needed beyond callback.
7. Checkin receipt on every path.
8. Dispose options.
9. Preserve primary + cleanup errors.

## Related chapters

- [Project/render automation](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)
- [Pixels/color](../02-EFFECT-PLUGINS/06-COLOR-PIXELS.md)
- [Render Queue](11-RENDER-QUEUE.md)
- [Memory/undo](12-MEMORY-UNDO-PERSISTENCE.md)
- [SDK 25.6 project/render review](../18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md)

## Evidence boundary

`RenderOptionsSuite4`/`RenderSuite5`/`WorldSuite3` current-baseline contracts are source-reviewed against SDK 25.6. Source examples do not imply a host-observed frame result.
