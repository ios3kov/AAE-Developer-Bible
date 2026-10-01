# SDK 25.6: память, lifetime и MFR — третья сверка глав

Дата: **2026-10-01**. Результат: содержательно переработаны главы [памяти и ошибок](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md) и [MFR](../02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md).

**Уровень: SDK source review и редакционная работа.** Это не новый native-плагин, не считыватель каналов, не проверка утечек в AE и не измерение ускорения. Согласованный объём Библии не изменён; полные этапы плана не закрываются фактом написания этих глав.

## Основа и способ проверки

Использована прежняя пользовательская поставка `ae25.6_61.64bit.AfterEffectsSDK`. Повторно вычисленный SHA-256 приложенного TAR: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`; размер **7 182 336 байт**. Совпадает с [первой записью поставки](05-SUPPLIED-SDK-25.6.md).

Обычные файлы извлечены в отдельный рабочий каталог с проверкой путей; служебные AppleDouble-записи не использовались как исходники. Приложенные executable `zstd` и `extractzstd.sh` не запускались. Исходный TAR не изменён. Повторная проверка подписи или происхождения Adobe не заявляется.

Сверены конкретные declarations, комментарии и показанные ниже участки образцов. Исторические оговорки источников не исправлялись молча: расхождения перечислены отдельно. Рекомендации по собственным snapshots, сериализации и тестам помечены в главах как рекомендации Библии, а не как дополнительно обнаруженные гарантии host.

## Что дописано

| Глава | Новое содержание |
|---|---|
| Память, threading, errors | Семьи ресурсов и парные операции; borrowed/owned/transferred; lock-state sequence handles; разные flatten selectors; SmartFX и auxiliary cleanup; ошибки освобождения; ограничения имеющихся RAII helpers |
| MFR | Точный действующий флаг и unused legacy-флаги; пересечение selectors; read-only sequence suite; mutable render copies; Compute Cache callbacks, ключи, receipts и режимы ожидания; критерии будущей проверки без заявления о новом запуске |

Глава MFR больше не формулирует blanket-запрет всех global-записей как цитату из SDK. Неизменяемое общее состояние и запрет удержания собственного blocking lock через host call представлены как архитектурные рекомендации; конкретные threading-ограничения привязаны к источнику.

## Основные проверенные контракты

- `AE_EffectCBSuites.h:52–78`: **`kPFHandleSuiteVersion1=2`**, несмотря на имя структуры `PF_HandleSuite1`; `host_resize_handle` допускает изменение handle.
- `SP/SPBasic.h:82–101`: acquisition повышает счётчик ссылок suite, release по имени/версии снижает его. Таблица функций не является принадлежащим клиенту heap-объектом.
- `AE_GeneralPlug.h:881–909`: отдельная AEGP memory family; lock nestable; предусмотрены reporting/stats.
- `AE_Effect.h:2839–2903`: автоматический lock-state для переданных state handles, исключение новой allocation в sequence setup, flatten/resetup и неперсистентный frame_data.
- `AE_Effect.h:1104–1138`: исторический flatten заменяет рабочие данные; get-flattened возвращает независимый handle с передачей владения host.
- `PathMaster.cpp:167–181,186–220,233–267`: наглядная разница setdown/flatten/get-flattened; комментарий о межплатформенном ограничении при resetup в `:300–303` сохранён.
- `AE_Effect.h:2501–2523,2576–2583`: отдельный deleter для pre-render data; early SmartFX pixel checkin не обязателен. Это не контракт auxiliary chunk.
- `AE_ChannelSuites.h:82–87,545–558`: auxiliary checkin обязателен. `SmartyPants.cpp:399–403,965–989` отделяет pre-render parameter-checkin оговорку образца от явного checkin в smart render.
- `AE_Macros.h:41–46`: `ERR` пропускает выражение после первой ошибки; `ERR2` выполняет выражение и сохраняет первичную ошибку. Оба макроса не подменяют учёт факта acquisition.
- `AE_Effect.h:497–509,2682–2687`: пользовательская отмена и ошибки различаются; ненулевой результат abort нужно вернуть host.
- `AE_Effect.h:912–935,984–1010`: текущий threaded-rendering флаг, условия flattening, read-only sequence data и репликация mutable render state.
- `AE_GeneralPlug.h:5707–5718`: точное расположение `PF_EffectSequenceDataSuite1`, `PF_GetConstSequenceData` и const-handle typedef. В этой таблице нет отдельного checkin; декларация не задаёт универсальный срок хранения адреса между командами.
- `AE_EffectCB.h:687–694`: `PF_ITERATE` может выполняться на нескольких потоках; `refcon` должен быть read-only или синхронизирован.
- `AE_ComputeCacheSuite.h:34–78,82–167`: cache class, callbacks, полный ключ, размер, удаление, receipt/checkin, режимы ожидания и cached-only lookup.
- `AE_Effect.h:899–910`: отдельная задача GUID-зависимостей финального кадра Smart effect. Compute Cache key и frame GUID не объявляются взаимозаменяемыми.

## Оговорки и различия текста SDK

1. Общая MFR-формулировка `AE_Effect.h:916–918` перечисляет sequence setup среди потенциально пересекающихся команд. Описания selectors `:1084–1092,1115–1125` дают более узкие условия UI-only setup и отдельно разрешают resetup на UI/render thread. Обе формулировки сохранены с условиями, без придуманной универсальной последовательности вызовов.
2. В схеме multi-checkout `AE_ComputeCacheSuite.h:112–125` переменные кодов названы `bool`, но реальные декларации `:142–158` возвращают `A_Err`. Схема не выдается за готовый компилируемый пример; собственная реализация должна сохранять полный код ошибки.
3. `wait_for_other_threadB=false` не запрещает вычисление отсутствующего значения: это явно видно из таблицы `:127–139`. Для lookup без compute/ожидания описан отдельный `AEGP_CheckoutCached` (`:148–158`).
4. Host-lock sequence data не объявлен mutex. Предупреждение о преждевременном unlock при re-entry и специальный threaded-render способ чтения рассматриваются раздельно.
5. Уведомление `NOT X-PLATFORM SAFE` в PathMaster не заменено заявлением о переносимом формате. Установка самим образцом MFR-флага не засчитывается как наш тест конкурентного выполнения.

Никакой из этих пунктов не объявлен новым воспроизведённым багом After Effects.

## Идентичность использованных SDK-файлов

Все пути относительно корня поставки. SHA-256 рассчитан по исходным байтам, без нормализации переводов строк.

| Файл | SHA-256 |
|---|---|
| `Examples/Headers/AE_Effect.h` | `5432df9bb447cefce2f96c1477d6beccd4686b7236d460c803beab76dae1d537` |
| `Examples/Headers/AE_EffectCB.h` | `33524c0b8cbbf7b0a3b442dce45149d231e1b9c69ca7ab1d219ce4f79d324180` |
| `Examples/Headers/AE_EffectCBSuites.h` | `9d6ea76a6cf44d6103b65aa01229fc72979404b94694661437089fff0bf3c271` |
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` |
| `Examples/Headers/AE_ComputeCacheSuite.h` | `40e2bc8df1a4e994c7c36724d746e44e1894f254f6fac46e3b500ff9655893cc` |
| `Examples/Headers/AE_Macros.h` | `d51b007444cec1fd404fd076f88e3e1290349159b8d0152e3dba3a2d1f773c46` |
| `Examples/Headers/SP/SPBasic.h` | `a1258cfd57eedbe5ecbfcebf2bc7df8a3826f495f8e3cc549dce55e60e73395b` |
| `Examples/Headers/AE_ChannelSuites.h` | `45ce3f0a1143ca05e85d455843eba017e9de5330d13348ea2997bc95eb905088` |
| `Examples/Effect/PathMaster/PathMaster.cpp` | `2c66e9a88934b8c38fc2914f7a5d14d408c93331911f83f1e4edc2737cc94496` |
| `Examples/Effect/SmartyPants/SmartyPants.cpp` | `4865f3d8db8de37f5109cb34fdf04b7ae8f5b5582f12f490baa67f7f179104c2` |

