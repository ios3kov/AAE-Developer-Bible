# GPU effects

Обновлено **2026-10-01** по Adobe After Effects SDK **25.6 build 61**. GPU — не отдельный тип plug-in: это backend Effect API, который должен сохранять ту же визуальную семантику, что CPU path.

Source review: [GPU, audio and Custom UI / Drawbot](../18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md).

## 1. GPU support — не один флаг

В SDK 25.6 GPU-возможность складывается из нескольких стадий:

```text
GLOBAL_SETUP
  declare PF_OutFlag2_SUPPORTS_GPU_RENDER_F32
  (+ DirectX flag where applicable)
        ↓
GPU_DEVICE_SETUP
  create per-device state
        ↓
SMART_PRE_RENDER
  decide whether THIS frame/context can use GPU
  set PF_RenderOutputFlag_GPU_RENDER_POSSIBLE
        ↓
SMART_RENDER_GPU
  render with GPU worlds
        ↓
GPU_DEVICE_SETDOWN
  dispose per-device state
```

То есть глобальная capability не означает, что каждый кадр будет GPU-rendered.

## 2. Framework и device identity приходят от host

`PF_GPU_Framework` в этой поставке содержит NONE, OPENCL, METAL, CUDA и DIRECTX. Setup/render extras передают framework и device index.

Не выбирайте «первую GPU в системе» самостоятельно, если host уже передал конкретный device context.

`PF_GPUDeviceInfo` содержит platform/device/context/queue pointers. Они host-owned. Не уничтожайте их через native API платформы как свои объекты.

## 3. Per-device state

`PF_GPUDeviceSetupOutput::gpu_data` — effect-owned pointer, который потом приходит в setdown с требованием effect dispose.

Хорошая модель:

```text
one immutable/global algorithm description
+ per-device compiled kernels/pipelines
+ per-render transient buffers
```

Не храните один CUDA/Metal/OpenCL/DirectX context как глобальный singleton без привязки к device index.

Bundled `SDK_Invert_ProcAmp` создаёт framework-specific state в GPU_DEVICE_SETUP и маршрутизирует отдельный SMART_RENDER_GPU path.

## 4. PF_GPUDeviceSuite1: ownership

Текущий suite документирует пары:

- AllocateDeviceMemory → FreeDeviceMemory;
- AllocateHostMemory → FreeHostMemory;
- CreateGPUWorld → DisposeGPUWorld.

Только созданные самим plug-in GPU worlds plug-in имеет право Dispose.

Suite comments рекомендуют device allocations делать через host suite; purge рассматривается как emergency path, а не обычный allocator.

## 5. Exclusive device access

Suite имеет Acquire/ReleaseExclusiveDeviceAccess. Но comment отдельно говорит, что для full GPU plug-ins с отдельным GPU render entry point exclusive access уже удерживается host.

Не добавляйте лишний lock вокруг любого GPU selector «на всякий случай». Сначала определить, какой execution model используется.

## 6. Pixel format GPU path

Bundled sample проверяет `PF_PixelFormat_GPU_BGRA128` в GPU Smart Render и использует 16 bytes/pixel.

Из этого можно говорить о конкретном sample path, но не о том, что любой GPU effect обязан принимать только этот формат во всех будущих SDK.

Нужно проверять актуальный pixel-format contract для каждого supported SDK/host.

## 7. Pre-render решает применимость GPU

Sample выставляет:

```text
PF_RenderOutputFlag_GPU_RENDER_POSSIBLE
```

в pre-render.

В production этот флаг должен зависеть от реальной возможности выполнить текущий кадр:

- текущие параметры;
- доступный backend;
- поддерживаемый pixel format;
- нужные resources;
- известные fallback conditions.

Не заявляйте GPU possible, если далее обязательно вернёте unsupported path.

## 8. CPU reference обязателен

CPU implementation должна быть:

