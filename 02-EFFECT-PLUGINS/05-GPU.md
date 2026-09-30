# GPU effects

GPU path — не отдельный продукт, а оптимизированный backend того же математического эффекта.

## Сначала CPU reference

CPU implementation должна быть:
- правильной;
- deterministic;
- тестируемой;
- достаточно простой, чтобы служить oracle для GPU comparison.

## Build dependencies из актуального SDK Guide

Adobe's GPU sample `SDK_Invert_ProcAmp` требует дополнительные зависимости.

### macOS

Guide указывает Boost для processing GPU kernel files в sample project. Конкретный path задаётся через Xcode custom path/environment настройки sample-а.

### Windows

Guide на 2025/2026 указывает:
- Boost;
- CUDA SDK версии, совместимой с используемым AE build;
- DirectX Shader Compiler (DXC).

Не фиксировать CUDA version навечно в библии продукта: проверять SDK Guide/release notes для каждого supported AE generation.

## DirectX

Если используется DirectX rendering path:
- нужный capability flag должен быть заявлен;
- PiPL должен соответствовать runtime flags;
- generated DirectX assets должны быть установлены рядом/в ожидаемом runtime layout;
- обязателен CPU fallback.

## CUDA

Adobe рекомендует Driver API для лучшей driver compatibility. Если используется Runtime API, осознанно выбрать static/dynamic strategy и контролировать deployment runtime libraries.

## GPU correctness

Сравнивать CPU ↔ GPU:
- 8/16/32-bpc;
- alpha 0/1/partial;
- HDR/negative float values;
- tiny images, odd widths, nontrivial rowbytes;
- extreme parameters;
- edge pixels;
- multiple GPUs / unsupported GPU fallback where possible.

Tolerance должна быть указана **до** теста, а не подобрана после расхождения.

## GPU performance

Профилировать отдельно:
- upload/download;
- kernel dispatch;
- kernel time;
- intermediate allocations;
- synchronization;
- shader compilation/cache warmup.

На маленьком кадре CPU может быть быстрее. Backend selection может учитывать workload size, но не должен менять визуальную семантику.
