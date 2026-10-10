# AAE Developer Bible v1.2.2 — SDK evidence

В саму книгу и архивы включены [результаты проверки на Mac владельца](NATIVE-SDK-OWNER-CHECK-2026-10-10.md), [машинный отчёт без временных путей](evidence/native-sdk-2026-10-10/native-compile-report.redacted.json) и [его происхождение/хеши](evidence/native-sdk-2026-10-10/provenance.json). README, VERIFICATION, навигация и changelog связывают эти материалы; MASTER/MANIFEST обновлены вместе с исходными документами.

## Что подтверждено отчётом

PROJECT-REPORTED: 13 проверок синтаксиса и типов C++ прошли, ошибок 0, на clean source `0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352` (v1.2.1). Apple clang 21.0.0, target arm64-apple-darwin25.6.0; Adobe SDK 25.6 build 61, Headers + Util manifest содержит 81 header. Это 10 основных исходников, два forwarding entry files и один foundation-header probe, не 13 независимых реализаций.

Публичный JSON сохраняет все результаты и per-source hashes; изменены только временные пути. Исходный отчёт и SDK не публикуются. Отдельно записаны предыдущий неуспешный запуск и успешный повтор с явно переданным SDKROOT. Точное значение SDKROOT в исходном JSON отсутствует и не выдумывается.

## Границы и публикация

Native-код и существующие SDK/compiler-драйверы этим дополнением не изменяются. Проверенный SHA в отчёте не заменяется SHA документационного релиза: новый запуск компиляции/AE не заявляется. Link, PiPL/load, After Effects, MFR/GPU runtime, Windows и [доступ SDK из GitHub CI](CI-GATES.md) этим отчётом не подтверждены.

Издатель проверяет неизменность native-входов, целостность отчёта/provenance, свежесть сохранённых MASTER/MANIFEST и успешные проверки точного итогового коммита. Архивы сверяются с Git tree, загруженные файлы — по SHA-256. Тег v1.2.2, точный release SHA, результаты CI и контрольные суммы устанавливаются опубликованным GitHub Release и `release-evidence.json`, а не заранее этой записью. v1.2.1 и его assets не заменяются.
