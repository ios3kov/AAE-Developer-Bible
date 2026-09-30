# Guides / Item Views / Selection

## AE 26.5 Guide Suite

**Suites:** `AEGP_GuideSuite2`, `AEGP_ItemViewSuite2`  
**Confidence:** 26.5 SDK release verified.

GuideSuite2 умеет:
- horizontal/vertical guide;
- pixel/percentage position;
- per-guide color;
- edge pinning.

ItemViewSuite2 управляет per-view:
- guides visible;
- snap;
- locked.

## Feature gating

Это новый API. Архитектура:

```text
host supports GuideSuite2?
  yes → full percentage/color/pinning
  no, GuideSuite1? → basic orientation/pixel position
  no → disable guide feature only
```

Не падать загрузкой всего AEGP.

---

## Почему Guide и ItemView разные

Guide object/data относится к item/layer guide model. `ItemViewSuite` — к конкретному view/UI state. Поэтому «создать guide» и «показывать guides в этом view» — разные операции.

---

## Selection / Collection

**Suite:** `AEGP_CollectionSuite2`

Collection API используется для selection-like host collections. Не хранить collection handle как долговечную модель приложения. Считать его snapshot/host object с собственным lifecycle.

Для бизнес-логики лучше переводить selection в:
- ItemID;
- LayerID;
- effect match name + layer identity;
- собственную immutable command model.

---

## Command pattern

UI callback:

```text
query current selection
→ normalize to stable IDs
→ validate
→ StartUndoGroup
→ mutate
→ EndUndoGroup
→ drop temporary collection/refs
```

Так native panel/menu command не становится зависимым от stale UI handles.
