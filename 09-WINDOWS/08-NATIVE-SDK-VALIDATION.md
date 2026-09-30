# Windows — native SDK validation

Перед Visual Studio build прогонять header-derived validation из `18-SDK-HEADER-TOOLS/`.

```powershell
cd 18-SDK-HEADER-TOOLS
.\run-windows.ps1 "C:\path\to\After Effects SDK\Examples\Headers"
```

PASS означает только:

- headers распарсились;
- inventory создан;
- suite symbols в наших cookbook C++ recipes существуют в указанном SDK.

После этого обязательны MSVC compile/link и запуск plug-in внутри целевого After Effects. Code signing проверяется отдельным release pipeline.
