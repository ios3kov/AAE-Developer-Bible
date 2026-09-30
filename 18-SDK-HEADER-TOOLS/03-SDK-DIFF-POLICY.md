# SDK diff policy

При переходе на новый SDK не начинать с «починим compiler errors». Сначала сравнить native contracts.

## Классификация diff

- **Added table/function** — можно использовать только после поднятия minimum host requirement или runtime feature gate.
- **Removed table/function** — blocker; нужен compatibility path.
- **Changed signature** — high risk; проверить ownership, constness, enum/type width и lifecycle.
- **Only version macro changed** — проверить release notes и host availability.
- **No header diff** — всё равно прогнать host regression: поведение AE может измениться без ABI change.

## Release rule

Новая SDK версия не считается принятой в проект, пока не обновлены:

- generated inventory;
- SDK diff artifact;
- build matrix;
- host smoke results;
- compatibility statement.
