# Minimal Gain effect — drop-in for SDK Skeleton

Status: **drop-in / SDK-contract exact pattern**.

## Base

Copy the official SDK `Skeleton` sample first. Keep its Xcode/Visual Studio project, PiPL `.r`, `entry.h`, SDK utils and build steps.

Replace the effect implementation with `EffectMain.cpp`, then update PiPL display/match/category strings consistently.

## Behavior

- one float Gain parameter;
- 8-bpc and 16-bpc processing;
- uses host Iterate suites;
- catches exceptions at C ABI boundary;
- no global mutable render state;
- MFR flag deliberately **not** claimed until tested.

## Why not hand-create project files

Windows PiPL resource generation and platform SDK settings are easy to get subtly wrong. Adobe recommends cloning Skeleton rather than reconstructing the build.
