# Project + Item recipes

**Suites:** `AEGP_ProjSuite6`, `AEGP_ItemSuite9`  
**Confidence:** SDK-verified + sample-derived (`Projector`)

## Получить текущий project и root folder

```cpp
A_Err GetProjectRoot(
    SPBasicSuite* pica,
    AEGP_ProjectH* projectPH,
    AEGP_ItemH* rootPH)
{
    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    A_long project_count = 0;
    ERR(suites.ProjSuite6()->AEGP_GetNumProjects(&project_count));

    if (project_count < 1) {
        return A_Err_GENERIC;
    }

    ERR(suites.ProjSuite6()->AEGP_GetProjectByIndex(0, projectPH));
    ERR(suites.ProjSuite6()->AEGP_GetProjectRootFolder(*projectPH, rootPH));
    return err;
}
```

### Важно

В публичной HTML-документации встречается typo `AEGP_GetProjectProjectByIndex`. Фактическое имя в SDK/header bindings — `AEGP_GetProjectByIndex`.

---

## Обойти project items

```cpp
A_Err VisitItems(
    SPBasicSuite* pica,
    AEGP_ProjectH projectH,
    void (*visit)(AEGP_ItemH))
{
    A_Err err = A_Err_NONE;
    AEGP_SuiteHandler suites(pica);

    AEGP_ItemH itemH = nullptr;
    ERR(suites.ItemSuite9()->AEGP_GetFirstProjItem(projectH, &itemH));

    while (!err && itemH) {
        visit(itemH);

        AEGP_ItemH nextH = nullptr;
        ERR(suites.ItemSuite9()->AEGP_GetNextProjItem(projectH, itemH, &nextH));
        itemH = nextH;
    }
    return err;
}
```

Не удалять текущий `itemH` и затем слепо использовать старый `nextH`. Для destructive iteration сначала собрать stable IDs либо повторно получить graph.

---

## Узнать тип item

```cpp
AEGP_ItemType type = AEGP_ItemType_NONE;
ERR(suites.ItemSuite9()->AEGP_GetItemType(itemH, &type));

if (type == AEGP_ItemType_COMP) {
    // composition
}
```

---

## Получить имя item

`AEGP_GetItemName` возвращает host memory handle. Его надо освободить через Memory Suite.

Паттерн:

```cpp
AEGP_MemHandle nameH = nullptr;
ERR(suites.ItemSuite9()->AEGP_GetItemName(
    plugin_id,
    itemH,
    &nameH));

if (!err && nameH) {
    // lock/read with MemorySuite according to SDK sample
    // ...
    ERR2(suites.MemorySuite1()->AEGP_FreeMemHandle(nameH));
}
```

Не сохранять указатель, полученный после lock, после unlock/free.

---

## Переименовать item

```cpp
const A_UTF16Char new_name[] = { 'R','e','n','a','m','e','d',0 };
ERR(suites.ItemSuite9()->AEGP_SetItemName(itemH, new_name));
```

На практике используйте собственный UTF-8→UTF-16 helper, а не ASCII initializer.

---

## Создать folder

Фактический header contract для современных SDK:

```cpp
AEGP_ItemH folderH = nullptr;
ERR(suites.ItemSuite9()->AEGP_CreateNewFolder(
    utf16_name,
    parent_folderH,   // nullptr → root where API permits
    &folderH));
```

В части публичной HTML-документации исторически встречалась лишняя `projH`-позиция. Проверять установленный `AE_GeneralPlug.h`.

---

## Удалить item

```cpp
ERR(suites.ItemSuite9()->AEGP_DeleteItem(itemH));
itemH = nullptr; // не использовать после удаления
```

После structural mutation re-query graph.

---

## Практический pattern: найти comp по item ID

Лучше сохранять `AEGP_ItemID`, а не `AEGP_ItemH`.

```text
iterate current project items
→ GetItemID()
→ compare stable stored ID
→ use fresh ItemH
```

Это устойчивее к большинству изменений project graph.