- правильной;
- deterministic;
- отдельно тестируемой;
- достаточно простой, чтобы служить oracle для GPU.

GPU backend не должен тихо иметь другую clamp, alpha или HDR policy.

## 9. CPU ↔ GPU correctness

До benchmark определить tolerance и сравнивать минимум:

- 32-bpc float основной GPU path;
- alpha 0 / partial / 1;
- negative и >1 HDR values;
- extreme params;
- tiny/odd dimensions;
- non-zero origins/ROI;
- edge pixels;
- repeated renders;
- MFR on/off там, где feature поддерживается;
- fallback when backend/device unavailable.

Не подбирайте tolerance после того, как увидели расхождение.

## 10. Backend-specific compilation

Bundled sample содержит CUDA, OpenCL, DirectX и Metal branches, но source presence не означает, что все они собираются в любой конфигурации.

Для каждой shipping platform нужно отдельно фиксировать:

```text
toolchain
kernel source/binary generation
runtime dependency
host framework selection
artifact contents
actual device test
```

## 11. Device loss / allocation failure

Минимальный error-path test:

- setup compilation failure;
- GPU allocation failure;
- unsupported framework;
- unsupported pixel format;
- intermediate world creation failure;
- render cancellation;
- setdown after partial setup.

Каждый успешно созданный resource должен иметь определённый release path даже после поздней ошибки.

## 12. Performance measurement

Профилировать отдельно:

- CPU preparation;
- host↔device transfer;
- kernel compile/warmup;
- dispatch;
- kernel time;
- intermediate allocations;
- synchronization;
- readback.

«GPU быстрее» без размера кадра, backend, device, warm/cold state и transfer cost — не benchmark.

## Verification boundary

## Один backend: маршрут Metal sample

Source-level walkthrough SDK 25.6 `Effect/SDK_Invert_ProcAmp`: открыть основной
dispatcher, `SDK_Invert_ProcAmp_Kernel.cl`, GPUUtils и Mac project **вместе**.
Mac CustomBuild preprocesses shared kernel с `GF_DEVICE_TARGET_METAL=1`, затем
`GPUUtils/CreateCString.py` создаёт embedded `.metal.h`; это не отдельный checked-in
`.metal` файл. Project содержит старый hardcoded clang3.5 include path и `python`;
их доступность требует review, наличие проекта не доказывает modern Xcode build.
Device setup создаёт
effect pipeline state для предоставленного host device; pre-render объявляет
eligibility данного запроса; GPU render проверяет GPU world format, передаёт pitch,
dimensions и coefficients kernel; setdown уничтожает только effect-owned state.
Host queue/device/context и borrowed worlds не dispose-ятся плагином.

| Условие | Policy до GPU commitment | После начала GPU render |
|---|---|---|
| Backend не реализован | Не обещать GPU possible | Вернуть explicit error, не CPU-cast GPU pointer |
| Frame feature не поддерживается | CPU route через корректную pre-render eligibility | Не выдать partial pixels как успех |
| Allocation/pipeline failure | Удалить partial owned resources | Preserve error, cleanup; host retry не предполагать |
| Format отличается от expected | Не угадывать layout | Reject по contract |
| Cancel/device failure | Снять eligibility лишь для будущих requests | Завершить backend work по его правилам, не free in-flight buffers |

CPU fallback — спроектированный маршрут host negotiation, не обещание, что AE
повторит любой failed GPU render на CPU. Synchronization и buffer lifetime брать
из конкретного backend sample/API; одинаковое имя queue не гарантирует завершение
dispatch. Log actual selector/framework/device/format/route для attribution.
Настройка проекта «GPU» и существование Metal kernel не доказывают его исполнение.
Throughput считать с preparation/transfer/sync, не одним kernel timestamp.

Текст сверён с SDK/source sample. Bible не заявляет собственный GPU runtime result; сборка demo binary не является условием редакционной готовности главы.
