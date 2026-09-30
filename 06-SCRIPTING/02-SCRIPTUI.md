# ScriptUI

ScriptUI подходит для небольших native-looking script tools и floating/palette UI.

## Use when

- UI небольшой;
- tool mostly scripting automation;
- не нужен современный web layout;
- важна минимальная упаковка.

## Avoid when

- сложные virtualized lists/grids;
- account/web workflows;
- modern responsive design;
- сложная app-like state architecture.

Для такого UI — panel technology.

## Architecture

Даже в ScriptUI:
- UI callbacks → command layer;
- command layer → AE scripting operations;
- pure transforms/data logic отдельно.

Это облегчает позже перенос UI на UXP/CEP.
