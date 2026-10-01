# Legacy / historical native integration boundaries

Обновлено **2026-10-01** по присланному **SDK 25.6 build 61**.

Цель этой главы — не составить музей старых API, а помочь разработчику понять, **что в bundled samples является историческим pattern, а что является текущей сигнатурой header 25.6**.

Подробная сверка: [PICA, Effect↔AEGP и legacy boundaries](../18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).

## 1. Bundled sample не равен current suite generation

В одной и той же поставке 25.6 находятся sample-файлы, написанные против более старых suite generations.

Конкретные примеры:

- `ProjDumper` использует `EffectSuite2` и `StreamSuite2`;
- `Streamie` использует `DynamicStreamSuite2` и старые stream call shapes;
- current header 25.6 содержит `StreamSuite6`, `DynamicStreamSuite4`, `KeyframeSuite5`, `EffectSuite4`.

Поэтому правило:

```text
sample = evidence of workflow/pattern
current header = compile-time signature source of truth
```

Копировать старую строку вызова без сверки нельзя.

## 2. Generic Effect call: наглядная версия-маркер

`ProjDumper` вызывает старую форму `AEGP_EffectCallGeneric(plugin, effect, time, extra)`.

Current `EffectSuite4` добавляет отдельный `PF_Cmd effect_cmd`; header говорит передать `PF_Cmd_COMPLETELY_GENERAL` для старого поведения.

Это хороший пример эволюции API внутри поставки: sample полезен как сценарий, но новая реализация должна следовать текущему declaration.

## 3. Commando initializer — не current prototype

Bundled `Commando.cpp/.h` объявляет initializer с дополнительными `file_pathZ` и `res_pathZ` и завершает его `void* global_refconPV`.

Current `AE_GeneralPlug.h` определяет `AEGP_PluginInitFuncPrototype` иначе: `SPBasicSuite*`, driver major/minor, `AEGP_PluginID`, `AEGP_GlobalRefcon*`.

Следствие для Библии: Commando можно читать как исторический hook/menu pattern, **но нельзя использовать его initializer signature как современный шаблон 25.6**.

Мы не утверждаем здесь, почему этот старый sample остаётся в архиве или как конкретный AE build обрабатывает его binary; host execution не проводился.

## 4. Старые UI / keyframer / format пути

Ранее краткая версия главы перечисляла ADM, FPF и Photoshop-format paths слишком обобщённо.

В просмотренном архиве 25.6 нет отдельного top-level sample family с именами ADM/FPF/Keyframer. Наличие старой документации или вспомогательных Photoshop-named headers в SP tree само по себе **не доказывает текущую поддержку конкретного plug-in format в AE 25.6**.

Поэтому такие темы должны иметь одну из меток:

- **support-only** — разбор существующего legacy продукта;
- **migration-source** — источник идей/данных при переносе;
- **do-not-start** — не выбирать как базовую архитектуру нового продукта без отдельного подтверждения.

Если понадобится реальная поддержка legacy продукта, нужно отдельно поднять его target SDK/headers/sample и проверить host.

## 5. Что считать legacy smell в новом коде

Не переносить без проверки:

- suite suffix/version из старого sample;
- старый initializer prototype;
- 32-bit-only pointer assumptions;
- Carbon/CFM-era platform code;
- raw global mutable state, рассчитанный на single-frame execution;
- hard-coded Intel-only архитектуру;
- старый command/menu behavior как вечную гарантию;
- buffer/string signatures, которые в current suite уже возвращают MemorySuite handle.

## 6. Version-gating в самой Библии

Каждая source-backed глава должна различать:

```text
SDK 25.6 current header
bundled older sample generation
later SDK note
historical observation
host-verified behavior
```

Нельзя переносить функцию из later SDK в baseline 25.6 только потому, что имя похоже.

Нельзя также объявлять старый sample «сломанный» только из-за отличия от current header: без сборки/host execution это **source discrepancy / version boundary**, а не runtime defect.

## 7. Практическая миграция

Для старого native plug-in:

1. зафиксировать исходный SDK и host, где он реально работал;
2. выписать используемые suite names/versions;
3. сравнить current declarations;
4. заменить только подтверждённые changed contracts;
5. сохранить project/parameter compatibility отдельно;
6. собрать с warnings-as-errors;
7. выполнить host lifecycle tests;
8. только после этого удалять compatibility branches.

См. также:

- [PICA suites](03-PICA-SUITES.md)
- [AEGP → Effect](../15-COMMUNICATION/03-AEGP-TO-EFFECT.md)
- [SDK verification policy](../18-SDK-HEADER-TOOLS/README.md)
