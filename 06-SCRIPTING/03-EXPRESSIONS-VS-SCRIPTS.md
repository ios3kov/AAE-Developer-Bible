# Expressions vs scripts

Scripts and expressions both use JavaScript-like syntax, but they occupy different semantic roles in After Effects.

## Core distinction

**Script**

~~~text
user/tool command
→ reads project
→ may mutate project structure/state
→ finishes
~~~

**Expression**

~~~text
property evaluation
→ reads allowed context
→ computes property value
→ may be evaluated repeatedly/out of intuitive order
~~~

Do not use an expression as a project-automation engine and do not use a script as a per-frame expression evaluator.

## Scripts are orchestration

Typical script responsibilities:

- create/remove items/layers;
- add effects/properties;
- set keyframes;
- import footage;
- configure render queue;
- rename/restructure project;
- run a user command;
- build rigs/templates.

Scripts can create coherent Undo history and return command success/error.

A script should validate before mutation and reacquire host references after structural changes where required.

## Expressions are evaluation

Typical expression responsibilities:

- calculate one property from time;
- link properties;
- procedural animation;
- derive values from controls/layers;
- small deterministic math.

An expression may be evaluated many times, including during preview/render and cache/dependency work.

Therefore expression code should not depend on hidden call order.

## No side-effect architecture

Treat expressions as value functions.

Do not design an expression to:

- write files;
- mutate the project;
- update UI;
- manage network state;
- keep a reliable mutable global counter;
- perform a one-time project migration.

Those belong in scripts/panels/native tools.

## Performance

An expression can run on many properties across many frames.

Common expensive patterns:

- repeated broad layer/property searches;
- repeated string/path logic;
- deep cross-comp dependency chains;
- duplicated heavy math on many properties;
- unnecessary sample loops.

Move one-time setup into a script when the resulting project can express the dependency directly.

Do not precompute dynamic values in a script if that changes required semantics.

## Identity and naming

Expressions that reference layers/effects by visible name can break after rename/localization/user edits.

Where the expression API provides stable approaches, prefer them; for product-generated rigs, define a naming/metadata policy and migration behavior.

A script generating the rig should validate that the references it creates actually resolve.

## Error handling

Script error:

~~~text
command fails
→ report structured/user-visible error
→ mutation may need cleanup
~~~

Expression error:

~~~text
property evaluation fails
→ AE reports expression error
→ rendered/evaluated value may fall back according to host behavior
~~~

Do not hide a script failure by injecting a broken expression and hoping AE reports it later.

## Version compatibility

Expression engines and available functions can change between AE generations.

For a product shipping expression rigs:

- record oldest/newest tested AE;
- keep old-project fixtures;
- test save/reopen;
- test expressions after project migration;
- avoid relying on a function merely because another Adobe host/browser supports it.

## Script-generated expressions

This is a valid hybrid pattern:

~~~text
script validates rig
→ creates controls/layers
→ assigns known expression source
→ verifies expression enabled/resolves
→ user animates controls
~~~

Treat the expression text as versioned product data.

If its semantics change, consider migration of existing projects rather than silently overwriting user-edited expressions.

## When to choose which

Use a script when the question is:

> What should the project/tool do now?

Use an expression when the question is:

> What value should this property have when AE evaluates it?

Use both when a script creates a stable project structure and expressions provide ongoing value relationships.

## Testing

For script + expression products test:

- fresh rig creation;
- duplicate rig;
- renamed user layers;
- missing target;
- old project;
- save/reopen;
- random frame seeks;
- render queue;
- expression disabled/error state;
- performance on many instances.

See [object model](01-OBJECT-MODEL.md).

## Законченный rig route

[ES3 demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx) создаёт новую
640×360 comp, Null/Slider, text, linear opacity keys, marker и mask. Script
обращается по matchNames; expression связывает opacity с product-controlled
`Bible Control`/`Bible Amount`. Expression прибавляет Slider к анимированному `value`
и ограничивает 0…100. При Slider50 expected opacity=50 в t=0 и100 в t=1;
отключение expression возвращает keyed0→100. Это expectations, не host observation.
`valueAtTime(0,false)` + `expressionEnabled/expressionError` проверяют resolution,
не все frames. Имена expression не становятся stable IDs: rename/missing control
сломает rig; duplicate/migration требует policy владельца продукта.

Expression literal фиксирован, не user string interpolation. Для динамического
имени escape backslash, quote и linebreak в JS literal либо использовать validated
layer-control strategy; не вставлять произвольный текст как executable expression.
Source example не запускался в AE; host expression engine/support нужно проверять
на целевой версии. В error path удаляется только вновь созданная comp; Undo не
считается atomic rollback. User-edited expression не перезаписывается migration
без явного согласия.
