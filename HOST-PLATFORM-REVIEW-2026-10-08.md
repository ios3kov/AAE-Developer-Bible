# Host/platform source rereview — 2026-10-08

Parent: `b5216fbd80ebb63aa48c2ee4b447eab3a9afc99c`. Evidence: **DOCUMENTED**;
application/installer/driver/renderer runtime **NOT_RUN**.

## Что прочитано

| Официальный источник | Дата страницы | Реальная область чтения |
|---|---|---|
| [AE release notes](https://helpx.adobe.com/after-effects/desktop/what-s-new/release-notes-after-effects.html) | 2026-09-09 | Release identity и ссылки на requirements/issues |
| [AE system requirements](https://helpx.adobe.com/after-effects/desktop/get-started/technical-requirements/system-requirements.html) | 2026-09-09 | Applicable versions и полные Windows/macOS tables |
| [Advanced3D](https://helpx.adobe.com/after-effects/desktop/work-with-3d-composition/advanced-3d-renderer/advanced-3d-renderer.html) | 2025-04-02 | Renderer overview и hardware requirements; остальная UI-инструкция не объявлена полным API review |
| [Known issues](https://helpx.adobe.com/after-effects/desktop/troubleshooting/fixed-and-known-issues/known-issues-after-effects.html) | 2026-10-07 | General issues и versioned sections опубликованной страницы |

Это датированные чтения mutable vendor pages, не immutable SDK archive.
Первый обзор2026-10-07 получил HTTP403; новое успешное чтение закрывает именно
тот access gap и не меняет историческую запись о неудачной попытке.

## Перенос в главы

[Environment matrix](00-START-HERE/02-ENVIRONMENT-MATRIX.md#host-snapshot-2026-10-08)
содержит компактный host snapshot и правила согласования с renderer page.
Windows ARM, Universal и GPU главы ссылаются на одну матрицу, чтобы не поддерживать
несколько расходящихся копий. Разделены host eligibility, SDK contract baseline,
toolchain/deployment target, продуктовая поддержка и реально проверенная среда.

Выявленное расхождение общей и renderer-страницы сохранено с датами; старые строки
не перенесены как более низкий универсальный minimum. Known issues используются
как основания для адресной диагностики/выбора product cases. Системные изменения
не превращены в автоматический этап установки плагина.

## Что не закрыто этим блоком

Не получены новые proprietary SDK bytes, header/suite ABI или platform build
results. Не проверены устройства, драйверы, installation/signing, GPU callbacks,
Advanced3D output или наличие UXP в установленном AE. Требования приложения
не являются перечнем всех возможностей plugin API.
