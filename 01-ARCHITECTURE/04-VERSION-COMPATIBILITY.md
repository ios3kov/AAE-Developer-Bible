# Version compatibility

## Policy

Собирать обычно разумно с новыми SDK headers, но **заявлять поддержку только тех AE versions, которые реально протестированы**.

Новый SDK не означает обязательный новый binary на каждую версию AE, но новая функция может потребовать suite/API gating.

## Runtime checks

Effect plug-in может ориентироваться на host/API version из данных, передаваемых host. AEGP также получает version information. Для точного app version при необходимости можно использовать поддержанные host/script mechanisms.

## Compatibility contract

Для каждой release записывать:

| AE | mac arm64 | mac x86_64 | Win x64 | Win ARM64 | Status |
|---|---:|---:|---:|---:|---|
| 25.x | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | tested |
| 26.x | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | tested |
| Beta | lab only | lab only | lab only | lab only | never claim from smoke only |

## Forward compatibility rule

При выходе нового AE:
1. install on clean test system;
2. load test;
3. render golden projects;
4. MFR on/off;
5. GPU on/off and available backends;
6. save/reopen project;
7. render queue/export;
8. performance comparison;
9. only then update support statement.
