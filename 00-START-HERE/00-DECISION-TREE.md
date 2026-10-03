# Decision tree — что именно вы разрабатываете?

## 1. Нужна обработка кадра?

Да → **C++ Effect plug-in**.

Типичные задачи:
- blur, distort, keying, color, generation;
- анализ изображения;
- GPU-heavy processing;
- custom parameters в Effect Controls;
- SmartFX/MFR.

Дальше: [маршрут «Первый Effect»](../NAVIGATION.md#route-effect).

## 2. Нужно управлять самим After Effects глубже, чем позволяет scripting?

Да → **AEGP**.

Типичные задачи:
- меню и commands;
- project/layer/item access через suites;
- hooks;
- render queue integration;
- коммуникация с другими native plug-ins;
- background/idle integration в пределах поддержанного SDK.

Дальше: [маршрут «Native integration / AEGP»](../NAVIGATION.md#route-native).

## 3. Нужен собственный формат видео/изображений/аудио?

Да → **AEIO**.

Типичные задачи:
- import decoder;
- export encoder;
- interpretation/options;
- передача frames/audio между AE и codec/container implementation.

Дальше: [AEIO — media import/export plug-ins](../04-AEIO/README.md).

## 4. Нужно заменить способ, которым AE рендерит 3D layers?

Да → возможно **Artisan**.

Но если вы просто рисуете 3D внутри собственного эффекта, Artisan обычно не нужен. Это очень тяжёлый API.

Дальше: [Artisan](../05-ARTISAN/README.md).

## 5. Нужна автоматизация без тяжёлого realtime render?

Да → **ExtendScript**.

Подходит для:
- создание comps/layers;
- применение эффектов;
- keyframes;
- import/export orchestration;
- render queue;
- batch tools;
- pipeline automation.

Дальше: [маршрут «Automation tool / ScriptUI / CEP»](../NAVIGATION.md#route-automation).

## 6. Нужна dockable UI-панель?

Dockable UI сам по себе не означает обязательный выбор CEP:
- для script-based панели рассмотрите [ScriptUI](../06-SCRIPTING/02-SCRIPTUI.md);
- для HTML/JavaScript UI рассмотрите [CEP](../07-PANELS/01-CEP.md);
- если нужен именно native panel contract, см.
  [Native dockable panels](../14-NATIVE-INTEGRATIONS/07-NATIVE-PANELS.md).

На дату 2026-09-30:
- production сейчас: **CEP**;
- стратегическое направление Adobe: **UXP**;
- UXP public beta для AE заявлена на ноябрь 2026.

Дальше: [маршрут выбора и реализации UI](../NAVIGATION.md#route-automation). Ограничения и roadmap: [Panels](../07-PANELS/README.md).

## 7. Нужны и высокая скорость, и богатый UI?

Часто правильная архитектура — **hybrid**:

```text
Panel / Script UI
      ↓ commands / serialized data
Native C++ core
      ↓
AE SDK / GPU / MFR
```

UI не должен владеть render state. Native core не должен знать о DOM/UI деталях.

Дальше:
[рецепт panel + native core](../12-RECIPES/05-HYBRID-PANEL-NATIVE.md)
и [Native ↔ script/panel](../15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md).

## Red flags выбора

- «Сделаем всё AEGP, потому что он мощнее» → лишняя сложность.
- «Сделаем всё ExtendScript» → плохо для heavy pixel compute.
- «Сделаем UI прямо внутри effect custom UI» → подходит только для effect-local controls, не для полноценного приложения.
- «Начнём новый большой CEP framework» → допустимо для релиза сейчас, но только с migration boundary под UXP.
