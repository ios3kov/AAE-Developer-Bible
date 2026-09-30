# macOS — native SDK validation

Перед Xcode build прогонять header-derived validation из `18-SDK-HEADER-TOOLS/`.

```bash
cd 18-SDK-HEADER-TOOLS
./run-macos.sh "/path/to/After Effects SDK/Examples/Headers"
```

PASS означает только:

- headers распарсились;
- inventory создан;
- suite symbols в наших cookbook C++ recipes существуют в указанном SDK.

После этого обязательны Xcode compile/link и запуск plug-in внутри целевого After Effects. Signing/notarization проверяются отдельным release pipeline.
