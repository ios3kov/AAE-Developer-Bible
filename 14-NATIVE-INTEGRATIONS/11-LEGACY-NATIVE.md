# Legacy / deprecated native integration

Эти пути надо знать при поддержке старого кода, но не выбирать как основу нового продукта без специальной причины.

## Photoshop format plug-ins / filters

After Effects исторически поддерживает часть Photoshop plug-in formats. Для нового AE-native media integration выбирать современные AEIO/MediaCore paths.

## Foreign Project Format (FPF)

Исторический project import path, deprecated в пользу более современных APIs.

## ADM UI

Старый Adobe Dialog Manager использовался некоторыми keyframer/palette samples. Новый продукт не должен начинаться с ADM.

## Старые fixed assumptions

Не переносить в новый код:
- 32-bit-only assumptions;
- Carbon/CFM era platform code;
- устаревшие command IDs как стабильный API;
- global mutable state, рассчитанный на single-frame rendering;
- hard-coded Intel-only binary assumptions.

## Правило библии

Legacy API документируется только с тремя метками:

- **support-only** — чтобы чинить существующий продукт;
- **migration-source** — откуда мигрировать;
- **do-not-start** — не использовать для нового проекта.
