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

## 10. Provider state model

Separate:

~~~text
published function-table lifetime
≠ provider service-state lifetime
≠ consumer acquisition lifetime
≠ per-request/per-call state
~~~

The table address must remain valid for legitimate acquisitions.

Service state used by functions must also remain valid for any call the provider still accepts.

Do not publish a table that forwards into an object scheduled for destruction while consumers can still call it.

## 11. Suite-name lifetime

`SPBasicSuite::AcquireSuite/ReleaseSuite` use suite name + public version as identity.

If a RAII helper stores the `const char*` name so it can release later, that string must outlive the acquisition.

Safe patterns:

- compile-time/static suite-name literal;
- product-owned stable string storage whose lifetime exceeds the acquisition.

Unsafe pattern:

~~~text
temporary std::string.c_str()
→ acquire
→ temporary destroyed
→ RAII destructor later calls ReleaseSuite with dangling name pointer
~~~

The Bible `PicaSuiteRef` intentionally documents this requirement rather than copying the suite name internally.

## 12. Version negotiation

Do not implement negotiation as:

~~~text
Acquire latest arbitrary integer
→ cast whatever returned
~~~

Define supported public versions explicitly.

Example:

~~~text
try v2
→ if unavailable and product supports fallback: try v1
→ adapt through version-specific wrapper
→ never cast v1 table to v2 struct
~~~

A consumer supporting multiple versions should normalize them behind an internal product interface.

## 13. Provider shutdown

Do not infer a generic hot-unpublish protocol from PICA reference counting.

Conservative provider shutdown model:

~~~text
stop accepting new product work
→ prevent product-owned async callbacks from entering service
→ ensure product consumers release their acquisitions
→ destroy service state only after no valid product call can reach it
→ unload provider/module according to actual host lifecycle
~~~

If the host/provider architecture does not expose a safe unload/unpublish mechanism, design for process/host lifetime rather than inventing hot replacement.

## 14. Optional dependency discovery

For optional service, acquire-on-use is often safer than assuming startup order.

Possible policy:

~~~text
feature invoked
→ try AcquireSuite
→ unavailable: feature unavailable message
→ available: use within bounded owner
→ ReleaseSuite
~~~

If acquisition is expensive/frequent, cache a balanced acquisition only when its lifetime and shutdown ordering are explicit.

## 15. Provider API evolution

A new public version should be considered when changing:

- table layout/order;
- function signature/calling convention;
- input/output struct layout;
- ownership rules;
- thread rules;
- error semantics that callers must interpret;
- required behavior.

Do not use an internal version field as substitute for public ABI version.

For compatible additive evolution, define compatibility in writing; do not assume “added at end” is automatically safe for every compiler/consumer.

## 16. Error model

Separate:

1. **acquisition error** — provider/version unavailable;
2. **service transport/ABI error** — malformed size/version/null pointer;
3. **domain result** — request valid but operation cannot be performed;
4. **cleanup/release error** — acquisition owner could not cleanly release.

Do not collapse all four into one generic `-1` if callers need recovery/diagnostics.

## 17. Product validation guidance

### Actual shared header versus service implementation — 2026-10-07

[`SharedSuite.h`](../16-WORKING-TEMPLATES/pica-shared-suite/SharedSuite.h) declares
`GetApiVersion` and `ProcessBytes` only: no AddSuite provider, consumer, allocator,
thread policy or error-code implementation is shipped. Sweetie/Checkout are the
dated SDK source patterns, not implementations of BibleCoreSuite1.

For a concrete `ProcessBytes` service, define caller-owned input/output storage,
borrowed-for-call pointers, capacity and required/output-size semantics, aliasing
policy and insufficient-capacity result **before** implementing either side. Do not
read output after service failure unless the contract explicitly defines that output.
`GetApiVersion` success cannot repair acquisition of the wrong table ABI; matching
name/public version and calling convention are prerequisites to calling it at all.
Publication failure leaves the provider unpublished; successful publication followed
by a later initializer failure must retain reachable table/backing state according
to the actual host lifecycle, not free it as ordinary local rollback.

If a concrete provider/consumer product claims these behaviors, useful runtime cases include:

1. provider absent;
2. wrong version;
3. supported version;
4. optional fallback;
5. two consumers acquire/release;
6. consumer early-return still releases;
7. provider function/domain error;
8. malformed size/version;
9. declared concurrency mode;
10. product shutdown with acquisitions released in the intended order;
11. restart/reload behavior only if the product claims it.

These are product runtime/support cases. Bible remains SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED unless a separate runtime record exists.

## 18. Anti-patterns

Avoid:

- table pointer cached after `ReleaseSuite`;
- dangling suite-name pointer in RAII owner;
- provider function table backed by temporary/local storage;
- C++ STL/classes/exceptions in public ABI;
- one mutable global service object with unspecified thread model;
- assuming refcount alone makes arbitrary module unload safe;
- publishing incompatible table under the same public version;
- using PICA as a hidden render-dependency channel.

## 19. Recommended service workflow

~~~text
define stable name + public version
→ define C-shaped table and data structs
→ define ownership/thread/error contract
→ publish table from stable storage
→ consumer acquires exact supported version
→ validate every size/version input
→ execute bounded call
→ release acquisition on every path
→ shut down product state only after product borrowers are gone
~~~

## Связанные материалы

- [Plug-in → Plug-in через PICA](../15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md)
- [Effect ↔ AEGP generic bridge](../15-COMMUNICATION/03-AEGP-TO-EFFECT.md)
- [PICA shared-suite template](../16-WORKING-TEMPLATES/pica-shared-suite/README.md)
- [Memory/lifetime](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md)
- [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md)
