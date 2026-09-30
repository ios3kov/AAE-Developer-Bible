# Crash diagnostics

## Every build needs identity

Минимум:
- semantic version;
- internal build number;
- git SHA;
- platform/arch;
- build timestamp or reproducible build ID;
- SDK generation.

## macOS bundle

Хранить exact `.dSYM` release artifact.

Crash ticket:
- `.ips`/crash report;
- AE build;
- OS;
- architecture;
- project;
- repro;
- GPU/MFR state.

## Windows

Хранить exact PDB.

Crash ticket:
- dump;
- AE build;
- Windows build;
- CPU/GPU/driver;
- project;
- repro;
- GPU/MFR.

## Triage classification

1. load/init crash;
2. params/UI event crash;
3. render CPU;
4. render GPU;
5. MFR race;
6. project serialization/migration;
7. third-party dependency;
8. host-only reproducible without plug-in modification.

Если bug воспроизводится unmodified Adobe sample при тех же условиях — это важный сигнал для отделения SDK/host issue от собственного кода.
