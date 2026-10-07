# PiPL, регистрация и загрузка плагина

**Основа: SDK 25.6 build 61, редакция 2026-10-01.** Здесь разбираются исходники Skeleton, его ресурс и проекты сборки, а также AEGP-ресурс Easy Cheese. Это не отчёт о загрузке нового бинарника. [Источники, SHA-256 и границы проверки](../18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md).

Главная практическая мысль: **скомпилированная библиотека, правильно описанный плагин и реально загруженный плагин — три разных результата**. Исправный C++ не компенсирует отсутствующий ресурс; правильное имя в ресурсе не создаёт экспортируемую функцию; наличие файла в папке не подтверждает, что AE использует именно его.

## 1. Три контракта, которые нельзя смешивать

В просмотренной поставке видны три разных механизма:

| Механизм | Его задача | Где смотреть |
|---|---|---|
| PiPL — ресурс описания плагина | Kind, имя, категория, архитектурная точка входа, версии и другие свойства | `Examples/Resources/AE_General.r`; ресурсы `.r` образцов |
| Effect registration entry | Передать host сведения об эффекте через предоставленный callback | `AE_PluginData.h`; `PluginDataEntryFunction2` в Skeleton |
| Исполняемая точка входа | Обработать PF_Cmd для Effect либо инициализировать AEGP и зарегистрировать hooks | `EffectMain` либо `AEGP_PluginInitFuncPrototype` |

Источники: `Examples/Headers/AE_PluginData.h:61–94`, `Examples/Template/Skeleton/Skeleton.cpp:219–250`, `Examples/Headers/AE_GeneralPlug.h:4167–4176`.

PiPL — описательные данные; `PluginDataEntryFunction2` и `EffectMain` — разные функции. Наличие callback-регистрации не даёт оснований выкинуть `.r` из проекта: Skeleton в этой поставке содержит оба механизма. Обратное тоже неверно: строка `EffectMain` в `.r` не реализует registration entry.

**Не следует превращать эту таблицу в выдуманный универсальный порядок работы загрузчика.** По этим исходникам не установлены все правила приоритета PiPL/callback, повторного сканирования и кэширования регистрации в разных версиях AE.

## 2. Что именно описывает SkeletonPiPL.r

`Examples/Template/Skeleton/SkeletonPiPL.r:8–69` задаёт Kind `AEEffect`, отображаемые имя и категорию, архитектурные записи `EffectMain`, формат PiPL 2.0, effect API major/minor, версию продукта, две группы outflags, match name, reserved info и support URL.

Ресурсный язык определяет `AEEffect` как `'eFKT'`, а `AEGP` как `'AEgx'`. Отдельный литерал `AEGeneral` имеет значение `'AEgp'`; нельзя заменять один другим только потому, что слова похожи. Основание: `Examples/Resources/AE_General.r:28–37`.

Полезно вести отдельную таблицу идентичности собственного продукта:

| Поле | Пример назначения | С чем не путать |
|---|---|---|
| Имя файла/bundle | Имя устанавливаемого артефакта | Не match name и не имя функции |
| Отображаемое Name | Название инструмента в интерфейсе | Не стабильный ID параметра |
| Match name | Техническое имя эффекта, отдельно передаваемое registration callback | Не Category и не CFBundleIdentifier |
| Entry point | Имя экспортированного символа | Не название продукта |
| CFBundleExecutable | Исполняемый файл внутри macOS bundle | Не ресурс PiPL |
| Build ID / SHA-256 | Идентификация конкретной поставки и её байтов | Не effect API version |

Поля Name/MatchName/Category/EntryPoint раздельны в `AE_PluginData.h:61–76`; macOS executable/identifier отдельно заданы в `Skeleton.plugin-Info.plist:5–16`. Рекомендация Библии — сохранять эту раздельность в build metadata и диагностике. Правила миграции опубликованного эффекта рассматриваются вместе с [параметрами и совместимостью проектов](../02-EFFECT-PLUGINS/02-PARAMETERS-UI.md), а не сводятся к переименованию файла.

## 3. Архитектурная запись не создаёт архитектуру

