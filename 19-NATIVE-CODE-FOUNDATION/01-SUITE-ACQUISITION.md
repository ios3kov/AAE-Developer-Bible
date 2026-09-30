# Suite acquisition

PICA suite имеет reference-counted acquire/release contract.

Правильный шаблон:

```text
SPBasicSuite alive
  → AcquireSuite(name, version)
  → validate err + pointer
  → use suite
  → ReleaseSuite(name, version)
```

Не хранить suite pointer после release. Не предполагать, что newest version есть в старом AE. Версия suite — часть compatibility contract.

`code/PicaSuiteRef.h` автоматизирует баланс пары acquire/release, но его lifetime всё равно обязан находиться внутри host lifetime.
