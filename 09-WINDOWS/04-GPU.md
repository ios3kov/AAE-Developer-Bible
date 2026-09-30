# Windows — GPU

Current AE GPU SDK build guide для sample предусматривает Boost, CUDA SDK и DirectX Shader Compiler.

## CUDA

Adobe guide рекомендует CUDA Driver API как наиболее устойчивый к будущим driver versions path.

Если Runtime API необходим:
- static linking runtime может снизить external runtime mismatch;
- dynamic runtime требует контролировать DLL availability/version.

Нельзя просто надеяться на CUDA DLL, случайно поставляемую текущим AE build.

## DirectX

Current guide указывает:
- DXC dependency for sample/toolchain;
- DirectX assets могут генерироваться рядом с binary и должны попасть в deployment;
- effect должен заявить DirectX rendering support flag;
- PiPL должен быть синхронизирован с capability;
- без флага host может уйти на CPU path.

## Multi-backend architecture

```text
RenderCore interface
  ├── CPU
  ├── CUDA
  └── DirectX
```

Selection logic отдельно от mathematical algorithm.

## GPU failure policy

Если GPU backend init/compile/device step неуспешен:
- fail gracefully;
- CPU fallback, если продукт его обещает;
- один понятный diagnostic, а не dialog на каждый frame;
- не оставлять partially initialized global state.
