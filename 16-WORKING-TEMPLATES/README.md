# Working templates

Цель этого раздела — не псевдокод, а **минимальные production-shaped куски**, которые можно graft/вставлять в официальный SDK sample соответствующего типа.

## Почему это не один «универсальный CMake проект»

Adobe сама рекомендует стартовать от ближайшего SDK sample, потому что PiPL/resource build steps и platform project settings уже настроены. Поэтому шаблоны здесь делятся на:

- **drop-in C++ source** — вставляется в конкретный official sample;
- **protocol headers** — полностью наши, platform-neutral;
- **JSX/CEP mini projects** — самостоятельные файлы;
- **integration recipe** — какой Adobe sample копировать и какой файл заменить.

## Templates

| Template | Base | Что доказывает |
|---|---|---|
| `effect-basic/` | SDK Skeleton | Effect registration, param, render, 8/16 bpc |
| `aegp-menu-command/` | SDK Persisto/Projector-style AEGP | menu + command hook + undo-safe mutation |
| `effect-aegp-generic-bridge/` | paired Effect + AEGP | `AEGP_EffectCallGeneric` ↔ `PF_Cmd_COMPLETELY_GENERAL` protocol |
| `pica-shared-suite/` | SDK Sweetie-style provider | stable native service ABI |
| `native-panel-registration/` | SDK Panelator | native Window-menu + dockable panel registration |
| `keyframer-batch/` | SDK Easy Cheese | correct batch keyframe transaction |
| `aeio-registration/` | SDK IO/FBIO | AEIO registration contract |
| `artisan-registration/` | SDK Artie | Artisan registration contract |
| `jsx-tool/` | Scripts folder | undo-safe ExtendScript tool |
| `cep-panel-bridge/` | CEP extension | panel JS ↔ JSX JSON dispatcher |

## Validation status labels

- **SDK-contract exact** — signatures/patterns follow public current SDK guide; still compile against headers you ship with.
- **drop-in** — intended to replace logic inside named Adobe sample, retaining its PiPL/project files.
- **standalone** — no Adobe SDK compile needed (JSX/HTML).

Нельзя честно назвать C++ binary «compiled/tested in AE» внутри этой sandbox без установленного proprietary SDK + AE host. Поэтому эта библия отличает **working contract template** от **host-verified binary**.
