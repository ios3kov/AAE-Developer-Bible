# SDK Header Tools — полный native API без ручного копирования

Это слой, который делает библию **самопроверяемой относительно конкретного Adobe After Effects SDK**.

Главное правило: HTML guide удобен для объяснений, но **точный контракт сборки задают headers той версии SDK, с которой собирается plug-in**. Поэтому здесь нет вручную переписанного «вечного» списка сотен функций. Вместо этого есть генератор, который читает локальные headers и строит точный inventory.

## Что генерируется

`tools/ae_sdk_inventory.py` находит C ABI function tables:

- `AEGP_*SuiteN` — AEGP host-control API;
- `PF_*SuiteN` — Effect plug-in suites;
- `DRAWBOT_*SuiteN` — native custom UI/Drawbot;
- `AEIO_*FunctionBlockN` — callbacks import/export plug-ins;
- `PR_*EntryPoints` — Artisan/native renderer callbacks;
- другие SDK function tables с типичными именами `Suite`, `FunctionBlock`, `EntryPoints`, `Callbacks`.

Для каждой таблицы сохраняются:

- имя/семейство;
- header-источник и SHA-256;
- все function-pointer names;
- normalized header signatures;
- найденные рядом suite/version macros;
- parser diagnostics для подозрительных таблиц, которые не удалось разобрать.

## Запуск

macOS:

```bash
python3 tools/ae_sdk_inventory.py \
  "/path/to/After Effects SDK/Examples/Headers" \
  --json generated/ae-sdk-inventory.json \
  --markdown generated/ae-sdk-inventory.md
```

Windows PowerShell:

```powershell
py tools\ae_sdk_inventory.py `
  "C:\path\to\After Effects SDK\Examples\Headers" `
  --json generated\ae-sdk-inventory.json `
  --markdown generated\ae-sdk-inventory.md
```

## Проверка наших recipes против SDK

После генерации inventory:

```bash
python3 tools/verify_recipe_symbols.py \
  generated/ae-sdk-inventory.json \
  ../17-NATIVE-SUITE-COOKBOOK/code
```

Скрипт проверяет реальные suite call-sites вида `suite->AEGP_Foo(...)` / `suite->PF_Foo(...)` и выдаёт `UNKNOWN`, если такого function pointer нет в локальных headers.

## Сравнение двух SDK

Сгенерировать JSON для старого и нового SDK, затем:

```bash
python3 tools/diff_sdk_inventory.py old.json new.json --markdown sdk-diff.md
```

Получим added/removed tables, added/removed functions и changed signatures.

## Что уже протестировано здесь

В `tests/fixture_header.h` лежит маленький **синтетический** SDK header. Он не содержит Adobe SDK code, но повторяет ABI-форму function tables. Unit test проверяет named suite, anonymous suite и AEIO-style function block.

```bash
python3 tests/test_inventory.py
```

## Что нельзя честно заявить в песочнице

Здесь нет лицензированного актуального Adobe SDK и самого After Effects, поэтому я не называю generated inventory «проверенным на AE host». На машине разработчика критерий готовности такой:

1. inventory успешно строится из фактических headers;
2. `verify_recipe_symbols.py` не показывает неизвестных calls;
3. код компилируется внутри ближайшего официального Adobe sample;
4. binary загружается в целевой AE;
5. smoke tests проходят на заявленных macOS/Windows + architecture + AE versions.
