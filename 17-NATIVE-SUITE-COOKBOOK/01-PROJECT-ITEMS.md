# Project + Item recipes

**Primary Bible baseline:** Adobe After Effects SDK **25.6 build 61**.

**Suites:** `AEGP_ProjSuite6`, `AEGP_ItemSuite9`.

Project/Item APIs look simple, but they sit above the whole project graph. Treat structural mutation and identity carefully.

## Project count and project root

Conceptual pattern:

```cpp
A_long project_count = 0;
ERR(suites.ProjSuite6()->AEGP_GetNumProjects(&project_count));

if (!err && project_count > 0) {
    AEGP_ProjectH projectH = nullptr;
    AEGP_ItemH rootH = nullptr;
    ERR(suites.ProjSuite6()->AEGP_GetProjectByIndex(0, &projectH));
    ERR(suites.ProjSuite6()->AEGP_GetProjectRootFolder(projectH, &rootH));
}
```

Do not hardcode the assumption “exactly one project” as a permanent API truth just because a historical sample did.

## Project handle

### Companion source is a bounded query, not project management

[`ProjectItemRecipes.cpp`](code/ProjectItemRecipes.cpp) implements only first-project
root lookup and item counting. `Bible_GetProjectAndRoot` chooses index 0 after a
count check; it does not implement project selection, ID resolution, folder creation
or any mutation described below. On failure its output handles are not a complete
result (project lookup may succeed before root lookup fails). Initialize outputs and
consume them only after success. `Bible_CountProjectItems` clears the count before
traversal but may leave a partial count on error; do not report it as the total.
These helpers rely on the caller's supported host callback and exception boundary.

`AEGP_ProjectH` is a host-owned project reference.

Do not:

- free/delete it;
- serialize its numeric pointer value;
- use it as cross-session identity.

If feature needs persistent product state, store your own schema/identifiers and re-resolve current project context.

## Iterate project items

Current ItemSuite9 contract:

```text
GetFirstProjItem(project)
→ ItemH or null
→ GetNextProjItem(project, current)
→ next ItemH
→ null after last item
```

Example:

```cpp
AEGP_ItemH itemH = nullptr;
ERR(suites.ItemSuite9()->AEGP_GetFirstProjItem(projectH, &itemH));

while (!err && itemH) {
    // inspect itemH
    AEGP_ItemH nextH = nullptr;
    ERR(suites.ItemSuite9()->AEGP_GetNextProjItem(projectH, itemH, &nextH));
    itemH = nextH;
}
```

## Do not destructively mutate through a traversal cursor

Bad pattern:

```text
GetNext(current)
→ delete current
→ assume stored next remains valid forever
```

Structural changes can invalidate graph assumptions.

For destructive batch:

```text
first pass: collect stable product targets / item IDs
→ end traversal
→ second pass: re-resolve/validate current graph
→ mutate
```

## Item types

`AEGP_GetItemType` distinguishes comp/folder/footage and other item categories.

Always inspect type before calling type-specific APIs.

Do not infer type from:

- display name;
- extension;
- Project panel icon;
- parent folder.

## Item name ownership

`AEGP_GetItemName` returns an `AEGP_MemHandle` containing null-terminated UTF-16 text and the header explicitly says it must be freed through Memory Suite.

Pattern:

```text
GetItemName
→ MemHandle
→ lock
→ copy/use
→ unlock
→ FreeMemHandle
```

Do not retain locked pointer after unlock/free.

## Rename item

`AEGP_SetItemName` takes null-terminated UTF-16 and is undoable.

Convert product/user strings deliberately. Do not build real Unicode names with ASCII initializer shortcuts.

## Item ID

`AEGP_GetItemID` returns an `A_long` item ID.

Useful role:

```text
current ItemH
→ item ID
→ product command/snapshot
```

Current ItemSuite9 does **not** provide a generic `GetItemFromID` lookup in the reviewed header.

So to resolve a stored item ID later, a product may need to traverse current project items and compare IDs.

Do not document Item ID as a magical cross-project/cross-session database key unless the API guarantees that boundary.

## Create folder

Current contract:

```cpp
AEGP_ItemH folderH = nullptr;
ERR(suites.ItemSuite9()->AEGP_CreateNewFolder(
    utf16_name,
    parent_folderH0,
    &folderH));
```

Header marks returned folder as allocated/owned by AE.

Do not free it as product memory.

Historical public HTML has shown an extra project-handle argument in some renderings. Exact SDK header wins.

## Parent folder

Use Item Suite to query/set item parent folder where the operation is supported.

Before moving many items:

- validate target folder;
- avoid accidental self/descendant logic where relevant;
- capture targets before structural mutation;
- re-query graph after mutation.

## Delete item

`AEGP_DeleteItem` is undoable and header says it removes the item from all compositions.

After successful delete:

```text
ItemH is no longer a valid target
→ drop it
→ re-query project graph
```

Deletion can therefore have wider project impact than “remove one row from Project panel”.

## Current time is not render time

`AEGP_GetItemCurrentTime` returns item native time and header notes it is **not updated while rendering**.

Do not use Project-panel current time as render-time truth.

Render workflows should use explicit render context/options time.

## Native timespaces

`AEGP_GetItemDuration` uses the item's native time space:

- comp → comp time;
- footage → footage time;
- folder → zero duration.

Do not compare `A_Time` values from different domains without conversion.

## Dimensions/PAR

Item dimensions and pixel aspect are useful metadata, but not every item category has the same semantic meaning.

Validate type before using dimensions as raster-source assumptions.

## Selection

`AEGP_GetActiveItem`, selection APIs and Project-panel selection are UI state.

Use them to start a command, then normalize explicit target identity.

Do not let background work depend on a borrowed “whatever is active now” handle.

## New/Open project operations

Project Suite has operations that can create/open projects and may affect currently opened project state.

Treat them as high-impact commands:

- explicit user intent;
- dirty-project policy;
- save/close implications;
- UI state;
- failure handling.

Do not hide project replacement inside a helper named `EnsureProject()`.

## Undo vs dangerous project operations

Ordinary item rename/move/delete can be undoable.

Opening/replacing project is a different class of lifecycle transition. Do not assume Undo group protects project-open semantics.

## Batch graph workflow

Recommended:

```text
resolve project
→ traverse and normalize target IDs/types
→ build pure plan
→ validate current state
→ StartUndoGroup
→ re-resolve target ItemH
→ mutate
→ drop host refs
→ return fresh project summary
```

## Failure modes

Plan for:

- no project;
- item deleted/renamed meanwhile;
- wrong item type;
- invalid parent folder;
- Unicode/path conversion failure;
- partial batch mutation;
- user changes active project/item during async work.

## Product pattern: find item by stored ID

Because current Item Suite exposes `GetItemID` but not a generic direct item-ID resolver in the reviewed table:

```text
stored item ID
→ traverse current project
→ GetItemID(each)
→ compare
→ use fresh ItemH
```

Cache an index only as an optimization, never as authoritative identity.

## Related chapters

- [Compositions](02-COMPOSITIONS.md)
- [Layers](03-LAYERS.md)
- [Footage/import](09-FOOTAGE-IMPORT.md)
- [Memory/undo/persistence](12-MEMORY-UNDO-PERSISTENCE.md)
- [Project/render automation](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)

## Evidence boundary

`ProjSuite6`/`ItemSuite9` declarations and ownership comments are SDK-contract-reviewed against SDK 25.6. Runtime behavior of a particular project-management product is not claimed by this recipe.
