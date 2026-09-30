# macOS — GPU development

## Principle

Mac GPU backend не должен диктовать effect semantics. Один algorithm contract → CPU oracle + Mac GPU backend.

## SDK sample setup

Current After Effects GPU build guide для SDK sample указывает Boost dependency для processing kernel files и Xcode custom path `BOOST_BASE_PATH`.

Не переносить sample dependency blindly в собственную архитектуру: сначала понять, какая часть toolchain реально нужна вашему backend.

## Apple Silicon

На Apple Silicon учитывать:
- unified memory не отменяет synchronization/correctness costs;
- arm64 CPU reference может иметь другую floating-point performance, но semantics должны совпадать;
- third-party GPU/native libs должны поддерживать arm64;
- Universal release не может содержать Intel-only helper binary.

## Test matrix

- Apple Silicon low/mid/high GPU classes available to team;
- 8/16/32-bpc;
- MFR + GPU simultaneously;
- GPU fallback to CPU;
- sleep/wake + relaunch;
- project reopen;
- extreme resolution.

## Profiling

Разделять:
- host checkout cost;
- buffer preparation;
- GPU dispatch;
- synchronization;
- kernel time;
- copy/readback;
- teardown.

Если «GPU effect медленный», без такой декомпозиции вывод бессмысленен.