Это десять исходных файлов, а не десять выполненных runtime-тестов. Сами headers, полные образцы Adobe и архив SDK в Git не опубликованы.

## Сверка с существующими helpers Библии

Прочитан исходный snapshot `fcfb0e32c14916b55c2bcdbe414d3d1b3f524eeb`:

| Файл в `19-NATIVE-CODE-FOUNDATION/code/` | Git blob | Вывод review |
|---|---|---|
| `PicaSuiteRef.h` | `38b7246d6b3ee7e50ca75bbe30a1bd807714ef2c` | Suite освобождается, но basic pointer/имя заимствованы; release error не возвращается |
| `AegpOwners.h` | `e4d8b573cb5b87e50357bbbc376756b59eccd9c3` | Разные deleters, move-only ownership; suite lifetime и memory lock не управляются owner; cleanup errors отбрасываются |
| `HostCallbackGuard.h` | `6644a35a258db55ffb0ef7f3aee0eb4d4ec71ade` | Fallback задаёт caller; guard не управляет внешними ресурсами и не классифицирует все ошибки |

Это документирование существующей реализации и её ограничений. Код helpers в этой итерации не изменён; native-compilation и behavioral-тесты не считаются повторёнными лишь вследствие review. Аудит FSTR Line/AE Hot Loader из этапа 3A этим не подменён.

## Статусы этой редакционной итерации

| Проверка | Результат и граница |
|---|---|
| Повторный hash TAR и идентификация десяти SDK-файлов | Выполнены по исходным байтам |
| Сверка изложенных функций, правил владения и комментариев | Выполнена; SDK source review |
| Review трёх существующих ownership/callback helpers | Выполнен; код не изменён |
| Новая реализация/сборка native-примера | NOT RUN: не предмет этой редакционной итерации |
| AE load/render, memory stress, MFR, GPU | NOT RUN; gates плана открыты |
| Перенос helpers из FSTR Line/AE Hot Loader | NOT RUN; отдельный этап 3A |

Документацию проверяет существующий `Validate`, включая генерацию и `mkdocs build --strict`. Итог CI нужно читать для последнего commit итерации; сама эта запись не предсказывает успешность ещё не завершившегося workflow.

Следующая редакционная тема: **регистрация/PiPL и жизненный цикл AEGP**, с привязкой к supplied SDK и существующему MenuTool. Это source-review/documentation milestone; product build/host evidence остаётся отдельным и не является условием готовности Bible.
