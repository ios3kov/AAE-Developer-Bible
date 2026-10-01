# Source templates and integration guides

Цель раздела — дать **production-shaped source patterns**, которые связывают объяснение Bible с реальным SDK/sample architecture.

Это reference material, а не набор binaries, которые репозиторий обязан собрать.

## Почему не один универсальный проект

Adobe native samples already contain version/platform-specific project, PiPL and resource plumbing. Поэтому Bible хранит в основном:

- **drop-in/source-shaped C++ fragments**;
- **protocol headers**;
- **JSX/CEP mini projects**;
- **integration recipes** — какой sample family использовать и что заменить.

## Templates

| Template | Base | Что иллюстрирует |
|---|---|---|
| `effect-basic/` | SDK Skeleton | registration, parameter, 8/16-bpc render shape |
| `aegp-menu-command/` | Persisto/Projector-style AEGP | menu/update/death-hook lifecycle |
| `effect-aegp-generic-bridge/` | paired Effect + AEGP | generic-call protocol |
| `pica-shared-suite/` | Sweetie-style provider | native service ABI shape |
| `native-panel-registration/` | Panelator | Window menu + dockable-panel registration |
| `keyframer-batch/` | Easy Cheese | batch-keyframe transaction |
| `aeio-registration/` | IO/FBIO | AEIO registration contract |
| `artisan-registration/` | Artie | Artisan registration contract |
| `jsx-tool/` | Scripts folder | undo-safe ExtendScript pattern |
| `cep-panel-bridge/` | CEP extension | panel JS ↔ JSX JSON dispatcher |

## Evidence labels

- **SDK-CONTRACT-REVIEWED** — relevant names/generations/signatures were checked against selected SDK material.
- **SOURCE EXAMPLE** — source illustrates the pattern; runtime behavior is not being claimed.
- **STANDALONE SOURCE** — no Adobe SDK project is required to read/use the JS/HTML source shape.
- **HISTORICAL COMPILE/RUNTIME EVIDENCE** — retained only when such evidence actually exists.

Older `host-test-required` / `host-test pending` labels mean “runtime not claimed”, not “Bible must now run this example”.

If a reader turns a template into a product, use the platform/build/testing chapters for that product's own validation.
