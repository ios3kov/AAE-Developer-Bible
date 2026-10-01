# AEGP → Effect: generic call

Обновлено **2026-10-01** по присланному **SDK 25.6 build 61**. Это documented direct call path между AEGP и конкретным экземпляром Effect. Он не заменяет render dependency graph и не является общим IPC.

Подробная сверка: [SDK 25.6 — PICA, Effect↔AEGP и legacy boundaries](../18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).

## 1. Текущий контракт SDK 25.6

В current SDK 25.6 `AEGP_EffectCallGeneric` находится в `AEGP_EffectSuite5` и имеет смысловую форму:

```text
AEGP_EffectCallGeneric(
    plugin_id,
    effect_ref,
    layer_time,
    effect_command,
    effect_extra)
```

Комментарий прямо говорит: чтобы получить старое поведение, нужно передать `PF_Cmd_COMPLETELY_GENERAL` как `effect_command`.

Effect API определяет `PF_Cmd_COMPLETELY_GENERAL` как команду для общих вызовов через AEGP.

Источник: `Headers/AE_GeneralPlug.h:2162–2168`, `Headers/AE_Effect.h:1228–1236`.

## 2. Version boundary: старый sample и текущий header различаются

Bundled `ProjDumper` вызывает старую `EffectSuite2` форму:

```text
EffectCallGeneric(plugin_id, effect_ref, time, extra)
```

То есть без отдельного `PF_Cmd` аргумента.

Это полезный исторический pattern, но **не current suite generation SDK 25.6 для нового кода**. В новой реализации нельзя копировать старую строку вызова буквально; нужно компилировать против текущего header.

Источник: `AEGP/ProjDumper/ProjDumper.cpp:142–168`.

## 3. Effect side

Bundled `Shifter` обрабатывает `PF_Cmd_COMPLETELY_GENERAL` в своём dispatcher и получает payload через `extra`.

В sample payload трактуется как C-string и копируется в return message. Это демонстрация связи, а не production protocol:

- нет size/version header;
- sample предполагает ожидаемый payload type;
- это не контракт для binary-compatible сложных структур;
- sample не устанавливает право хранить `extra` после возврата команды.

Источник: `Effect/Shifter/Shifter.cpp:317–327,555–617`.

## 4. Время вызова

Текущий header указывает, что `timePT` использует **timebase слоя, на котором находится effect**. Поэтому comp-time значение нельзя бездумно передавать как layer-time.

Если вызывающая логика живёт в comp time, сначала используйте документированный механизм преобразования времени, а не собственную догадку о start-time/stretch.

## 5. Хороший payload contract

Для пары модулей одного продукта payload должен быть self-describing:

```cpp
struct BridgeMessageV1 {
    uint32_t size;
    uint32_t version;
    uint32_t opcode;
    uint32_t flags;
    uint64_t request_id;
    int32_t result_code;
};
```

Перед чтением расширения effect проверяет минимум `size` и `version`.

Не передавайте через ABI:

- `std::string`;
- STL containers;
- exceptions;
- указатели на object graph с неизвестным lifetime;
- platform-specific class instances без общего binary contract.

## 6. Синхронный call не даёт права сохранить pointer

API передаёт `void* effect_extraPV` на время вызова. В просмотренном контракте нет обещания, что Effect может сохранить этот pointer и использовать позже.

Поэтому безопасная модель по умолчанию:

```text
caller builds payload
→ generic call
→ effect reads/writes payload synchronously
→ call returns
→ payload may cease to exist
```

Если нужен долгоживущий обмен, используйте собственный versioned service/handle protocol, а не скрытое сохранение raw pointer.

## 7. Для чего подходит

- ping/handshake;
- invalidate/reload control resource;
- маленькая команда конкретному effect instance;
- синхронный запрос/ответ;
- диагностическая команда между модулями одного продукта.

## 8. Для чего не подходит

Generic call не должен становиться скрытой render dependency:

```text
AEGP changed hidden state
→ renderer depends on it
→ AE dependency/cache graph об этом не знает
→ stale frame / inconsistent render
```

Render-affecting state должен быть выражен поддержанными параметрами/dependencies/cache identity механизмами.

Также generic call не заменяет published suite, когда нужен многофункциональный service для нескольких consumers.

## 9. Lifetime target effect

AEGP сначала должен получить `AEGP_EffectRefH`, вызвать операцию и затем освободить ref правильным API. Generic call не передаёт ownership effect-ref в Effect.

Не кешируйте старый `AEGP_EffectRefH` как вечный идентификатор без отдельной гарантии host API.

## 10. Error model

Есть минимум два уровня результата:

1. `A_Err` самого AEGP call;
2. результат вашего protocol внутри payload.

Не смешивайте их. Ошибка доставки/host call и «команда дошла, но provider отказал» — разные состояния.

## 11. Product validation guidance

If a concrete product claims bridge behavior, useful runtime cases include:

- target effect missing;
- wrong protocol version;
- short payload;
- unknown opcode;
- valid request/response;
- target disabled/reordered/removed;
- correct layer-time conversion;
- repeated calls;
- save/reopen only when protocol affects persistent state;
- no stale render cache when render-affecting state changes.

These are product evidence cases, not Bible completion requirements.

## 12. Target resolution and stale refs

Resolve `AEGP_EffectRefH` as late as practical for each semantic command.

Do not let panel/background work hold one EffectRef across arbitrary project edits.

Recommended:

~~~text
stable product target identity
→ host-safe command starts
→ resolve current layer/effect
→ acquire caller-owned EffectRef
→ generic call
→ dispose EffectRef
~~~

If the effect is removed/reordered while an async request is pending, reject/re-resolve rather than calling a stale ref.

## 13. Protocol evolution

Treat message version as product ABI.

For a new incompatible message:

- bump version;
- validate `size` before optional fields;
- keep reserved fields zero/defined;
- define whether old caller/new effect combinations fail or degrade;
- do not reinterpret shorter V1 storage as larger V2 without size checks.

For additive tails:

~~~text
if size >= offset + field_size:
    read optional field
else:
    use documented default
~~~

## 14. Reentrancy and callback work

A generic call is synchronous, but effect code may still call host APIs or product services.

Avoid holding a product mutex across `AEGP_EffectCallGeneric` if the effect-side command can re-enter another product path needing the same lock.

Keep COMPLETELY_GENERAL handlers bounded; do not turn a synchronous control call into a hidden long-running worker join/network operation.

## 15. Persistent vs transient commands

Transient command examples:

- ping;
- invalidate runtime cache;
- request diagnostics.

Persistent state change:

- must map to project/effect-visible persistent state if the result must survive save/reopen;
- should not live only in a global service object changed by generic call.

A generic call is a transport, not a persistence model.

## 16. Anti-patterns

Avoid:

- saving `effect_extraPV` beyond return;
- storing EffectRef forever;
- passing comp time as layer time by assumption;
- STL/C++ object ABI;
- using generic call as a multi-consumer service bus;
- hidden render-affecting mutable state;
- treating host `A_Err` success as domain-command success;
- blocking long-running work inside the synchronous call.

## Related

Связанный шаблон: [effect-aegp-generic-bridge](../16-WORKING-TEMPLATES/effect-aegp-generic-bridge/README.md).
