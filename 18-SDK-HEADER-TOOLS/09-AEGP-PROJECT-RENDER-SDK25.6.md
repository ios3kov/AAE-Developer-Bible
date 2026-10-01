# SDK 25.6: проект, очередь рендера и получение кадров через AEGP

Дата: **2026-10-01**. Редакционная сверка по поставке `ae25.6_61.64bit.AfterEffectsSDK`.

**Результат — расширение главы Библии, не новый плагин и не запуск AE.** Основной текст: [AEGP project and render automation](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md). Условия завершения общего плана не меняются.

## Источники и метод

SHA-256 приложенного TAR повторно рассчитан: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`. Совпадает с ранее принятой поставкой. Для чтения извлечены обычные файлы; абсолютные пути, переходы вверх, ссылки и AppleDouble-записи не использованы. Приложенные `zstd` и `extractzstd.sh` не исполнялись. Этот шаг не удостоверяет подпись Adobe и не является повторной компиляцией SDK.

Прочитаны относящиеся к главе диапазоны шести файлов ниже. Разбор ограничен указанными declarations и фрагментами samples; вся поставка целиком не объявляется проверенной. В главе сокращение **H** означает `Examples/Headers/AE_GeneralPlug.h`, **Old** — `Examples/Headers/AE_GeneralPlugOld.h`.

| Предмет | Источник | Что поддерживает источник |
|---|---|---|
| Проект и опасные операции | H:285–345 | Получение проектов, dirty flag, Unicode-путь; NewProject и OpenProjectFromPath предупреждают о закрытии уже открытых проектов. Комментарий про один проект относится к AE 5.0. |
| Обход и имена объектов | H:433–545 | First/Next, NULL после последнего item, active item, тип, ID, parent folder; имя и путь возвращаются через отдельные memory handles. DeleteItem удаляет объект из композиций, а не освобождает ссылку. |
| Comp и Layer | H:649–660,1005–1043,1162–1214 | Преобразование item/comp, связь layer/source/parent, отдельный layer ID и поиск по ID внутри parent comp. Не установлен универсальный срок жизни ID после закрытия/импорта проекта. |
| Время | `Examples/Headers/A.h:88–91`; H:496–503,1162–1170,5131–5164 | A_Time содержит value/scale; разные временные пространства, current item time не обновляется во время рендера; render time и time step — разные настройки. |
| Undo и обработка ошибок | H:2943–2958 | Парные quiet-errors и undo API. EndUndoGroup не описан как откат уже выполненных операций. |
| Скрипты и потоки | H:3008–3022,3037–3049 | Специальное non-main разрешение для CauseIdle, отдельный запрет получать его указатель через suite на worker; UI suppression; проверка scripting availability и текстовые result/error. |
| Очередь и элемент | H:3199–3239,3309–3385; Old:170–245 | Разные состояния очереди и элемента, требование STOPPED для SetRenderState; invalidation всех RQItemRefH при изменении состава/порядка. Suite3 тоже принимает enum статуса, не Boolean. |
| Output module | H:3388–3502 | Отдельная invalidation output-module refs; path, channels, crop, stretch, post-render action и сведения о формате. Расширение имени файла не заменяет настройку формата. |
| World и options | H:5026–5240 | Тип/размер/stride и typed base-address API; read-only ограничения checked-out frames; NewFromItem создаёт options с временем 0; ROI из нулей означает всю область. |
| Layer options | H:5243–5327 | Отдельные layer options и их Dispose; upstream/downstream выбирают разную границу эффектов; NewFromDownstreamOfEffect имеет явное UI-thread ограничение. |
| Получение кадров | H:5330–5400 | RenderSuite5 version macro равен 8; sync/async, отмена, receipt, read-only borrowed world, обязательный CheckinFrame. Async completion имеет исключение при shutdown. |
| Кэш | H:5413–5443 | Render timestamp, video-change check, проверка полезности speculative render и adopted platform world. CheckinRenderedFrame не равен CheckinFrame. |
| QueueBert | `Examples/AEGP/Queuebert/QueueBert.cpp:110–165` | Старые нулевые/числовые refs, демонстрационные изменения очереди, фиксированный путь и TRUE в SetRenderState. Это не безопасная готовая команда для рабочего проекта. |
| Projector | `Examples/AEGP/Projector/Projector.cpp:670–703` | Добавление шести элементов; старт очереди находится в закомментированном блоке, не в исполняемой части рассматриваемого фрагмента. |

## Current suite generations relevant to this chapter

Current SDK 25.6 header exposes:

- `AEGP_RQItemSuite4` for render-queue items;
- `AEGP_RenderSuite5` for frame rendering.

Existing Bible recipes use older compatible `RQItemSuite3` / `RenderSuite4` subsets. They are source-example dependencies, not the current-generation baseline, and suite tables must never be cast between generations.

## Важная находка в существующем рецепте Bible

Проверены исходники `17-NATIVE-SUITE-COOKBOOK/code/` с содержимым, доступным после коммита `4cd4515e605783f9255edb59cf734d0cabe0f1fd`:

| Файл | Git blob | Вывод source review |
|---|---|---|
| `ProjectItemRecipes.cpp` | `160bf6b5101a7c042910dc37ec04c39da2d866f5` | Получает проект/корень и считает items. Нет общего exception guard; счётчик может быть частичным при ошибке. |
| `RenderQueueRecipes.cpp` | `21fd555c42c5a8f2308da712ba84d05edb64008a` | После добавления заново получает refs, но последний вызов передаёт TRUE как статус. Нет полного preflight, readback и rollback. |
| `RenderRecipes.cpp` | `ea9a572d1c9869c4f82b76bb05581206b708800b` | Получает receipt, вызывает consumer, делает checkin. Borrowed options не создаёт и не освобождает; cancellation callback не передаёт. |

**`AEGP_SetRenderState(rq_itemH, TRUE)` не означает QUEUED.** В рассматриваемом SDK `AEGP_RenderItemStatus_UNQUEUED=1`, `QUEUED=2` (H:3210–3225); `SPTypes.h:60–61` определяет TRUE как 1, если он ещё не определён. Old:206–208 подтверждает enum-аргумент и для используемой рецептом RQItemSuite3. При обычном TRUE=1 рецепт просит UNQUEUED. Это обнаруженная ошибка выбора аргумента, а не новый результат выполнения AE.

Такая же запись есть в QueueBert:131. Наличие её в sample не меняет объявленный контракт. Главой показан именованный QUEUED и обязательный readback. **Первоначальный source-review зафиксировал ошибку до исправления.** Позднее cookbook-рецепт был изменён: теперь он передаёт `AEGP_RenderItemStatus_QUEUED` и делает readback через `AEGP_GetRenderState`. Историческое наблюдение сохраняется как evidence того, почему Boolean здесь недопустим. Исправление source-level аргумента не является host verification очереди.

`RenderRecipes.cpp` использует RenderSuite4, тогда как новые объяснения отдельно ссылаются на RenderSuite5 в основной части header. Версии не кастуются друг в друга. Нормальный путь рецепта возвращает checkin error, если не было основной ошибки; аварийный RAII cleanup имеет ограничения уже разобранного owner. Это не проверка отмены, shutdown или асинхронного получения кадров.

## Идентичность файлов SDK

SHA-256 по исходным байтам без нормализации переводов строк:

| Файл | SHA-256 |
|---|---|
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` |
| `Examples/Headers/AE_GeneralPlugOld.h` | `1668a133fa264984e747812538be997677be563ed67bda5f345cb0fb961213e4` |
| `Examples/Headers/A.h` | `96e4363bab5a28a230e8c68201ff4a7031e816f8c07f0a1b705cbb8b69db7a96` |
| `Examples/Headers/SP/SPTypes.h` | `92ff4f7277fb8c52232cd7bc6b4e21774e8deb190afe1fefdf588e522de58157` |
| `Examples/AEGP/Queuebert/QueueBert.cpp` | `93ce342d8fa7855f85eca140ae5e3564fc3f870fda4340c96cc90736e3f30fca` |
| `Examples/AEGP/Projector/Projector.cpp` | `f7db7a6a1cb0e3d1cac7e6ae4e5478601c009d0e6ef9782dc52f7ad6c24ef127` |

## Статус проверки

Проверены TAR identity, hashes перечисленных файлов, указанные declarations и относящиеся к теме фрагменты samples/рецептов. Уровень: **SDK source review / DOCUMENTED**, а замечания к нашему коду — source-review findings. Архитектурные схемы главы обозначены как рекомендации, не дополнительные гарантии Adobe.

Новые C++ примеры не компилировались и не запускались; mutation/undo, Unicode paths, cancellation, queue exports, async shutdown и контроль пикселей внутри AE — **NOT RUN**. SDK и полные исходники Adobe не публикуются. Изменяются документы и навигация, не рабочий AEP, настройки AE или импортер.

Проверку Markdown, генерации MASTER/MANIFEST и существующих portable tests выполняет штатный GitHub Validate на конкретном коммите. Его результат фиксируется отдельно от заявлений о runtime. Следующая редакционная тема — streams и ключевые кадры, не новый измерительный инструмент.
