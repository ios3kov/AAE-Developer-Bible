# SDK 25.6: регистрация, PiPL и жизненный цикл AEGP

Дата: **2026-10-01**. Редакционная итерация по присланной поставке `ae25.6_61.64bit.AfterEffectsSDK`.

**Результат этой работы — главы Библии и проверяемая привязка к исходникам. Компиляция новых фрагментов, сборка ресурсов, загрузка AEGP и host-тесты не выполнялись.** Разработка auxiliary-считывателя остаётся приостановленной.

## Место в плане

Продолжается согласованное пользователем написание глав в предметной области [плана](../COMPLETION-PLAN.md). Это не закрывает этапы безопасности инструментов, аудита переиспользования, точной компиляции или проверки примеров в AE. Условия приёмки остаются в [COMPLETION-CHECKLIST](../COMPLETION-CHECKLIST.md).

Обновляемые разделы: [PiPL и загрузка](../01-ARCHITECTURE/03-PIPL-AND-LOADING.md), [AEGP hooks и suites](../03-AEGP/01-HOOKS-SUITES.md), маршрут чтения AEGP, STATUS и VERIFICATION. Существующий MenuTool рассматривается как исходник для объяснения, а не как новый проверенный эталон.

## Источник и метод

Повторно рассчитан SHA-256 приложенного TAR: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`. Он совпал с [ранее принятой поставкой](05-SUPPLIED-SDK-25.6.md). Для чтения извлечены обычные файлы; служебные AppleDouble-записи не использованы. Приложенные shell-скрипт и executable не запускались. Сравнение Zstandard/TAR из первой итерации здесь не выдаётся за новый запуск.

Изучены перечисленные ниже 19 файлов. Хеши рассчитаны по исходным байтам; строки в главах отсчитываются от начала соответствующего файла. Ни headers, ни целые Adobe samples, ни SDK-бинарники в публичный Git не добавляются.

Отдельно прочитан текущий Bible MenuTool: `16-WORKING-TEMPLATES/aegp-menu-command/MenuTool.cpp`, Git blob `2a9f4584e82bf7d58789fe3affdf38160a925d33`. Исходная точка этой редакции — `2b0dddfbb329024fbd5e8925d57ce425511840b0`; [зафиксированный исходник](https://github.com/ios3kov/AAE-Developer-Bible/blob/2b0dddfbb329024fbd5e8925d57ce425511840b0/16-WORKING-TEMPLATES/aegp-menu-command/MenuTool.cpp). Его код не изменялся.

## Что установлено по исходникам

| Предмет | Источник в `Examples/` | Граница вывода |
|---|---|---|
| Разные Effect и AEGP точки входа | `Headers/AE_PluginData.h:61–94`; `Headers/AE_GeneralPlug.h:4167–4176`; `Template/Skeleton/Skeleton.cpp:219–250` | Регистрация данных эффекта, его dispatcher и AEGP initializer — разные контракты. Не восстановлен полный внутренний алгоритм загрузчика AE. |
| Kind и архитектурные записи | `Resources/AE_General.r:28–37`; `Template/Skeleton/SkeletonPiPL.r:8–40`; `AEGP/Easy_Cheese/Easy_Cheese_PiPL.r:7–35` | В ресурсном описании `AEEffect='eFKT'`, `AEGP='AEgx'`; `AEGeneral='AEgp'` — отдельный литерал. Наличие записи архитектуры не доказывает наличие machine-code slice. |
| Экспорт и registration macro | `Util/entry.h:28–69`; `Template/Skeleton/Skeleton.h:94–106`; `Skeleton.cpp:219–240` | Видимость символа и C linkage проверяются отдельно от строкового имени. EXT2 — многооператорный macro с переменной `result`, не обычная функция. |
| Версии | `Headers/AE_EffectVers.h:13–14`; `Headers/AE_Effect.h:186–198,307–311,2827–2830`; `Skeleton.h:62–68`; `SkeletonPiPL.r:33–45` | API major/minor здесь 13/29; версия продукта, формат PiPL, driver version и версия suite не взаимозаменяемы. |
| Outflags | `Headers/AE_Effect.h:767–770,815–820,966–969`; `Skeleton.cpp:67–84`; `SkeletonPiPL.r:51–57` | У правила согласования есть документированное исключение `PiPL_OVERRIDES_OUTDATA_OUTFLAGS`. Динамические flags не разрешают произвольное изменение всех PiPL-битов. |
| Windows ресурсная цепочка | `Template/Skeleton/Win/Skeleton.vcxproj:317–345` | В XML четыре конфигурационных команды `.r → .rr → .rrc → .rc` и `ResourceCompile`. Команды не выполнялись; отсутствующий исходный `.rc` предусмотрен генерацией. |
| macOS resource/bundle | `Template/Skeleton/Mac/Skeleton.xcodeproj/project.pbxproj:126–145,200–225`; `Skeleton.plugin-Info.plist:5–16` | `.r` включён в resources; имя executable и bundle metadata отдельны. `INSTALL_PATH` проекта не является доказательством пути сканирования AE. |
| Hooks и refcon | `Headers/AE_GeneralPlug.h:2692–2737,2742–2800,4167–4176` | Global refcon, отдельный hook refcon, command status и idle interval имеют разные роли. About/Version hooks отмечены историческими оговорками. |
| Register suite version | `Headers/AE_GeneralPlug.h:2742–2745` | `kAEGPRegisterSuiteVersion5` равен **6**, не 5. Номер нельзя получать из суффикса типа. |
| Menu lifetime | `Headers/AE_GeneralPlug.h:2745–2832,2866–2900` | Удаление menu command и освобождение suite не являются отменой зарегистрированного callback. В просмотренном RegisterSuite5 нет общего unregister-hook API. Это не утверждение об отсутствии любых механизмов во всём AE. |
| Worker → idle | `Headers/AE_GeneralPlug.h:3008–3022` | CauseIdle асинхронен и имеет специальное разрешение non-main вызова; получение указателя через suite API под это разрешение не подпадает. UI suppression надо проверять отдельно. |
| SuiteHandler | `Util/AEGP_SuiteHandler.h:32–49,268–287,443–463`; `AEGP_SuiteHandler.cpp:33–65`; `MissingSuiteError.cpp:24–43` | Lazy acquisition может бросить исключение; destructor освобождает suites, не hooks. Возвращаемые ошибки release в этом helper не сохраняются. |
| Easy Cheese | `AEGP/Easy_Cheese/Easy_Cheese.cpp:47–89,332–348,419–455`; `Easy_Cheese.h:36–37` | Образец показывает регистрацию command/update/idle и использование SDK typedef. Он не доказывает готовый rollback или универсальную подписку на изменения проекта. |

## Расхождения и ограничения, которые нельзя скрывать

**Skeleton PiPL:** строка 52 содержит реальный литерал `0x02000000`, но рядом комментарий `50332160`. Значение литерала — `33554432`; оно соответствует `1 << 25` и DEEP_COLOR_AWARE в GlobalSetup. Ошибочный десятичный комментарий не становится дополнительной capability.

**Reserved Info:** `SkeletonPiPL.r:63–65` содержит 0, тогда как `Util/entry.h:38` определяет AE_RESERVED_INFO как 8, передаваемый registration macro. Разница сохранена как наблюдение. Значение и приоритет этих полей не выводятся по догадке; не предлагается менять одно из них только ради численного совпадения.

**Driver priority:** enum содержит BeforeAE/AfterAE, но комментарий к аргументу CommandHook говорит «currently always BeforeAE». Глава сохраняет обе части источника; поведение AfterAE в целевом host здесь не измерено.

**Установка:** прежний краткий текст главы приводил MediaCore-пути как общий ориентир. Эта поставка и build settings не устанавливают полный список реально сканируемых директорий и их приоритет. Поэтому новая глава отделяет сборочный INSTALL_PATH, размещение bundle и доказанную загрузку, а не приписывает SDK универсальное подтверждение per-user discovery.

**MenuTool:** регистрация death hook предшествует передаче владения ToolState, поздние ошибки оставляют отключённую команду и возвращают A_Err_NONE. Это сознательная стратегия сохранения refcon, не успешная полная инициализация. Ошибки DisableCommand/ReportInfo не сохраняются; ветка UI suppression отсутствует. Реакции на исключение после регистрации и завершение частичной инициализации требуют отдельных host-тестов. Ревью не превращает source-level ограничения в runtime claims; отдельный host-run нужен только если такой результат требуется утверждать.

## Идентичность просмотренных файлов

| Файл относительно корня SDK | SHA-256 |
|---|---|
| `Examples/Headers/AE_Effect.h` | `5432df9bb447cefce2f96c1477d6beccd4686b7236d460c803beab76dae1d537` |
| `Examples/Headers/AE_EffectVers.h` | `6e02783ee9a90fa0906c0bd2242c3752c71e563a8eec5123ae852247bf56d2b4` |
| `Examples/Headers/AE_PluginData.h` | `25be4a7620bc1c8fbcde7828304e9a207e9cabd0aaf3060f12c4e15c71ff52ca` |
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` |
| `Examples/Headers/SP/SPBasic.h` | `a1258cfd57eedbe5ecbfcebf2bc7df8a3826f495f8e3cc549dce55e60e73395b` |
| `Examples/Resources/AE_General.r` | `a21776f5087f4afb6a63d1c815696b44e3b68bc166546c3a9cf0a7d791eb60c5` |
| `Examples/Template/Skeleton/SkeletonPiPL.r` | `53c4598c9809b9bd979e599a13952ba27c5eb7e2649dc216fbee42e22d639f18` |
| `Examples/Template/Skeleton/Skeleton.h` | `5a6ee3530c741cf693bffda562a4af1662e47eead0dd37381258c690de33b2c5` |
| `Examples/Template/Skeleton/Skeleton.cpp` | `bb6d9c2ec85861486644111b61b2858e8fde757d948c6700c6e1d803917ecb0b` |
| `Examples/Template/Skeleton/Win/Skeleton.vcxproj` | `e722cc053c6e7d679435645282eae3d4d3cc3eb7722a2b250e63b9a1e3ca5a30` |
| `Examples/Template/Skeleton/Mac/Skeleton.xcodeproj/project.pbxproj` | `b74baecd67e56a240fd0be1bdb596255217b8b36b52dfd3a0b632be7f2344c6d` |
| `Examples/Template/Skeleton/Mac/Skeleton.plugin-Info.plist` | `013caa86320df6cef25e00ff44e81ad3cb2ab6f63c398136efb6358fea6ad507` |
| `Examples/AEGP/Easy_Cheese/Easy_Cheese_PiPL.r` | `caa60e4936de1ae16246672899c9781548f8b089e5541c3c9eec84653c70901d` |
| `Examples/AEGP/Easy_Cheese/Easy_Cheese.h` | `ffc98712a41962869fae12c473df3fff7cd86d0f7116b7f906e15e10cdd1ab72` |
| `Examples/AEGP/Easy_Cheese/Easy_Cheese.cpp` | `8f24fcd95201bfc8e7f8dbd66b984891d8720dc34c72f97b0c63dccc0bd33d18` |
| `Examples/Util/entry.h` | `2ae54d29d4bd28fc55585d7b36dd7bf93046352648bfdb9c10eca0f9905669d4` |
| `Examples/Util/AEGP_SuiteHandler.h` | `2eeec0827ca13f039eb87c961c8c41e77f046379457930d4bb2700c756b40b13` |
| `Examples/Util/AEGP_SuiteHandler.cpp` | `7c054c7b0778b1b26463d6bf31cd57ee1d971946e8da22fb174e9f088741606f` |
| `Examples/Util/MissingSuiteError.cpp` | `23cd851d73a8a6b8624f6aceeaad74fb2e28aa44fecdaf349c6aa9c3b3c58d2b` |

## Выполненное и невыполненное

TAR identity проверена повторно; перечисленные исходники прочитаны и хешированы. Стандартный XML parser прочитал Skeleton.vcxproj: найдены четыре конфигурационные команды PiPLTool и ResourceCompile для SkeletonPiPL.rc. Это структурная проверка проекта, не выполнение Windows build.

SDK source review отделён от авторских рекомендаций по lifecycle и диагностике. Новый native-код не создавался; существующий MenuTool не менялся. Windows/macOS build, PiPL binary inspection, загрузка AE, shutdown, ошибки частичной регистрации и отсутствие дублей меню — **NOT RUN в этой итерации**.

Документация и существующие portable regressions проверяются GitHub Validate после фиксации; их результат относится к конкретному commit/run. Они не исполняют приведённые SDK callbacks. Следующий редакционный блок — операции AEGP с проектом, слоями и потоками свойств; приёмка примеров остаётся отдельной работой.
