# Footage / import recipes

**Suites:** `AEGP_FootageSuite5`, `AEGP_ItemSuite9`, `AEGP_CompSuite13`, `AEGP_LayerSuite9`  
**Confidence:** architecture SDK-verified; exact import flags/path structs must be compiled against installed 26.5 headers.

## Два разных сценария

### A. Импорт уже поддерживаемого AE media

Использовать Footage Suite:

```text
path + interpretation/import options
→ NewFootage / AddFootageToProject
→ ItemH
→ optionally AddLayer(item, comp)
```

### B. Новый file format

Не Footage Suite recipe. Нужен **AEIO** или File Import Manager path — см. `04-AEIO/` и `14-NATIVE-INTEGRATIONS/08-AEIO.md`.

---

## Production checklist

Для footage учитывать:

- sequence vs single file;
- alpha interpretation;
- frame rate / conform rate;
- proxy;
- missing/relinked footage;
- UTF-16/native paths;
- Windows/macOS path conventions;
- still duration;
- color/profile interpretation.

---

## Почему здесь нет «универсальной 10-строчной функции»

Footage constructors используют version-specific structures/options и являются местом, где особенно опасно выдавать псевдо-compile код без proprietary headers. Для реально собираемого импортера стартовать от Adobe `Projector`/`IO` sample и graft-ить business logic.

Cookbook фиксирует lifecycle и suite ownership, но exact struct initializers должны идти из установленного SDK той версии, которую вы реально собираете.
