# Windows — GPU development

Эта глава описывает Windows-specific слой GPU effect development. Общая lifecycle-модель — в [GPU effects](../02-EFFECT-PLUGINS/05-GPU.md).

## Главный принцип

Математический contract должен быть backend-independent:

```text
Render intent / parameter model
       ├── CPU
       ├── CUDA
       └── DirectX
```

Backend selection — отдельный слой. CPU/CUDA/DirectX не должны иметь разные alpha/HDR/edge semantics.

## Host framework/device context

Если AE передаёт framework/device context, используйте его как source of device identity. Не создавайте скрытую GPU selection policy, расходящуюся с host scheduling.

## CUDA dependency policy

Решите явно:

- Driver API vs Runtime API;
- static vs dynamic runtime where applicable;
- driver/device capability;
- failure/fallback behavior.

Нельзя зависеть от CUDA DLL только потому, что она случайно присутствует на development machine.

## CUDA Driver API

Driver API может уменьшить зависимость от конкретной user-space runtime DLL distribution, но не отменяет driver compatibility, device capability и error handling.

## CUDA Runtime API

Если используете Runtime API, зафиксируйте linkage, required DLL/runtime, installer ownership, version и search path.

Не позволяйте Windows DLL search случайно подхватить несовместимую библиотеку чужого продукта.

## DirectX backend

DirectX path может включать shader source, generated shader binary, DXC build dependency и runtime assets.

Generated assets должны входить в release package и находиться через controlled path.

## Capability declarations

Effect flags/PiPL должны соответствовать реально поддерживаемому backend path. Нельзя объявить DirectX support и не иметь рабочего resource/shader path.

## Per-device state

Используйте device-specific pipeline/context/resources и render-local transient state. Не храните один global mutable backend object для всех devices/frames.

## Multi-backend selection

Selection logic должна быть observable:

```text
host framework == DirectX → DirectX backend
host framework == CUDA    → CUDA backend
unsupported               → CPU fallback or explicit unsupported
```

## CPU fallback

Если fallback заявлен, он должен сохранять effect semantics и parameter meaning. Причину fallback полезно логировать один раз, а не каждый frame.

## GPU diversity

Windows GPU landscape неоднороден: vendor, driver branch, integrated/discrete GPU, laptop switching, remote/virtual environment.

«Работает на нашей NVIDIA» не равно общему support claim.

## Driver failures

Классифицируйте unsupported API, driver regression, shader load failure, allocation failure, device lost/reset, timeout и invalid resource state.

## Architecture

x64 и ARM64 требуют полной native dependency chain. ARM64 main `.aex` с x64-only DLL всё равно не является ARM64-ready продуктом.

## Shader/kernel packaging

Не полагайтесь на current working directory, developer absolute path или source-tree layout.

## Debugging CUDA

Разделяйте host-side C++ crash, driver error, kernel launch error, kernel memory bug, synchronization issue и numerical mismatch.

## Debugging DirectX

Разделяйте shader/asset, device/resource creation, command recording, synchronization, state transitions и numerical output.

## MFR + GPU

MFR усиливает race risks в product-owned shared state: global caches, per-device pools, temp buffers, lazy initialization и logging.

GPU driver thread-safety не делает product state thread-safe.

## Correctness

CPU ↔ backend сравнивается по заранее определённой tolerance: float, alpha, HDR, edges, ROI, odd sizes, repeated runs.

## Performance

Измеряйте CPU prepare, upload/copy, compile/load, dispatch, kernel/shader, sync, readback и allocations отдельно.

## Failure policy

```text
backend setup fails
→ cleanup partial resources
→ mark backend unavailable
→ CPU fallback if promised
→ actionable diagnostic
```

Half-initialized global state оставлять нельзя.

## Deployment

Release package должен включать main `.aex`, required DLLs, shader/kernel assets, helper binaries и notices/licenses.

Для каждой DLL должен быть owner/update/uninstall policy.

## Product matrix

Полезно различать Win x64 + CUDA, Win x64 + DirectX, Win ARM64 + supported backend и CPU fallback.

Bible документирует метод и не обязана строить каждый backend artifact.

## Related chapters

- [GPU effects](../02-EFFECT-PLUGINS/05-GPU.md)
- [Windows debugging](03-DEBUGGING.md)
- [Windows ARM64](02-ARM64.md)
- [CPU/GPU equivalence recipe](../12-RECIPES/04-CPU-GPU-EQUIVALENCE.md)
- [Distribution](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)

## Evidence boundary

Это platform architecture/release guidance. Runtime support конкретной GPU/backend/device комбинации принадлежит evidence конкретного продукта.
