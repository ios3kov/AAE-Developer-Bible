# Custom UI and Drawbot

Обновлено **2026-10-01** по Adobe After Effects SDK **25.6 build 61**.

Custom UI — часть Effect API. Drawbot — host drawing abstraction, используемая внутри event-driven UI. Это не отдельная HTML/panel technology.

Source review: [GPU, audio and Custom UI / Drawbot](../18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md).

## 1. Когда нужен Custom UI

Используйте native standard parameters, пока задача решается slider/checkbox/color/popup/layer control.

Custom UI нужен для:

- overlay handles;
- custom visualization;
- специализированного control внутри Effect Controls;
- drawing в Layer/Comp view;
- interaction, которой нет в стандартном parameter widget.

Rich application UI с asset browser/accounts/web content — отдельная panel architecture.

## 2. Три части контракта

Custom UI требует согласования трёх вещей:

```text
GLOBAL_SETUP
  PF_OutFlag_CUSTOM_UI
        ↓
register_ui(PF_CustomUIInfo)
  declare contexts/events/size
        ↓
PF_Cmd_EVENT
  handle PF_EventExtra
```

Одного `PF_Cmd_EVENT` case недостаточно.

## 3. Event lifecycle

SDK 25.6 перечисляет:

- NEW_CONTEXT;
- ACTIVATE;
- DO_CLICK;
- DRAG;
- DRAW;
- DEACTIVATE;
- CLOSE_CONTEXT;
- IDLE;
- ADJUST_CURSOR;
- KEYDOWN;
- MOUSE_EXITED.

`PF_EventExtra` содержит event type, type-specific union, context/window information, callbacks и in/out flags.

Не читайте поле union, не соответствующее текущему `e_type`.

## 4. Handled event

Если plug-in обработал event, выставляйте соответствующий event output flag только после успешной обработки.

Bundled `Custom_ECW_UI` помечает draw/click paths `PF_EO_HANDLED_EVENT`.

Не ставьте handled заранее, если затем возвращается ошибка или событие не было обработано.

## 5. Drawbot drawing reference

В draw event текущий custom-UI suite позволяет получить drawing reference из event context.

Далее Drawbot:

```text
DrawRef
  -> borrowed SupplierRef
  -> borrowed SurfaceRef

Supplier
  -> created Brush/Pen/Path/Font...
     -> ReleaseObject required
```

Главная ownership-ошибка: supplier/surface, полученные через DrawRef, **не освобождаются как созданные объекты**. А созданные brush/path/font нужно release.

Bundled sample прямо комментирует это различие.

## 6. Acquire/release Drawbot suites

`Custom_ECW_UI`:

1. acquires Drawbot suite set;
2. acquires effect custom-UI suite to get drawing reference;
3. gets supplier/surface;
4. creates draw resources;
5. draws;
6. releases created objects;
7. releases acquired suites.

C++ helper/scoper можно использовать только если его lifetime совпадает с event scope.

Не кешируйте event drawing references между contexts без explicit guarantee.

## 7. Coordinates

Custom UI имеет разные window contexts. Coordinate conversion нужно делать через event/host callbacks, а не считать screen/layer/comp coordinates одинаковыми.

HiDPI/Retina support означает избегать hard-coded physical-pixel assumptions. Размер линии/handle и hit testing должны тестироваться на scale changes.

## 8. Invalidation и redraw

Redraw request и render request — разные операции.

`PF_OutFlag_REFRESH_UI` просит перерисовку UI.

`PF_OutFlag_FORCE_RERENDER` влияет на render invalidation и имеет дополнительные sequence-data требования в современном threading model.

Не используйте FORCE_RERENDER как универсальный «обновить интерфейс».

## 9. Async custom UI

SDK 25.6 документирует `PF_OutFlag2_CUSTOM_UI_ASYNC_MANAGER`.

Header прямо предупреждает: после разделения UI/render threads кадры для custom UI не следует синхронно рендерить из UI thread. Async manager:

- отслеживает async frame requests;
- повторно вызывает DRAW при готовности;
- может отменять устаревшие requests при scrub/project changes.

Это означает, что UI code должен уметь рисовать **текущее доступное состояние**, а не блокировать интерфейс до готовности кадра.

В текущей Bible нет host-verified async-manager example — не скрываем этот пробел.

## 10. Input interaction

DO_CLICK и DRAG — разные event phases. Cursor adjustment — отдельный event.

Рекомендуемый state machine:

```text
DO_CLICK
  validate hit
  capture interaction state

DRAG
  derive new value from current pointer
  update supported parameter/state
  request redraw/rerender appropriately

release/end
  finish transient state
```

Не выполняйте тяжелый render в drag handler.

## 11. UI state vs render state

Interaction state может быть transient, но любое состояние, влияющее на final pixels, должно участвовать в project/render dependency model.

Не храните важный render parameter только в widget/global variable.

## 12. Drawbot resource safety

На каждом error path:

- release objects already created;
- release suite acquisitions;
- preserve original error unless cleanup failure is the only error;
- do not release borrowed supplier/surface.

Для сложного UI лучше RAII wrappers, но wrappers должны кодировать **разные ownership classes**, а не один generic delete.

## 13. Test matrix

- Effect Controls draw;
- Comp/Layer overlay, если заявлено;
- click/drag;
- cursor;
- context open/close;
- parameter automation while UI open;
- zoom/pan;
- HiDPI/Retina;
- theme/background variants;
- project switch/close;
- repeated open/close;
- async rendered-frame cancellation;
- error injection/resource leak check.

## Verification boundary

Bundled Custom_ECW_UI/CCU source reviewed. Bible не заявляет собственный UI runtime result; отдельная demo implementation/host QA не является completion requirement документации.
