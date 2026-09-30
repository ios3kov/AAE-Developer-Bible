# Composition recipes

**Suite:** `AEGP_CompSuite13` for AE 26.5-specific features; older functions remain available through the current suite.  
**Confidence:** SDK-verified.

## Создать comp

```cpp
A_Time duration{10, 1}; // 10 seconds
A_Ratio par{1, 1};
A_Ratio fps{25, 1};

AEGP_CompH compH = nullptr;
ERR(suites.CompSuite13()->AEGP_CreateComp(
    parent_folderH,
    utf16_name,
    1920,
    1080,
    &par,
    &duration,
    &fps,
    &compH));
```

Порядок: parent folder → name → dimensions → PAR → duration → frame rate → output handle.

---

## Получить comp из project item

```cpp
AEGP_CompH compH = nullptr;
ERR(suites.CompSuite13()->AEGP_GetCompFromItem(itemH, &compH));
```

И обратно:

```cpp
AEGP_ItemH comp_itemH = nullptr;
ERR(suites.CompSuite13()->AEGP_GetItemFromComp(compH, &comp_itemH));
```

---

## Создать solid

```cpp
AEGP_LayerH solid_layerH = nullptr;
PF_Pixel color{};
color.alpha = 255;
color.red   = 255;
color.green = 0;
color.blue  = 0;

ERR(suites.CompSuite13()->AEGP_CreateSolidInComp(
    utf16_name,
    500,
    500,
    &color,
    compH,
    nullptr,          // duration: use host/default contract as appropriate
    &solid_layerH));
```

Точную optional-duration семантику сверять с headers версии SDK.

---

## Создать camera / light / text layer

```cpp
AEGP_LayerH cameraH = nullptr;
AEGP_LayerH lightH  = nullptr;
AEGP_LayerH textH   = nullptr;

ERR(suites.CompSuite13()->AEGP_CreateCameraInComp(
    utf16_camera_name, center_point, compH, &cameraH));

ERR(suites.CompSuite13()->AEGP_CreateLightInComp(
    utf16_light_name, center_point, compH, &lightH));

ERR(suites.CompSuite13()->AEGP_CreateTextLayerInComp(
    compH, TRUE, &textH));
```

`center_point` type/coordinates брать из installed SDK declaration; не подменять screen-space и comp-space координаты.

---

## 26.5: parametric mesh layer

`AEGP_CompSuite13` добавляет `AEGP_CreateParametricMeshLayerInComp`. Это **feature-gated** recipe:

```text
Acquire/compile against CompSuite13
→ call CreateParametricMeshLayerInComp
→ older host? disable this command
```

Не делайте весь plug-in AE 26.5-only, если mesh — необязательная функция.

---

## Получить marker stream composition

В актуальном CompSuite доступен comp marker stream. Дальше он обрабатывается обычными Stream/Keyframe/Marker suites.

Архитектура:

```text
CompH
→ GetNewCompMarkerStream
→ StreamRefH
→ KeyframeSuite (times)
→ StreamSuite (values)
→ MarkerSuite (marker contents)
→ DisposeStream
```
