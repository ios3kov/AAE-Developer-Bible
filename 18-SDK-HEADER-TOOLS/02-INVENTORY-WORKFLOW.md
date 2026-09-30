# Workflow: от SDK headers до рабочего recipe

1. Установить/распаковать целевой AE SDK.
2. Запустить `ae_sdk_inventory.py` на Include/Headers.
3. Зафиксировать JSON inventory рядом с build artifacts конкретной версии SDK.
4. Запустить `verify_recipe_symbols.py` на C++ recipes.
5. Если обновился SDK — построить новый JSON и прогнать `diff_sdk_inventory.py`.
6. Любой changed signature вручную проверить в header и ближайшем Adobe sample.
7. Только после этого обновлять compatibility matrix и минимальную AE version.

## Почему это важнее статического справочника

Suite API versioned. Даже если имя функции не меняется, меняется generation таблицы, availability host version и иногда соседние types/macros. Статический Markdown неизбежно стареет; header-derived inventory привязан к реальной сборке.

## CI gate

Минимальный native CI gate:

```text
inventory generation
  ↓
recipe symbol verification
  ↓
compile Debug
  ↓
compile Release
  ↓
unit tests pure C++
  ↓
package/sign
  ↓
host smoke test (отдельный runner/машина с AE)
```

Host smoke test нельзя заменить компиляцией: PiPL, loader, missing suites, signing, MFR и GPU ошибки проявляются уже внутри AE.
