# Plug-in → Plug-in через published PICA suite

Обновлено **2026-10-01** по SDK 25.6. Для повторяемого in-process service это основной versioned function-table pattern из поставки.

См. также [главу о PICA suites](../14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md) и [source review](../18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).

## Provider

Adobe sample `Sweetie`:

1. создаёт function table со static lifetime;
2. получает `SPSuitesSuite`;
3. добавляет suite в runtime suite list;
4. освобождает только acquisition самого `SPSuitesSuite`.

Ключевые поля публикации:

```text
suite list
provider/host reference
suite name
public API version
internal version
function-table pointer
returned suite reference
```

Source: `AEGP/Sweetie/Sweetie.cpp:23–78`, `Headers/SP/SPSuites.h:116–136`.

## Consumer

Consumer получает exact name/version через `SPBasicSuite::AcquireSuite`, использует table и обязан сделать matching `ReleaseSuite`.

`Checkout` показывает optional dependency: если Sweetie не загружен, sample не считает это фатальной ошибкой для самого effect.

Source: `Headers/SP/SPBasic.h:80–101`, `Effect/Checkout/Checkout.cpp:45–68`.

## ABI rules

- versioned function table;
- stable unique name;
- plain C-shaped data;
- fixed-width primitive types;
- calling convention согласован между provider/consumer;
- no exceptions across boundary;
- no STL ABI;
- каждый pointer имеет documented ownership/lifetime;
- size/version проверяются до чтения расширенной структуры;
- incompatible change получает новую public suite version.

## Public version ≠ internal version

`SPBasicSuite` acquire использует public version. Низкоуровневый `SPSuitesSuite` различает public API version и internal version.

Не используйте internal version как клиентский feature number, если он не является частью вашего публичного договора.

## Optional vs required dependency

**Optional service:**

```text
suite missing
→ feature disabled
→ plug-in remains usable
```

**Required service:**

```text
suite missing
→ initialization fails explicitly
→ clear diagnostic
```

Нельзя просто dereference null suite pointer.

## Load order

Consumer не должен считать наличие provider доказанным только потому, что оба bundle лежат в одной папке.

Если feature optional — acquire-on-use или graceful startup path.

Если feature required — проверяйте acquisition и выдавайте конкретную ошибку. Сам sample Checkout демонстрирует отсутствие provider как реальный сценарий.

## Lifetime

Нельзя:

- хранить table pointer после `ReleaseSuite`;
- хранить borrowed buffer provider после документированного срока;
- считать адрес function pointer постоянным ID;
- предполагать, что опубликованный suite автоматически поддерживает hot replacement.

Sweetie не демонстрирует generic unregister/replacement workflow.

## Threading

Suite availability не означает thread safety.

Provider API должен отдельно объявить:

```text
main-thread-only
render-thread-safe
serialized internally
reentrant / non-reentrant
may call host / must not call host
```

Без этого contract consumer обязан выбирать консервативный путь.

## Error model

Рекомендуемая схема:

```text
transport/acquire error
service function error
protocol/result error
```

Это три разные категории.

## Testing

Минимум:

- provider missing;
- wrong version;
- correct version;
- repeated acquire/release;
- two consumers;
- provider function error;
- malformed sizes;
- consumer early-return cleanup;
- AE restart;
- заявленный concurrency mode.

Шаблон: [pica-shared-suite](../16-WORKING-TEMPLATES/pica-shared-suite/).
