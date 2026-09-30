# Layer recipes

**Suites:** `AEGP_LayerSuite9`, `AEGP_CompSuite13`  
**Confidence:** SDK-verified. `AEGP_AddLayer` signature additionally checked against header-derived bindings.

## Количество слоёв и layer по index

```cpp
A_long count = 0;
ERR(suites.LayerSuite9()->AEGP_GetCompNumLayers(compH, &count));

for (A_long i = 0; i < count && !err; ++i) {
    AEGP_LayerH layerH = nullptr;
    ERR(suites.LayerSuite9()->AEGP_GetCompLayerByIndex(compH, i, &layerH));
    // use layerH now
}
```

Не полагаться на index как на persistent identity.

---

## Добавить footage/project item как layer

Сначала проверить legality:

```cpp
A_Boolean validB = FALSE;
ERR(suites.LayerSuite9()->AEGP_IsAddLayerValid(itemH, compH, &validB));

if (validB) {
    AEGP_LayerH new_layerH = nullptr;
    ERR(suites.LayerSuite9()->AEGP_AddLayer(
        itemH,
        compH,
        &new_layerH));
}
```

### Docs erratum

В некоторых версиях публичной HTML-страницы третий аргумент `AEGP_AddLayer` отображался как `A_Boolean*`. Header-derived contract — `AEGP_LayerH*`.

---

## Stable identity: Layer ID

```cpp
AEGP_LayerIDVal id = 0;
ERR(suites.LayerSuite9()->AEGP_GetLayerID(layerH, &id));
```

Позже:

```cpp
AEGP_LayerH freshH = nullptr;
ERR(suites.LayerSuite9()->AEGP_GetLayerFromLayerID(compH, id, &freshH));
```

Это предпочтительнее хранения `LayerH` через длинную цепочку UI операций.

---

## Переименовать layer

```cpp
ERR(suites.LayerSuite9()->AEGP_SetLayerName(layerH, utf16_name));
```

---

## Duplicate

```cpp
AEGP_LayerH duplicateH = nullptr;
ERR(suites.LayerSuite9()->AEGP_DuplicateLayer(
    layerH,
    &duplicateH));
```

После duplicate пересчитать layer indices.

---

## Parent layer

```cpp
AEGP_LayerH parentH = nullptr;
ERR(suites.LayerSuite9()->AEGP_GetLayerParent(layerH, &parentH));

ERR(suites.LayerSuite9()->AEGP_SetLayerParent(
    layerH,
    new_parentH));
```

Перед parent operation проверять cycle/host legality, если API предоставляет соответствующую проверку.

---

## Delete

```cpp
ERR(suites.LayerSuite9()->AEGP_DeleteLayer(layerH));
layerH = nullptr;
```

Никаких вызовов по удалённому handle.
