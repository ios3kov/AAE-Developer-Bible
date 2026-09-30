# Lifetime + threading rules

Это самый важный cross-cutting раздел cookbook.

## 1. Borrowed vs owned

Нельзя придумать универсальное правило «все handles надо dispose». В AE API есть:

- borrowed host handle;
- plug-in-owned reference;
- checkout receipt;
- memory handle;
- begin/end cookie.

Каждая категория закрывается **своей парой**.

## 2. Structural invalidation

Особенно опасны:
- Dynamic Stream hierarchy;
- Render Queue items/output modules;
- effect refs при delete/reorder;
- layer refs после delete;
- project/item graph после destructive changes.

После structural mutation считать соседние transient refs подозрительными и re-query.

## 3. Begin/end transactions

Примеры:
- `StartUndoGroup` / `EndUndoGroup`;
- `StartAddKeyframes` / `EndAddKeyframes`;
- render `Checkout` / `Checkin`.

Production code должен гарантировать закрытие пары на каждом error path.

## 4. UI/project state vs render

Не делать project mutation из:
- MFR worker;
- effect render callback;
- arbitrary background thread.

Command/idle/panel callback должен передавать immutable work в background core, а mutation результата — возвращаться в допустимый host context.

## 5. AEGP из Effect render

AE позволяет effects использовать некоторые AEGP suites, но официальный guide предупреждает о hidden dependency/caching bugs. Если AEGP query влияет на пиксели, AE может не знать, что cache invalid.

Правило:

```text
render result depends on data?
→ data must be represented in effect dependency/state contract
→ otherwise do not query it ad hoc from AEGP during render
```

## 6. Не держать mutex во время host call

Плохо:

```text
lock(global_mutex)
→ AE suite call
→ host re-enters your code
→ tries same mutex
→ deadlock
```

Правильно:
- copy state under lock;
- unlock;
- call host;
- merge result under lock if needed.

## 7. Plugin unload

Death hook:
- отменить/закрыть ваш background work;
- отцепить callbacks;
- освободить собственные resources;
- не обращаться к уже уничтоженным host objects.

## 8. Versioned feature boundaries

Compile-time availability != runtime host availability.

Если поддерживается несколько AE:
- собрать против выбранного minimum/SDK strategy;
- acquire/check suite;
- feature gate;
- test matrix по каждому host.
