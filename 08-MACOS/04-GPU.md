# macOS — GPU development

Эта глава описывает platform-specific слой GPU effect development на macOS.

Общая Effect/GPU lifecycle-модель находится в [GPU effects](../02-EFFECT-PLUGINS/05-GPU.md). Здесь — то, что меняется именно из-за macOS, Apple Silicon, Metal, bundle layout и Xcode/toolchain.

Используйте датированный [host/renderer snapshot](../00-START-HERE/02-ENVIRONMENT-MATRIX.md#host-snapshot-2026-10-08)
для разделения общих требований AE, Advanced3D и известных проблем конкретных
конфигураций. Старое требование renderer не снижает минимум текущего host.

## Главный принцип

Mac GPU backend не должен определять effect semantics.

Правильная архитектура:

```text
Effect parameter/state contract
        ↓
pure render intent
   ┌────┴────┐
   │         │
 CPU       Metal
oracle     backend
```

CPU и Metal могут иметь разную реализацию, но alpha policy, HDR policy, coordinate system, edge behavior, parameter meaning и ROI semantics должны быть согласованы.

## Host выбирает GPU context

### SDK25.6 concrete source route (execution NOT_RUN)

Начать с `Examples/Effect/SDK_Invert_ProcAmp/Mac/SDK_Invert_ProcAmp.xcodeproj`
в copied Examples tree. Читать dispatcher/device setup вместе с shared
`SDK_Invert_ProcAmp_Kernel.cl` и GPUUtils: Mac custom build preprocesses kernel
с `GF_DEVICE_TARGET_METAL=1`, затем CreateCString.py создаёт embedded `.metal.h`.
Отдельного checked-in `.metal` это не требует. Старый hardcoded clang3.5 Metal
include path и invocation `python` требуют adaptation/review под installed toolchain;
source presence не гарантирует successful modern Xcode build.

Для подтверждения route поставить breakpoints на dispatcher GPU selectors и
device-setup/render functions sample; записать фактический framework/device index,
формат worlds и setup result. CPU render hit при выбранной GPU project setting
не является GPU test. Unsupported format/framework и setup failure проверять
отдельно по [failure policy](../02-EFFECT-PLUGINS/05-GPU.md), не принуждать host
исполнять GPU callback с CPU pointers. Device selection не заменять global default.
Debug attribution/logging build и ordinary timing build — отдельные artifacts.

В GPU selector path After Effects передаёт framework/device context. Не выбирайте самостоятельно «первую GPU» или отдельный global Metal device, если host уже дал нужную device identity/context.

## Apple Silicon

Unified memory не означает отсутствие synchronization cost. Остаются command scheduling, resource lifetime, hazards, transient allocations и completion/wait costs.

Не используйте «zero copy» как автоматический performance claim.

## Per-device state

Хорошая модель:

```text
global immutable algorithm metadata
+ per-device Metal pipelines/resources
+ per-render transient resources
```

Per-device state должен создаваться в соответствующем setup lifecycle, быть привязан к host-provided device identity и корректно уничтожаться в setdown.

Не храните mutable per-frame state в одном global object, если renders могут пересекаться.

## Metal resources

Для product-owned Metal objects документируйте:

- кто создаёт;
- кто владеет;
- когда освобождает;
- можно ли reuse между frames;
- нужен ли explicit synchronization;
- что происходит при setup failure.

Host-owned objects не уничтожаются как product-owned.

## SDK sample toolchain

Adobe GPU sample/toolchain может использовать дополнительные build dependencies и helper processing для shader/kernel assets.

Правило: sample build plumbing — источник понимания, а не обязательная архитектура вашего продукта.

Перед копированием dependency выясните, нужна ли она вашему backend, используется ли только build-time, входит ли runtime dependency в bundle и поддерживает ли architecture policy продукта.

## Apple Silicon + Intel support

Если продукт заявляет Universal support, main plug-in binary, nested dylibs/frameworks, helper executables и generated native libraries должны поддерживать заявленные slices.

Один Intel-only helper делает Universal bundle функционально не-Universal.

## CPU oracle

CPU path полезно держать как correctness reference. Он должен быть deterministic, отдельно тестируемым и достаточно простым для анализа расхождений.

GPU backend не должен становиться «новой математикой».

## Float behavior

CPU/Metal различия могут возникать из-за FMA, fast math, precision, denorm handling и order of operations. Поэтому tolerance задаётся до сравнения результатов.

## ROI and origins

GPU kernel не должен предполагать `origin = 0`, full-frame buffer или full-comp width. SmartFX/host может дать partial region.

Coordinate transform должен учитывать host-provided origin/rect/layout.

## MFR + GPU

MFR и GPU — два разных concurrency layers. Проверяйте per-frame mutable state, per-device shared state, resource pools, lazy initialization и cleanup.

Плохая модель — один mutable global Metal buffer, используемый всеми frames.

## Failure policy

Продумайте:

- pipeline creation failure;
- unsupported device/framework;
- allocation failure;
- partial setup;
- render cancellation;
- setdown after failed setup.

Если product обещает CPU fallback, заранее определите, какие capability/eligibility
отказы позволяют не выбирать GPU path. Ошибка уже начатого GPU render не означает,
что host автоматически повторит кадр на CPU. Не передавайте GPU worlds в CPU
итератор и не подменяйте ошибку fabricated success. Cleanup и returned error следуют
точному callback contract; retry/fallback требует отдельно подтверждённого маршрута
из [канонической failure policy](../02-EFFECT-PLUGINS/05-GPU.md).

## Debugging

Разделяйте setup, dispatch, correctness и lifetime failures. Wrong output и crash — разные классы проблемы.

## Profiling

Профилируйте отдельно:

- CPU parameter/preparation;
- host checkout;
- allocation;
- command encoding;
- dispatch;
- kernel execution;
- synchronization;
- readback;
- cleanup.

«GPU slow» без этой декомпозиции ничего не объясняет.

## Cold vs warm behavior

Отделяйте first render, pipeline/kernel warmup, steady-state render, project reopen и app relaunch.

## Product test matrix

Для продукта полезно покрыть 8/16/32-bpc paths, alpha, HDR, odd/tiny/large sizes, non-zero origins/ROI, MFR on/off, GPU unavailable fallback и repeated renders.

Bible описывает эту матрицу; сама Bible не обязана запускать её для source examples.

## Performance architecture

Избегайте shader recompilation every frame, unconditional intermediate allocations, immediate blocking waits и full-frame work при маленьком ROI.

Но не оптимизируйте до определения correctness contract.

## Release packaging

GPU assets/resources должны попасть в bundle, иметь controlled relative paths и не изменяться после signing.

## Related chapters

- [GPU effects](../02-EFFECT-PLUGINS/05-GPU.md)
- [Universal binary](02-UNIVERSAL-BINARY.md)
- [macOS debugging](03-DEBUGGING.md)
- [Signing/notarization](05-SIGNING-NOTARIZATION.md)
- [CPU/GPU equivalence recipe](../12-RECIPES/04-CPU-GPU-EQUIVALENCE.md)

## Evidence boundary

GPU lifecycle/contracts в core chapter SDK/source-reviewed. Эта глава — platform architecture/testing guidance; конкретный Mac GPU runtime result заявляется только если есть отдельная запись evidence.
