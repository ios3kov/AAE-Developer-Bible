# PICA suites — versioned native service bus

Обновлено **2026-10-01** по присланному **After Effects SDK 25.6 build 61**. Эта глава описывает контракт suite-provider/consumer, а не обещает hot-reload или безопасную выгрузку произвольного модуля.

Подробная привязка к исходникам: [SDK 25.6 — PICA, Effect↔AEGP и legacy boundaries](../18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).

## 1. Что такое PICA в практическом смысле

`SPBasicSuite` даёт потребителю две базовые операции:

```text
AcquireSuite(name, public_version)
    -> suite pointer + increment reference count

ReleaseSuite(name, public_version)
    -> decrement reference count
```

В заголовке 25.6 прямо указано, что acquire увеличивает reference count, а release уменьшает его и допускает выгрузку suite при достижении нуля. Это **lifetime/refcount contract**, но не гарантия thread safety функции внутри suite.

У `SPSuitesSuite` есть низкоуровневые операции над конкретным suite list. В отличие от `SPBasicSuite`, они дополнительно различают **public API version** и **internal version**. Поэтому номер структуры, публичная версия API и внутренняя версия registry — разные понятия.

Источник: `Headers/SP/SPBasic.h:80–101`, `Headers/SP/SPSuites.h:116–178`.

## 2. Provider: как suite публикуется

Adobe sample **Sweetie** создаёт статическую таблицу `DuckSuite1`, получает `SPSuitesSuite` через `SPBasicSuite` и добавляет таблицу в `kSPRuntimeSuiteList` через `AddSuite`.

Схема:

```text
AE loads provider AEGP
    ↓
provider obtains SPSuitesSuite
    ↓
AddSuite(runtime-list, name, api-version, internal-version, function-table)
    ↓
other plug-ins can AcquireSuite(name, version)
```

В sample function table имеет static storage duration. Это хороший ориентир для lifetime: consumer не должен получить указатель на таблицу, которая исчезнет сразу после initializer.

**Но Sweetie не демонстрирует:**

- runtime replacement уже опубликованной версии;
- общий unregister/hot-unpublish workflow;
- безопасную выгрузку provider при живых consumers;
- migration consumers между двумя одновременно опубликованными несовместимыми ABI.

Поэтому опубликованный suite — хороший способ связи модулей, но не доказательство общего механизма hot replacement.

Источник: `AEGP/Sweetie/Sweetie.cpp:23–78`, `Util/DuckSuite.h:1–13`.

## 3. Consumer: acquire, use, release

Effect sample **Checkout** получает DuckSuite через `AEFX_SuiteScoper`, вызывает функцию и автоматически освобождает acquisition при выходе из scope. Отсутствие Sweetie sample там считается необязательной возможностью: exception перехватывается, effect продолжает загрузку.

Это полезный pattern для optional service:

```text
try acquire exact suite name/version
    available -> use feature
    unavailable -> disable only dependent feature
release acquisition on every exit path
```

`AEFX_SuiteHelperT` в поставке 25.6 показывает acquire в constructor и release в destructor. Сам release-result в destructor отбрасывается; если конкретному продукту нужно фиксировать ошибку release, нужен явный close/result path, а не надежда на destructor.

Источник: `Effect/Checkout/Checkout.cpp:45–68`, `Util/AEFX_SuiteHelper.h:73–116`.

## 4. Имя и версия — ABI identity

Suite нужно идентифицировать минимум парой:

```text
stable suite name
+ public API version
```

Новая несовместимая структура не должна молча публиковаться под старой версией.

Для собственного suite полезно считать version bump обязательным, если меняется:

- порядок function pointers;
- сигнатура function pointer;
- размер/смысл структуры, которую consumer обязан передавать;
- ownership или lifetime contract;
- обязательная семантика результата.

Добавление функции «в конец структуры» всё равно нельзя считать автоматически совместимым без согласованного ABI/versioning правила между provider и consumers.

## 5. C ABI, а не C++ object graph

Публичный function table должен быть максимально простым:

```cpp
typedef struct CoreSuite1 {
    int32_t (*Process)(const void* input, uint64_t input_size);
} CoreSuite1;
```

Практические правила:

- fixed-width integer types;
- plain structs/function pointers;
- документированный calling convention (`SPAPI` там, где он требуется контрактом);
- никаких exceptions через границу;
- никаких `std::string`, STL containers, references и C++ ownership objects как wire ABI;
- явно записанное владение каждым buffer/handle;
- входные size/version проверяются до чтения расширенной структуры.

Текущий Bible `SharedSuite.h` — **C++-oriented ABI template**, потому что использует `std::int32_t/std::uint64_t`. Его нельзя называть C-source-compatible header без дополнительной адаптации. Это документационное ограничение, а не новый host defect.

## 6. Buffer ownership должен быть частью API

Для каждой функции suite заранее ответьте:

| Вопрос | Должен быть определён |
|---|---|
| Кто выделяет output buffer? | caller / provider / host |
| Кто освобождает? | точная функция/API |
| Можно ли вернуть borrowed pointer? | только с явным lifetime |
| Что означает required size > capacity? | код ошибки + required size |
| Разрешено ли input==output? | да/нет |
| Можно ли хранить callback/refcon после return? | только если контракт это разрешает |

«Оба модуля находятся в одном процессе» не отменяет ownership.

## 7. Threading — отдельный контракт

Reference count suite не делает service thread-safe.

Если функция может вызываться из render path, provider должен отдельно определить:

- какие вызовы разрешены одновременно;
- какое состояние immutable;
- где находится per-instance/per-render state;
- допустимы ли host callbacks внутри service;
- можно ли блокировать;
- кто отвечает за cancellation.

Без такого договора consumer не должен вызывать project/UI mutation из worker/render thread только потому, что suite pointer доступен.

## 8. Provider lifetime и load order

Sample Checkout специально показывает ситуацию «suite отсутствует». Из этого следует практическое правило: **не проектировать optional consumer так, будто provider гарантированно уже загружен**.

Для обязательной зависимости нужен fail-closed startup с понятной диагностикой. Для необязательной — feature negotiation.

Не храните полученный function-table pointer после `ReleaseSuite`. Не превращайте адрес функции или таблицы в постоянный ID provider.

## 9. Когда PICA подходит лучше generic call

Published suite лучше, когда нужен повторяемый сервис:

- много операций;
- несколько consumers;
- стабильный versioned ABI;
- явные функции и ownership;
- общий native core.

Для единичной команды конкретному экземпляру effect может быть уместнее [AEGP → Effect generic call](../15-COMMUNICATION/03-AEGP-TO-EFFECT.md).

## 10. Что проверять в собственном provider/consumer

Минимальная матрица:

1. provider отсутствует;
2. нужная version отсутствует;
3. supported version присутствует;
4. два consumers одновременно acquire/release;
5. consumer ошибается после acquire — release всё равно происходит;
6. provider возвращает ошибку функции;
7. неправильный input size/version;
8. повторный запуск AE;
9. заявленный concurrency mode;
10. shutdown при живых/освобождённых acquisitions.

Пока эта матрица не выполнена в AE, source review остаётся source review.

## Связанные материалы

- [Plug-in → Plug-in через PICA](../15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md)
- [Effect ↔ AEGP generic bridge](../15-COMMUNICATION/03-AEGP-TO-EFFECT.md)
- [PICA shared-suite template](../16-WORKING-TEMPLATES/pica-shared-suite/README.md)
- [Memory/lifetime](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md)
- [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md)
