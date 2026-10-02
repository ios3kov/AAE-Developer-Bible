# SDK 25.6: принятая поставка и первая сверка глав

Дата: **2026-09-30**. Основа — приложенный пользователем архив с каталогом `ae25.6_61.64bit.AfterEffectsSDK`.

**Результат: исходники SDK прочитаны, три главы доработаны с привязкой к файлам и строкам. Это не новая сборка native-плагина и не прогон After Effects.**

**Исторический контекст — уточнение 2026-10-02:** следующий блок и этап 3A ниже относятся к плану на дату этой записи. Portable reuse rerun позже выполнен: [ledger](../VERIFICATION.md#gate-3a-reuse-audit-verification-2026-10-01). Текущие редакционные обязанности задаёт [план](../COMPLETION-PLAN.md); прежние требования build/host Gates не действуют. Исходные хэши, диапазоны строк и результаты этого review сохранены.

## Место в согласованном плане

Эта запись — источниковая опора текущей редакции Bible. Она фиксирует exact SDK baseline и source-review findings. Старый completion-gate model superseded: compiler/host evidence остаётся отдельным evidence class и не определяет готовность документации.

По уточнению пользователя основной результат этой итерации — **главы Библии**, не новый вспомогательный продукт. Разработка native-считывателя auxiliary-каналов приостановлена; ранее написанные tools и отчёты не удалены. Следующий редакционный блок: параметры/UI и пиксельные форматы, затем согласование с разделами памяти и MFR. Новые эталонные реализации не обходят предварительный аудит этапа 3A.

## Проверка идентичности, без запуска приложенных программ

Приложенные имена не совпадают с фактическими контейнерами:

- `ae25.6_61.64bit.AfterEffectsSDK.tar.zstd.zip` содержит Zstandard-поток, не ZIP.
- `ae25.6_61.64bit.AfterEffectsSDK.tar.zstd` уже содержит TAR.

Zstandard-поток распакован библиотекой среды анализа. Полученные **7 182 336 байт побайтово совпали** с отдельно приложенным TAR. Размер сжатого потока — **1 540 471 байт**. Из TAR использованы обычные файлы/каталоги; AppleDouble-служебные записи не используются как исходники. Приложенные `zstd` и `extractzstd.sh` не исполнялись, атрибуты/настройки машины пользователя не менялись.

Это проверка целостности пары файлов, **не проверка подписи Adobe или происхождения загрузки**. Название 25.6 build 61 взято из поставки; номер effect-протокола проверен независимо в header.

SHA-256 Zstandard: `e02fa2b488c3cceb238866b648eb9a2526d308a260744367915a2f173663c36c`.

SHA-256 TAR: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`.

## Изменённые главы

| Глава | Содержательная доработка |
|---|---|
| [Устройство Effect-плагина](../02-EFFECT-PLUGINS/01-ANATOMY.md) | Реальная сигнатура, разделение регистрации/диспетчера, lifecycle, implicit input, IDs, запрет анимации и UI-only изменения |
| [SmartFX](../02-EFFECT-PLUGINS/03-SMARTFX.md) | Различия extra-структур, области и уникальные checkout IDs, pre-render data, четыре разных cleanup-контракта, ограничения SmartyPants |
| [Дополнительные каналы](../02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md) | Семантика/type/dimension, точные имена suite-функций, found/error, requested/returned type, stride и обязательный checkin |

В главах source-backed утверждения отделены от рекомендаций проектирования и пока непроверенного runtime-поведения. Учебное объявление функции не выдается за завершённый, собранный плагин. Сам SDK, его headers, бинарники и полные исходники образцов **не добавляются в публичный репозиторий**.

## Уточнения, непосредственно полученные из поставки

1. `Examples/Headers/AE_EffectVers.h:13–14`: протокол `PF_PLUG_IN_VERSION=13`, `PF_PLUG_IN_SUBVERS=29`. Не смешивать с версией приложения или `out_data->my_version`.
2. `AE_Effect.h:1213–1261`: численные enum-значения 13/14 соответствуют `USER_CHANGED_PARAM`/`UPDATE_PARAMS_UI`, 23/24 — `SMART_PRE_RENDER`/`SMART_RENDER`. Это позволяет подписать ранее захваченные номера; **не доказывает**, что конкретная ветка была выполнена в незатрейсированном рендере.
3. `AE_Effect.h:1446–1479`: подтверждены DPTH/DPAA, UBT1/UST2/FLT4. У `PF_DataType_RGB` в этой поставке буквально записано `'RBG '`: spelling не исправлялся догадкой.
4. `AE_ChannelSuites.h:521–561`: реальные названия полей `PF_GetLayerChannelIndexedRefAndDesc` и `PF_GetLayerChannelTypedRefAndDesc` отличаются от сокращённых перестановок слов во вводном комментарии. В коде приоритет у declarations.
5. `AE_ChannelSuites.h:67–87,545–558`: checkout запрашивает datatype, checkin auxiliary-chunk обязателен. Стрелка комментария у by-value `data_type` не подменяет описание запрашиваемого типа.
6. `AE_Effect.h:2576–2583`: SmartFX input pixels действуют до конца команды или раннего checkin; ранний `checkin_layer_pixels` отмечен как необязательный. Это **не** правило auxiliary API.
7. `SmartyPants.cpp:399–403,965–989`: отдельная оговорка автоматического checkin параметров в SMART_PRE_RENDER; в SMART_RENDER образец явно возвращает checkout-параметры.
8. `AE_Effect.h:2511–2514`: `max_result_rect` не должен зависеть от размера текущего запрошенного output.

Неизвестные callback-адреса в исследовании 3D Channel Extract не переименовывались по сходству. Подтверждение SDK-символа и установление адреса реально исполненного callback — разные действия.

## Исходники, использованные для сверки

Все пути — относительно корня поставки. SHA-256 рассчитан по исходным байтам, без нормализации переводов строк. В главах приведены более узкие диапазоны строк.

| Файл | SHA-256 |
|---|---|
| `Examples/Headers/AE_EffectVers.h` | `6e02783ee9a90fa0906c0bd2242c3752c71e563a8eec5123ae852247bf56d2b4` |
| `Examples/Headers/AE_Effect.h` | `5432df9bb447cefce2f96c1477d6beccd4686b7236d460c803beab76dae1d537` |
| `Examples/Headers/AE_ChannelSuites.h` | `45ce3f0a1143ca05e85d455843eba017e9de5330d13348ea2997bc95eb905088` |
| `Examples/Headers/A.h` | `96e4363bab5a28a230e8c68201ff4a7031e816f8c07f0a1b705cbb8b69db7a96` |
| `Examples/Template/Skeleton/Skeleton.cpp` | `bb6d9c2ec85861486644111b61b2858e8fde757d948c6700c6e1d803917ecb0b` |
| `Examples/Template/Skeleton/Skeleton.h` | `5a6ee3530c741cf693bffda562a4af1662e47eead0dd37381258c690de33b2c5` |
| `Examples/Effect/SmartyPants/SmartyPants.cpp` | `4865f3d8db8de37f5109cb34fdf04b7ae8f5b5582f12f490baa67f7f179104c2` |

## Проверки и непроведённые проверки

| Проверка этой итерации | Статус и предел |
|---|---|
| Распаковка и побайтовое сравнение двух приложенных контейнеров | PASS: одинаковое TAR-содержимое |
| Идентификация перечисленных исходников | PASS: SHA-256 сохранены выше |
| Сверка названий, полей, указанных ограничений и учебного объявления | Выполнена по исходникам; уровень DOCUMENTED / SDK source review |
| Сборка и запуск новых native-примеров | NOT RUN: native-пример в этой итерации не создавался |
| Повтор исторической macOS syntax/type проверки | NOT RUN: предыдущая запись в VERIFICATION не является новым запуском |
| Windows compile, AE load/render, GPU/MFR, importer qualification | NOT RUN; соответствующие gates остаются открытыми |

Проверки документации выполняются существующим GitHub Validate после фиксации. Их итог относится к конкретному commit/Actions run, а не к Adobe host. Исторические 13 translation-unit проверок из [VERIFICATION](../VERIFICATION.md) сохранены как ранее записанный baseline; новая поставка не превращает их автоматически в повторённый результат.

Текст SDK содержит исторические комментарии и предупреждения. Они читаются в контексте настоящих declarations и конкретного примера; любые обнаруженные расхождения фиксируются, а не исправляются в исходнике молча. Этот обзор охватывает перечисленные главы, не весь SDK.


## SDK contract rerun — 2026-10-01

The same SDK bytes were supplied again and rechecked. The Zstandard stream decompresses byte-for-byte to the supplied TAR; TAR SHA-256: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`.

After extending the inventory parser to resolve callback typedef fields, the exact same SDK now yields:

- 140 headers;
- 233 tables;
- 3,560 function entries;
- 0 unparsed candidate tables;
- 4 retained non-required partial diagnostics.

The previous 230/3,537 counts were parser-coverage counts, not a different SDK snapshot.

The required-contract manifest passes all 35 required contract tables/functions, and the current cookbook passes 39/39 call-site suite-generation checks. See [the SDK 25.6 audit record](17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md).
