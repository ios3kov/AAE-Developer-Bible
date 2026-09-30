# PICA suites — внутренний native service bus After Effects

## Что это

PICA (Plug-In Component Architecture) — versioned function-suite mechanism. `SPBasicSuite` даёт `AcquireSuite`/`ReleaseSuite`; конкретные API After Effects организованы в suites.

Для C++ effect обычно используется `AEFX_SuiteScoper`, который RAII-способом acquire/release нужный suite.

```cpp
AEFX_SuiteScoper<PF_GPUDeviceSuite1> gpu(
    in_data,
    kPFGPUDeviceSuite,
    kPFGPUDeviceSuiteVersion1,
    out_data);

gpu->GetDeviceInfo(in_data->effect_ref, device_index, &info);
```

## Почему suite имеет номер версии

Имя + версия — часть ABI contract. Новый suite version может добавлять/менять signature, при этом старые версии могут оставаться доступными.

Правильный pattern:

```text
try newest suite
  -> available: use it
  -> missing: acquire older supported version
  -> still missing: disable feature or fail explicitly
```

## Основные AEGP suite-группы

- Memory
- Command / Register
- Project / Item / Collection
- Composition / Layer / Stream / Dynamic Stream
- Effect / Mask / Keyframe / Marker
- Footage / File Import
- Text / Text Layer
- Utility / Persistent Data
- Render / World / Composite
- Render Queue / Render Queue Item / Output Module / Render Options
- Color Settings
- PF Interface
- Iterate
- Guide / Item View (26.5 additions include Guide APIs)

Список версий всегда сверять с headers конкретного SDK.

## Thread rule

По умолчанию считать suite calls **не thread-safe**, пока документация конкретной функции не говорит обратное. AEGP project/UI mutations — main/UI thread only.

## Plug-in published suite

AEGP может опубликовать свой suite для других plug-ins. Это лучший native in-process bridge, когда несколько модулей одного продукта должны совместно использовать сервис:

```text
Effect A ----AcquireSuite("com.acme.CoreSuite", v1)---> AEGP Core
Effect B ----AcquireSuite("com.acme.CoreSuite", v1)---> AEGP Core
```

Преимущества:
- ABI contract явный;
- нет зависимости от load order на уровне прямых pointers;
- можно versioning suite;
- меньше hidden globals.

См. `16-WORKING-TEMPLATES/pica-shared-suite/`.
