# Effect plug-ins

Effect plug-in — основной путь, если инструмент должен обрабатывать/генерировать pixels или audio внутри стандартного effect pipeline AE.

## Маршрут чтения по SDK 25.6

**Обновлено 2026-10-01 по присланной поставке SDK.** Это сверка учебных глав с заголовками и образцами, не новый результат запуска плагинов в AE.

1. [Устройство Effect-плагина](01-ANATOMY.md): регистрация, команды, параметры и время жизни данных на примере Skeleton.
2. [Параметры и UI](02-PARAMETERS-UI.md): индексы/IDs, setup-макросы, запрет анимации, supervised-изменения, UI-only и ограничения UPDATE_PARAMS_UI; глава расширена по SDK.
3. [SmartFX](03-SMARTFX.md): зависимости, области, checkout IDs и различающиеся правила cleanup.
4. [Цвет и пиксели](06-COLOR-PIXELS.md): ARGB32/64/128, диапазон 16 bpc, typed access, stride/origin, alpha, working-space color и отделение экспорта; глава расширена по SDK.
5. [Дополнительные каналы](08-AUXILIARY-CHANNELS.md): глубина, ID, нормали, descriptors, типы и сырые buffers.
6. [Память, lifetime и ошибки](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md): owned/borrowed/transferred ресурсы, state handles, различия flattening, обязательный cleanup и ограничения существующих RAII helpers.
7. [MFR и потокобезопасность](04-MFR-THREAD-SAFETY.md): действующие flags, пересечение selectors, read-only sequence state, mutable render copies и Compute Cache с точными режимами ожидания. Глава расширена по SDK; MFR-тесты не объявляются выполненными.
8. [GPU effects](05-GPU.md): capability chain, per-device state, GPU worlds, allocation ownership, framework/device boundaries and CPU↔GPU acceptance.
9. [Audio effects](07-AUDIO.md): audio selectors, SoundWorld, checkout/checkin, format/history semantics and missing bundled sample boundary.
10. [Custom UI / Drawbot](09-CUSTOM-UI-DRAWBOT.md): event lifecycle, Drawbot ownership, invalidation and async custom-UI boundary.

[Первая сверка поставки](../18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md), [сверка параметров/пикселей](../18-SDK-HEADER-TOOLS/06-PARAMETERS-PIXELS-SDK25.6.md), [сверка памяти/MFR](../18-SDK-HEADER-TOOLS/07-MEMORY-MFR-SDK25.6.md) и [GPU/audio/Custom UI review](../18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md) содержат SHA-256, диапазоны источников и границы проверки. Расхождения комментариев и образцов сохраняются явно. Учебные фрагменты не являются новыми эталонными плагинами; обновление текста не закрывает сборку, загрузку и рендер примеров.

## Порядок разработки

1. Взять **Skeleton** или максимально близкий SDK sample.
2. Добиться clean build и загрузки без собственных изменений.
3. Переименовать sample и PiPL identifiers.
4. Реализовать CPU reference path.
5. Добавить 8/16/32-bpc correctness.
6. Перевести на SmartFX там, где это оправдано/необходимо.
7. Сделать thread-safe.
8. Только после соответствующей проверки включать MFR capability в поставляемой сборке; для самой проверки нужна отдельная тестовая сборка с флагом.
9. Добавить GPU backend, если benchmark доказывает пользу.
10. Custom UI — последним, после стабильной render core.

Это рекомендуемый порядок собственной разработки. Конкретный Skeleton из поставки 25.6 имеет classic 8/16-bpc ветви, но не является готовой 32-bpc/MFR реализацией; это разобрано в первой главе. Даже до включения MFR учитывайте потокобезопасность используемых iterate callbacks.

## Production layers

```text
AE entry point / selectors
        ↓
Adapter: PF_* ↔ internal types
        ↓
Pure render core
        ↓
CPU backend / GPU backend
        ↓
Tests + golden images
```

Чем меньше AE-specific типов проходит в render core, тем проще тестировать алгоритм вне After Effects.
