# SDK Header Tools — declaration index and symbol-name checks

Это вспомогательный индексатор локальных SDK headers. Он не является C/C++ compiler, signature checker или полным ABI diff. Проверка типов выполняется отдельно через `scripts/check_native.py`.

Главное правило: точный контракт сборки задают headers целевого SDK. Regex parser поддерживает ограниченные формы объявлений. Неполный разбор таблицы теперь сохраняет диагностику и возвращает ошибку; `--allow-incomplete` разрешает только исследовательский индекс. Реальный SDK 25.6 содержит неподдерживаемые объявления, поэтому полного inventory пока нет.

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

Скрипт проверяет имена в call-sites вида `suite->AEGP_Foo(...)` / `suite->PF_Foo(...)`; suite generation, аргументы и типы не проверяются. Пустые/несуществующие входы, отсутствие вызовов и неполный inventory завершаются ошибкой. Комментарии и строки не считаются вызовами.

## Сравнение двух SDK

Сгенерировать JSON для старого и нового SDK, затем:

```bash
python3 tools/diff_sdk_inventory.py old.json new.json --markdown sdk-diff.md
```

Получим added/removed tables/functions, textual signature changes и изменения порядка function fields. Typedef expansion, packing и platform ABI не проверяются. Конфликтующие или неполные inventory отклоняются.

## Что уже протестировано здесь

В `tests/fixture_header.h` лежит маленький **синтетический** SDK header. Он не содержит Adobe SDK code, но повторяет ABI-форму function tables. Unit test проверяет named suite, anonymous suite и AEIO-style function block.

```bash
python3 tests/test_inventory.py
```

## Что нельзя честно заявить в песочнице

В v1.1 выполнены syntax/type checks с локальным SDK 25.6; host validation не выполнялась. Критерий готовности на машине разработчика:

1. inventory успешно строится из фактических headers;
2. `verify_recipe_symbols.py` не показывает неизвестных calls;
3. код компилируется внутри ближайшего официального Adobe sample;
4. binary загружается в целевой AE;
5. smoke tests проходят на заявленных macOS/Windows + architecture + AE versions.
