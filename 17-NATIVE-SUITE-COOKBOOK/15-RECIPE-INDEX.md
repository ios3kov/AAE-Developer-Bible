# Native recipe index

## Project graph

- get current project → `01-PROJECT-ITEMS.md`
- root folder → `01-PROJECT-ITEMS.md`
- iterate items → `01-PROJECT-ITEMS.md`
- create folder → `01-PROJECT-ITEMS.md`
- rename/delete item → `01-PROJECT-ITEMS.md`
- create composition → `02-COMPOSITIONS.md`
- create solid/camera/light/text → `02-COMPOSITIONS.md`
- get layers → `03-LAYERS.md`
- add/duplicate/delete layer → `03-LAYERS.md`
- stable LayerID → `03-LAYERS.md`

## Effects + properties

- enumerate effects → `04-EFFECTS.md`
- find installed effect → `04-EFFECTS.md`
- apply/delete effect → `04-EFFECTS.md`
- AEGP→Effect generic call → `04-EFFECTS.md`
- get layer property stream → `05-STREAMS-PROPERTIES.md`
- get effect parameter stream → `05-STREAMS-PROPERTIES.md`
- read/set property → `05-STREAMS-PROPERTIES.md`
- expressions → `05-STREAMS-PROPERTIES.md`
- dynamic hierarchy → `05-STREAMS-PROPERTIES.md`

## Animation

- enumerate/add/delete keyframes → `06-KEYFRAMES.md`
- batch keyframes → `06-KEYFRAMES.md`
- masks → `07-MASKS.md`
- text → `08-TEXT-MARKERS.md`
- markers → `08-TEXT-MARKERS.md`

## Render

- render item/frame to pixels → `10-RENDER-FRAMES.md`
- receipt/world ownership → `10-RENDER-FRAMES.md`
- add comp to Render Queue → `11-RENDER-QUEUE.md`
- configure output module → `11-RENDER-QUEUE.md`
- start queue → `11-RENDER-QUEUE.md`

## Host infrastructure

- undo → `12-MEMORY-UNDO-PERSISTENCE.md`
- host memory → `12-MEMORY-UNDO-PERSISTENCE.md`
- preferences → `12-MEMORY-UNDO-PERSISTENCE.md`
- 26.5 guides → `13-GUIDES-VIEWS-SELECTION.md`
- selection → `13-GUIDES-VIEWS-SELECTION.md`
- stale handles/threading → `14-LIFETIME-THREADING.md`

## Drop-in code

“Drop-in” means graft into a licensed SDK sample project, not standalone build or
complete commands. For scoped import/adopt/create/animate/queue and frame chains,
use [the operation walkthrough](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md) alongside
the individual chapters. [Source guide](code/README.md) lists actual implemented
fragments; masks, text/markers and footage have contract/design routes, not separate
authored translation units. [Evidence](VERIFICATION.md) retains exact identity limits.

| Task | Chapter route | Actual source |
|---|---|---|
| Project/root/item traversal | [Project/items](01-PROJECT-ITEMS.md) | [ProjectItemRecipes](code/ProjectItemRecipes.cpp) |
| Fixed comp / bounded LayerIDs | [Compositions](02-COMPOSITIONS.md), [layers](03-LAYERS.md) | [CompLayerRecipes](code/CompLayerRecipes.cpp) |
| Installed match / apply / static OneD | [Effects](04-EFFECTS.md), [streams](05-STREAMS-PROPERTIES.md) | [EffectStreamRecipes](code/EffectStreamRecipes.cpp) |
| OneD CompTime batch | [Keyframes](06-KEYFRAMES.md) | [KeyframeRecipes](code/KeyframeRecipes.cpp) |
| Borrowed options → receipt/world/checkin | [Frames](10-RENDER-FRAMES.md) | [RenderRecipes](code/RenderRecipes.cpp) |
| Add/path/QUEUED/readback | [Queue](11-RENDER-QUEUE.md) | [RenderQueueRecipes](code/RenderQueueRecipes.cpp) |

См. [`code/`](code/README.md):
- common RAII patterns;
- project/item traversal;
- comp/layer operations;
- effect/stream operations;
- keyframe batch transaction;
- render receipt transaction.

## Full suite function map

- suite/function capability index → `16-SUITE-FUNCTION-MAP.md`
