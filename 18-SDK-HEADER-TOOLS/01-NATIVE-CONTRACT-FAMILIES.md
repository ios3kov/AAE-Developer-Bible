# Native contract families — кто кого вызывает

## 1. Effect plug-in

**Модель:** AE → ваш entry point → `PF_Cmd_*` selector.

Ваш effect не «крутит AE сам». Host вызывает effect в нужные моменты: global setup, params setup, sequence lifecycle, render/SmartFX, UI events, audio и т.д. Для дополнительных host-сервисов effect получает/приобретает PF/PICA suites.

## 2. AEGP

**Модель:** AE → registered hooks вашего AEGP; AEGP → AE через `AEGP_*SuiteN`.

AEGP подходит для project graph, items, comps, layers, streams, effects, keyframes, render queue, native commands/hooks и другой глубокой автоматизации.

## 3. AEIO

**Модель:** AEGP register → AE хранит ваш `AEIO_FunctionBlockN` → AE вызывает callbacks для import/output lifecycle.

Это callback table, а не обычная «suite, которую дергает бизнес-логика».

## 4. Artisan

**Модель:** AEGP register → AE вызывает `PR_ArtisanEntryPoints` для host-controlled 3D rendering pipeline.

Не использовать как универсальный render replacement для обычных 2D comps.

## 5. PICA/SweetPea

**Модель:** `SPBasicSuite::AcquireSuite(name, version, &ptr)` → вызовы function table → `ReleaseSuite`.

Это транспорт большинства native service contracts. Suite pointer нельзя считать вечным глобальным объектом вне host lifetime.

## 6. Drawbot

Effect/host UI получает Drawbot suites и рисует через supplier/surface/path/font contracts. Это host-integrated custom UI, а не произвольный Cocoa/Win32 canvas.

## 7. Script / panel

ExtendScript и CEP/UXP находятся **выше** native ABI. Они общаются с scripting object model, а не напрямую с `AEGP_LayerSuite9*`.

Если hybrid продукту нужен bridge в native core, контракт bridge должен быть явным: command/protocol + version + validation + threading boundary. См. `15-COMMUNICATION/`.
