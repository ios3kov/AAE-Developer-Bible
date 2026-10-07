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

### Current public-contract rereview — 2026-10-07

Pinned guide source `6d9b285d9755d1fbf8ead7680ba49de24f94b547`:
[Guides/Item Views](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aegps/aegp-suites.md#guides).
Exact supplied25.6 `AE_GeneralPlug.h:551–561` has ItemViewSuite1 with playback-time
query only; no GuideSuite/ItemViewSuite2 declarations found in reviewed Headers/Util.
Guide's ItemViewSuite2 detail says **AE26.0+**, although What'sNew groups it with
26.5 SDK additions. Record both sources rather than raising all members to26.5.
No corresponding26.x archive/header acquisition or runtime observation here.

GuideSuite2 extended getters preserve position type/color/pinning. **Base getters
can return a percentage position without indicating its type**; do not interpret
every returned number as pixels. Guide documents pixel clamp±100000, percentage
clamp±300%, nonfinite values rejected; these are public-guide facts, not25.6
header constants. If the feature needs round-trip fidelity, require extended typed
accessors or refuse conversion; an older getter cannot infer the missing unit.

Concrete preset design: target item1920×1080 → vertical25%/75%, horizontal50%.
Extended route uses explicit percentage type; pixel fallback yields x480/x1440/y540
only for this size and loses resize-relative behavior. Report that semantic downgrade
and omit unsupported color/pinning only with explicit user policy. Do not silently
claim a percentage preset has survived a later resize.

Use published `AEGP_AddItemGuide2` then `AEGP_GetItemGuideByIndex2` to read back full
state; range clamping means requested value is not actual state. For edits use
`AEGP_SetItemGuide2`, read back; list indices again after guide structural mutation.
Layer variant has separate target/lifecycle, not an ItemH cast. Only after model
success and valid current view apply optional `AEGP_SetItemViewGuidesVisible`;
snap and locked are separate setters, not side effects of adding a guide. A failed
view update leaves model applied; return per-stage outcome, do not retry creation.
No compiled26.x adapter is supplied: confirm exact suite macros/signatures in the
actual target distribution before implementing this command.

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

Bounded failure route: selection captured at click → normalize project/comp context
and IDs → prepare pure guide preset → on host callback re-resolve item and view.
If project changed, target vanished or required suite is unavailable, refuse before
mutation. An older-suite fallback maps only supported fields explicitly; unsupported
color/pinning is reported, not silently claimed. If model write succeeds but the view
closes before visibility update, report model applied/view update unavailable rather
than pretending both were atomic. No GuidesRecipes.cpp or tested fallback adapter is
shipped; this is UI-command guidance, not baseline availability proof for later APIs.

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
