# Layer recipes

**Primary Bible baseline:** Adobe After Effects SDK **25.6 build 61**.

**Suites:** `AEGP_LayerSuite9`, with composition context from `AEGP_CompSuite12` where needed.

Later `CompSuite13` notes must stay version-gated.

## Enumerate layers

```cpp
A_long count = 0;
ERR(suites.LayerSuite9()->AEGP_GetCompNumLayers(compH, &count));

for (A_long i = 0; i < count && !err; ++i) {
    AEGP_LayerH layerH = nullptr;
    ERR(suites.LayerSuite9()->AEGP_GetCompLayerByIndex(compH, i, &layerH));
    // use layerH within the current operation
}
```

Layer index is ordering, not persistent identity.

Companion [`CompLayerRecipes.cpp`](code/CompLayerRecipes.cpp) implements only fixed
composition creation and bounded LayerID collection. `Bible_GetLayerIds` writes at
most `capacity` IDs; success does **not** mean all layers fit, and no total count or
truncation flag is returned. Query the current count separately when completeness
matters. `writtenPL` is partial on an SDK error, and even capacity 0 currently requires
a non-null `ids` pointer. Add/rename/duplicate/delete/parent/selection workflows below
are guidance, not functionality implemented by this collector. Re-resolve comp + IDs
before later mutation; caller supplies callback guard and Undo.

## Stable layer ID

Use Layer Suite ID APIs where appropriate:

```text
LayerH
→ GetLayerID
→ LayerID

later in same relevant project/comp context
→ GetLayerFromLayerID
→ fresh LayerH
```

Do not over-promise ID lifetime beyond documented project/import/merge boundaries.

## Add project item as layer

Validate first:

```cpp
A_Boolean validB = FALSE;
ERR(suites.LayerSuite9()->AEGP_IsAddLayerValid(itemH, compH, &validB));
```

Then add only if legal.

Current header-derived `AEGP_AddLayer` returns `AEGP_LayerH*`; some historical HTML showed an incorrect third-argument type.

See [docs errata](../14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md).

## Rename layer

```cpp
ERR(suites.LayerSuite9()->AEGP_SetLayerName(layerH, utf16_name));
```

Validate UTF-16 string lifetime and user input before mutation.

## Duplicate layer

```cpp
AEGP_LayerH duplicateH = nullptr;
ERR(suites.LayerSuite9()->AEGP_DuplicateLayer(layerH, &duplicateH));
```

After duplicate:

- layer indices may change;
- selection may change depending on host behavior;
- cached index→identity maps should be rebuilt.

## Delete layer

```cpp
ERR(suites.LayerSuite9()->AEGP_DeleteLayer(layerH));
layerH = nullptr;
```

After delete, do not call anything through the deleted handle.

Any dependent cached refs/indices should be considered suspect and re-resolved.

## Parent layer

Pattern:

```text
GetLayerParent
→ validate desired new parent
→ SetLayerParent
```

Do not build cycles or assume arbitrary layer types can parent every target. Use documented legality/host behavior.

## Source item

LayerH and source ItemH are different model objects.

A layer may represent:

- footage;
- comp;
- text/shape/null/camera/light-like host objects;
- other layer types without an ordinary source item.

Do not assume every layer has a normal footage source.

## Comp ownership

Layer belongs to a composition context.

Store product identity as:

```text
composition identity
+ layer ID
```

rather than LayerID alone if your product can operate across multiple comps.

## Timing

Layer time-related operations must distinguish:

- comp time;
- layer time;
- in/out;
- start time;
- stretch/time remapping where relevant.

Do not silently convert with project current UI time.

## Selection

Selection is UI state, not stable layer identity.

Safe UI command:

```text
query selected layers
→ normalize comp + LayerIDs
→ validate
→ mutate
```

Do not retain selection collection/LayerH refs through long asynchronous work.

## Effects/properties

To modify a layer's effects/properties, resolve through Effect/Stream/DynamicStream APIs rather than assuming UI index/name is stable.

Use match names where appropriate for effects/properties.

## Undo

For batch layer mutation:

1. resolve target IDs;
2. validate all targets;
3. open undo group;
4. mutate;
5. cleanup/drop refs;
6. return updated summary.

Undo does not guarantee automatic rollback of every partial mutation.

## Invalidation

Operations that structurally change the comp can make previously observed indices stale.

Examples:

- add;
- duplicate;
- delete;
- reorder.

After structural mutation, re-query ordering.

## Long-running commands

If heavy planning happens on worker thread, pass only pure data/stable IDs to worker.

Before host mutation:

- re-resolve comp;
- re-resolve layer;
- validate revision/context;
- then mutate on supported host path.

## Failure modes

Handle:

- comp disappeared;
- layer ID not found;
- wrong layer type;
- add invalid;
- parent invalid;
- user changed project during async work;
- partial batch failure.

## Product pattern

```text
UI intent
→ comp ID + LayerIDs
→ pure operation plan
→ host callback
→ resolve current LayerH refs
→ validate
→ undo
→ mutate
→ fresh state
```

## Related chapters

- [Compositions](02-COMPOSITIONS.md)
- [Effects](04-EFFECTS.md)
- [Streams/properties](05-STREAMS-PROPERTIES.md)
- [Guides/views/selection](13-GUIDES-VIEWS-SELECTION.md)
- [Lifetime/threading](14-LIFETIME-THREADING.md)

## Evidence boundary

`LayerSuite9`/`CompSuite12` baseline is source-reviewed against SDK 25.6. Runtime semantics of a concrete batch tool belong to that product's evidence.
