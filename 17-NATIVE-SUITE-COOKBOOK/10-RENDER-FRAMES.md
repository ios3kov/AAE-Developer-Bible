# Render frame → pixels

**Suites:** `AEGP_RenderOptionsSuite4`, `AEGP_RenderSuite4`, `AEGP_WorldSuite3`  
**Confidence:** SDK-verified.

## Pipeline

```text
ItemH
→ RenderOptions.NewFromItem
→ configure time / world / field / downsample
→ RenderAndCheckoutFrame
→ FrameReceiptH
→ GetReceiptWorld
→ WorldH
→ GetBaseAddr8/16/32 + dimensions/rowbytes
→ read/copy pixels
→ CheckinFrame
→ Dispose RenderOptions
```

## Checkout frame

```cpp
AEGP_FrameReceiptH receiptH = nullptr;

ERR(suites.RenderSuite4()->AEGP_RenderAndCheckoutFrame(
    render_optionsH,
    nullptr,     // optional cancel callback
    nullptr,     // cancel refcon
    &receiptH));
```

`receiptH` — не pixels.

## Получить world

```cpp
AEGP_WorldH worldH = nullptr;
ERR(suites.RenderSuite4()->AEGP_GetReceiptWorld(
    receiptH,
    &worldH));
```

`worldH` принадлежит frame receipt/host. Не dispose-ить его как ваш allocated world.

## Получить pixels

Через World Suite:

```text
GetType → 8/16/float world
GetSize
GetRowBytes
GetBaseAddr8 / GetBaseAddr16 / GetBaseAddr32
```

Никогда не считать `rowbytes == width * sizeof(pixel)`.

## Обязательный check-in

```cpp
ERR2(suites.RenderSuite4()->AEGP_CheckinFrame(receiptH));
receiptH = nullptr;
```

AE делает caching decisions на основе checked-out receipts. Держать receipt дольше нужного нельзя.

## Rendered region

Partial rendering/caching означает, что полезно проверять:

```cpp
A_LRect rendered{};
ERR(suites.RenderSuite4()->AEGP_GetRenderedRegion(
    receiptH, &rendered));
```

Не предполагать автоматически, что весь world содержит новый render.

## Не мутировать полученный cached world

Если нужно изменять pixels — копировать в собственный world/buffer. Receipt world — результат host render/cache, не ваша scratch-память.

## Threading

Некоторые исторические render calls на UI thread deprecated/ограничиваются. Не строить новую архитектуру на синхронном UI-thread render loop. Для UI thumbnails/analysis продумать asynchronous/cache-friendly design и сверить актуальные 26.5 ограничения.

## Infinite render recursion

Если Effect A рендерит layer, содержащий Effect B, который делает симметричный checkout обратно, можно получить recursive render/deadlock. Особенно осторожно с `RenderAndCheckoutLayerFrame`.
