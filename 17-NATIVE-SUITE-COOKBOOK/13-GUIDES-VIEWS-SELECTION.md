# Guides / Item Views / Selection

Эта глава объединяет три похожих по UI-эффекту, но разных по lifecycle области:

- guide data;
- per-view display state;
- current selection/collections.

Главное правило: **guide model, view state и selection snapshot — не одно и то же**.

## Version boundary

Primary Bible native baseline — SDK **25.6**.

`GuideSuite2` / `ItemViewSuite2` notes относятся к later-version research (26.5) и должны version-gate-иться.

Не подменяйте baseline 25.6 более поздним API только потому, что он удобнее.

## Guide data

Guide API описывает model-level guide information.

В более позднем API доступны richer attributes вроде orientation, position, percentage/pixel mode, color и edge/pinning-related state.

Точный набор зависит от suite generation.

## View state

ItemView API относится к конкретному view/UI context.

Примеры per-view state:

- guides visible;
- snap enabled;
- guides locked.

Это не то же самое, что persistent guide model.

Одна composition/item может иметь guide data, но разные view state.

## Почему разделение важно

Плохая модель:

```text
Guide object == всё, что пользователь видит про guides
```

Правильнее:

```text
item/model guides
+ current view presentation state
```

Это влияет на persistence assumptions, multi-view behavior, panel sync и UI commands.

## Feature gating

Если продукт использует более новый Guide API:

```text
try current/new suite
→ full feature

else try older suite
→ degraded/basic feature

else
→ disable only guide feature
```

Optional Guide suite не должен быть причиной отказа загрузки всего AEGP tool.

## Capability vs version number

Лучше проверять capability вроде «supports guide color?» или «supports percentage position?» через доступный suite contract, а не только `AE >= X`.

## Selection / Collection

Collection Suite используется для host collections и selection-like data.

Selection следует рассматривать как **snapshot**, а не long-lived business model.

```text
query selection now
→ normalize useful identities
→ discard temporary collection/ref
```

Не храните selection collection бесконечно.

## Normalize selection

Для application logic переводите host selection в более устойчивую command model:

- ItemID;
- LayerID;
- property identity;
- effect match name + layer identity;
- собственный immutable DTO.

После UI delay/background compute re-resolve target.

## Selection freshness

Пользователь может изменить selection между opening panel, click, async computation и final mutation.

Поэтому перед mutation resolve + validate again.

Если операция должна примениться именно к selection-at-click-time, сохраняйте IDs, а не opaque collection handles.

## Multi-selection behavior

Определите semantics:

- all-or-nothing;
- skip unsupported;
- stop on first error;
- report per-item result.

Не оставляйте это случайным следствием loop order.

## Empty selection

Пустая selection — нормальное состояние. UI может disable command, попросить выбрать target или применить explicit default behavior.

## Mixed selection

Если selected AV layer + camera + text, а command умеет только AV layers, либо filter explicitly and report, либо reject whole command.

Не используйте host errors как случайный UX classifier.

## Stable IDs

IDs удобнее refs для long-lived product model, но не обещайте больше стабильности, чем документирует API.

Особенно осторожно с import/merge, duplication, project reopen и structural edits.

## Undo

Selection-driven mutation:

```text
query/normalize selection
→ validate targets
→ StartUndoGroup
→ mutate
→ EndUndoGroup
```

Сначала validate, потом mutate — меньше partial-change failures.

## View commands

View state может быть transient UI state, а не project mutation. Не включайте его автоматически в project undo только потому, что команда пришла из AEGP.

## Threading

Selection/view queries и project mutation выполняются через documented host-safe path.

Background thread может обрабатывать normalized IDs/data, но не держать borrowed UI refs.

## Failure modes

Планируйте:

- view closed;
- active item changed;
- selection changed;
- target deleted;
- suite unavailable;
- mixed unsupported selection;
- guide index invalidated;
- project changed during async task.

Ошибка должна говорить, что именно устарело/недоступно.

## Panel integration

Panel может хранить last normalized selection snapshot для display, но перед destructive command должен revalidate host state.

UI snapshot удобен как projection, не authoritative source.

## Example command pattern

```text
on user action
→ query current selection
→ normalize to stable IDs
→ validate supported targets
→ create immutable command
→ start undo if project mutation
→ re-resolve each target
→ mutate
→ cleanup temporary collections/refs
→ return fresh result/snapshot
```

## Guides command example

Для create-guides preset:

```text
resolve target item
→ acquire supported Guide suite generation
→ map preset to available capabilities
→ add/update guides
→ separately update view visibility only if requested
```

Не смешивайте model guide creation с view visibility как одну implicit operation.

## Product testing guidance

Полезные cases: no active item, empty/mixed selection, item closed during command, selection changed during async compute, older-suite fallback, multiple views, save/reopen for model data.

Bible описывает эти cases; source recipe не обязан заявлять runtime test.

## Related chapters

- [Lifetime/threading](14-LIFETIME-THREADING.md)
- [Project/items](01-PROJECT-ITEMS.md)
- [Layers](03-LAYERS.md)
- [AEGP tools](../14-NATIVE-INTEGRATIONS/05-AEGP-TOOLS.md)
- [Communication architecture](../01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md)

## Evidence boundary

Collection/selection guidance следует AEGP ownership model. `GuideSuite2`/`ItemViewSuite2` material — explicitly later-version research и не должен читаться как SDK 25.6 baseline.
