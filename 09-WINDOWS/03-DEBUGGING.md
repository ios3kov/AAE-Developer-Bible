# Windows — debugging

## Visual Studio launch

Настроить project Debugging:
- Command → `AfterFX.exe` нужной версии;
- Working Directory → directory host-а;
- plug-in output/copy step → dev MediaCore path.

Путь к AfterFX.exe не зашивать в shared project навечно: использовать local property sheet/env variable.

## Attach

Можно:
1. запустить AE;
2. Visual Studio → Attach to Process → AfterFX.exe;
3. убедиться, что symbols для вашего `.aex` loaded.

## PDB discipline

Для каждого release:
- PDB сохраняется;
- binary hash/version фиксируется;
- PDB не заменяется новым build под тем же version label.

## Crash dump

При user crash запрашивать:
- exact plug-in version/build;
- AE version/build;
- Windows build;
- CPU architecture;
- GPU + driver;
- dump/crash report;
- project/repro steps;
- MFR/GPU state.

Debugging без matching PDB часто превращается в угадывание.

## Tools

По необходимости:
- Visual Studio debugger;
- WinDbg for dumps;
- Application Verifier/sanitizer-like tooling where compatible;
- GPU vendor/profiling tools;
- ETW/perf tools for contention/IO.