В Skeleton для Windows выбирается `CodeWin64X86` либо `CodeWinARM64` по compile-time условиям; для macOS в ресурсе присутствуют `CodeMacIntel64` и `CodeMacARM64`. Все эти записи указывают на `EffectMain`. В Easy Cheese аналогичные поля указывают на `EntryPointFunc`.

Источники: `SkeletonPiPL.r:22–31`; `Examples/AEGP/Easy_Cheese/Easy_Cheese_PiPL.r:25–34`.

Отсюда следует проверка согласованности, а не обещание универсального бинарника:

```text
архитектура реально запущенного host
        ↕
архитектура machine code внутри артефакта
        ↕
соответствующая запись ресурса
        ↕
экспортированный символ нужного имени и контракта
```

Например, две Mac-записи в `.r` не доказывают, что сборка содержит оба machine-code slice. В просмотренном Xcode-проекте есть `ONLY_ACTIVE_ARCH = YES`; анализировать нужно фактическую конфигурацию и произведённый файл, не только список свойств ресурса (`Mac/Skeleton.xcodeproj/project.pbxproj:200–225`). Это источник для проверки, не выполненная здесь universal-build проверка.

## 4. Экспорт функции и её строковое имя

`Examples/Util/entry.h:30–34` задаёт `DllExport` отдельно для Windows и macOS. В `Skeleton.h:94–106` dispatcher объявлен внутри `extern "C"` с `DllExport`. Поэтому при чтении одной `.cpp` нельзя заключать, что у `EffectMain` отсутствует экспорт: соответствующее объявление находится в header.

Строка с именем функции в PiPL должна соответствовать реально экспортированному символу. Это **два независимых свойства**: resource name не меняет C++ linkage, а `extern "C"` не добавляет потерянный ресурс.

Для AEGP образец использует SDK-тип прямо в объявлении:

```cpp
extern "C" DllExport AEGP_PluginInitFuncPrototype EntryPointFunc;
```

Основание: `Easy_Cheese.h:36–37`. Это короткое объявление, не законченный плагин. Подробности AEGP initializer и возвращаемого global refcon — в [следующей главе](../03-AEGP/01-HOOKS-SUITES.md).

## 5. Registration callback — не повторный GLOBAL_SETUP

`PluginDataEntryFunction2` принимает opaque plugin-data pointer, callback второй версии, SPBasicSuite и строки имени/версии host. Callback отдельно получает отображаемое имя, match name, категорию, имя dispatcher, Kind, API major/minor, reserved info и support URL. Вторая версия callback добавляет support URL; старая версия сохранена ниже в том же header.

Основание: `Examples/Headers/AE_PluginData.h:53–143`.

В Skeleton `PF_REGISTER_EFFECT_EXT2` передаёт сведения о Skeleton и строку `EffectMain` (`Skeleton.cpp:219–240`). Затем **другая функция**, EffectMain, диспетчеризует команды, включая GLOBAL_SETUP. Регистрация описания эффекта сама по себе не подтверждает создание его параметров, применение к слою или вызов рендера.

### Ловушка macro из entry.h

`PF_REGISTER_EFFECT_EXT2` — не обычная функция. Его раскрытие содержит присваивание переменной `result` и отдельный `if`; имя этой переменной зафиксировано в macro (`Examples/Util/entry.h:55–69`). Не переносите такой вызов в условное выражение, ternary или функцию без соответствующей переменной, исходя лишь из внешнего вида вызова.

Рекомендация для своего кода: сначала прочитать раскрытие, затем оставить вызов отдельной операцией в предсказуемом scope. Сборка against exact SDK должна проверять весь entry translation unit. Наличие похожего macro в другом SDK не подтверждает идентичность его тела.

## 6. Какие версии сравнивать

В рассматриваемой поставке одновременно существуют:

- номер поставки SDK: 25.6 build 61;
- Effect API major/minor: **13/29**;
- версия формата PiPL: **2/0** в Skeleton;
- версия самого эффекта, упакованная `PF_VERSION`;
- major/minor driver, передаваемые AEGP initializer;
- версии приобретаемых suites.

API-числа проверены по `AE_EffectVers.h:13–14` и `AE_Effect.h:194–198,307–311`; назначение `my_version` явно отделено от plugin specification в `AE_Effect.h:2827–2830`. У Skeleton собственные version fields расположены в `Skeleton.h:62–68`, а GlobalSetup использует их в `Skeleton.cpp:67–84`.

**Не ставьте число 25.6 вместо 13/29 и не используйте суффикс типа suite как её числовую версию.** Например, AEGP_RegisterSuite5 приобретается по macro, которое здесь равно 6; это разобрано в главе AEGP.

## 7. Outflags: согласование с двумя важными оговорками

Обычная практическая проверка — сопоставить статические capabilities в PiPL и заявления GlobalSetup. В Skeleton ресурс содержит `0x02000000`, а код заявляет `PF_OutFlag_DEEP_COLOR_AWARE`. Header задаёт этому флагу `1L << 25`; это одна и та же битовая величина.

Источники: `SkeletonPiPL.r:51–57`, `Skeleton.cpp:67–84`, `AE_Effect.h:966–969`.

Но формула «все флаги всегда должны быть одинаковы» слишком груба:

**PiPL-only override.** Комментарий `AE_Effect.h:767–770` прямо говорит: при `PF_OutFlag_PiPL_OVERRIDES_OUTDATA_OUTFLAGS`, задаваемом только в PiPL, `out_flags` на GLOBAL_SETUP игнорируется и не обязан совпадать. Это описание конкретного поля и флага; не переносите его автоматически на любые outflags2 или любой selector.

**Dynamic flags.** `PF_OutFlag2_SUPPORTS_QUERY_DYNAMIC_FLAGS` связан с отдельной командой и допускает динамическую информацию для определённых контрактом свойств (`AE_Effect.h:815–820`). Это не возможность переписывать весь PiPL во время рендера. Реализованные SmartFX, float и MFR пути всё равно должны соответствовать заявленным возможностям.

### Сохранённые расхождения Skeleton

Рядом с `0x02000000` в ресурсе написан десятичный комментарий `50332160`; сам литерал равен **33554432**. За capability принимается литерал и соответствующее объявление, не противоречащий ему комментарий.

Есть и другое расхождение: PiPL reserved info равен 0, но registration macro получает `AE_RESERVED_INFO`, определённый в entry.h как 8. **Семантика и приоритет этой разницы здесь не установлены.** Исходники не «исправлены» ради совпадения. Похожесть двух полей не позволяет объявить каждое различие ошибкой host или заменить значения наугад.

## 8. Как `.r` становится частью артефакта

Практическое продолжение exact Skeleton resource chain:
[macOS Xcode/resources/slices/exports](../08-MACOS/09-PRODUCTION-BUILD-PIPELINE.md) и
[Windows preprocessing/PiPLTool/rc/res/link](../09-WINDOWS/09-PRODUCTION-BUILD-PIPELINE.md).
Это commands и expected result types, не recorded build/load PASS.

### Windows: сохраняем весь resource pipeline

В `Examples/Template/Skeleton/Win/Skeleton.vcxproj:317–345` задана цепочка:

```text
SkeletonPiPL.r
  → C/C++ preprocessing: .rr
  → SDK PiPLTool: .rrc
  → preprocessing: SkeletonPiPL.rc
  → ResourceCompile
  → ресурс в собираемом модуле
```

В XML есть отдельные команды для Debug/Release и x64/ARM64. Отдельно подключены `.cpp` утилиты SuiteHandler и MissingSuiteError (`:371–374`). Только добавление Skeleton.cpp в пустой проект не воспроизводит эту сборку.

В поставке исходного `SkeletonPiPL.rc` нет: он является результатом custom build step. Это не причина подставлять `.rc` от другого эффекта. Проверять следует цепочку генерации, используемые include paths, architecture defines и фактический ресурс. В этой итерации XML прочитан и структурно проверен, но PiPLTool и Windows compiler не запускались.

### macOS: resource phase и bundle metadata

Xcode-проект включает SkeletonPiPL.r в Resources и включает SuiteHandler/MissingSuiteError в Sources (`Mac/Skeleton.xcodeproj/project.pbxproj:126–145`). Он задаёт `.plugin` wrapper, Info.plist и bundle identifier (`:200–225`). Сам Info.plist отдельно называет `CFBundleExecutable`.

Следовательно, переименование образца требует согласовать не только заголовок эффекта, но и ресурс, экспорт, имя executable и настройки bundle. Это редакционная схема проверки; signing, linking и загрузка конкретного bundle остаются отдельными тестами.

## 9. Место сборки, место установки и загруженный модуль

`INSTALL_PATH = "$(HOME)/Library/Bundles"` в Xcode-проекте описывает build/install setting проекта. Из него нельзя вывести, что After Effects сканирует эту директорию. Аналогично красивый путь к `.plugin` не подтверждает, что host выбрал его вместо другой копии.

Прежняя короткая редакция главы приводила общие MediaCore-пути, включая per-user путь, без проверки конкретного discovery contract. **Присланный SDK здесь не подтверждает полный список путей и их приоритет.** При упаковке используйте проверенные платформенные инструкции и отдельно фиксируйте реальную загрузку; положения этой главы не являются проверкой установленной машины пользователя.

Для разбирательства полезна такая цепочка доказательств:

```text
source revision → build configuration → produced artifact + hash
→ установленный payload → путь реально загруженного модуля
→ runtime Build ID → выполненный сценарий
```

Это рекомендуемая методика Библии. Только последняя часть показывает работу инструмента; совпадение хеша исходного файла не закрывает её.

## 10. Диагностика по месту отказа

| Наблюдение | Что проверять дальше | Чего пока нельзя утверждать |
|---|---|---|
| Компилятор принял `.cpp` | Resource generation, link inputs, symbol exports | Плагин собран и загружается |
| Модуль создан, AE его не показывает | Фактические архитектуры, PiPL Kind/entry, размещение, зависимости и диагностику host | Это обязательно ошибка алгоритма |
| Эффект виден в списке | GLOBAL_SETUP, параметры и применение к слою | Рендер выполнялся |
| AEGP загрузился, но пункта меню нет | Результаты GetUniqueCommand/InsertMenuCommand и последующих registrations | AEGP обязан отображаться как Effect |
| Пункт есть, но серый | Логику UpdateMenuHook и условия доступности | Загрузчик сломан |
| Изменённый бинарник не меняет поведение | Загруженный путь/Build ID, дубли, состояние процесса | Host гарантированно перечитал файл |

Это диагностические развилки, не автоматический диагноз. Не удаляйте пользовательские настройки и сторонние плагины ради «чистоты» без согласования. Не меняйте ABI-cast до совпадения с compiler только для подавления ошибки.

## 11. Что требуется от рабочего примера

До статуса «проверен в AE» должны быть получены отдельные результаты: чистая сборка, проверка ресурса и экспортов, загрузка идентифицированного артефакта, основной сценарий и корректное завершение. Для AEGP дополнительно проверяются отсутствие дублей меню и частичная инициализация; для Effect — соответствие параметров и рендера заявленным capabilities.

Приватные эксперименты с поздней загрузкой из [проектных кейсов](../22-PROJECT-CASE-STUDIES/README.md) не заменяют эти требования. Registration callback, успешная поздняя загрузка нового модуля и безопасная замена уже загруженного кода — разные утверждения. Рассмотренные declarations не дают общего контракта hot reload.

Далее: [инициализация AEGP, hooks и suites](../03-AEGP/01-HOOKS-SUITES.md). Точные исходники этой главы перечислены в [записи сверки](../18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md); непроведённые host-проверки остаются открытыми.


## Private loader boundary

The [AE Hot Loader case study](../22-PROJECT-CASE-STUDIES/REUSE-AUDIT-2026-10-01.md) records a successful AE 25.6 ARM64 experiment using the internal `ML::LoadPlugins` path to late-load a new diagnostic effect bundle. That result is intentionally **not** converted into a supported loading recipe here.

Public PiPL/registration/loading guidance in this chapter remains based on the documented SDK/sample model. Private loader ABI, image-relative offsets and version-specific host internals belong to research case studies unless separately supported and revalidated for the exact AE build.
