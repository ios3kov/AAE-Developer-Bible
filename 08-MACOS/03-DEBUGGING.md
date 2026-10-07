# macOS — debugging After Effects plug-ins

Source/version boundary checked **2026-10-04**: [macOS debugger guide](https://ae-plugins.docsforadobe.dev/intro/debugging-ae-macos/). Non-Beta 26.5+ and Beta 2027+ are distinct later-version guide statements; no attach run on an installed build is claimed. [Review](../BLOCK-5-REVIEW-2026-10-04.md).

## Normal workflow

- Xcode scheme executable → After Effects;
- breakpoints в plug-in;
- Build & Run или Debug → Attach to Process;
- plugin binary копируется в dev MediaCore folder.

## macOS 15+ unsigned plug-ins

Current SDK Guide указывает, что macOS 15+ не загружает unsigned plug-ins в обычном dev flow. Для development можно применять ad-hoc signing после build:

```bash
codesign --force --deep --sign - "/path/to/MyPlugin.plugin"
```

Для release этого недостаточно — см. signing/notarization.

## AE 26.5+ non-Beta debugger restriction

Current After Effects SDK Guide описывает отдельную проблему: debugger attach к официальной non-Beta/LTS сборке на macOS начиная с AE 26.5 может блокироваться code signing.

Рекомендованный dev workflow:
1. сделать **development copy** installation folder AE;
2. извлечь entitlements;
3. добавить `com.apple.security.get-task-allow = true`;
4. re-sign development copy ad-hoc;
5. запускать и debug только эту копию.

Не модифицировать production AE installation, используемую для обычной работы/QA.

## AE Beta 2027+

SDK Guide сообщает новый developer-mode path для official Beta builds 2027+.

Machine-level marker:

```bash
sudo mkdir -p "/Library/Application Support/Adobe/After Effects (Beta)"
sudo touch "/Library/Application Support/Adobe/After Effects (Beta)/developer-mode"
```

После этого attach выполняется через Xcode или `lldb -p <pid>`.

Поскольку это version-sensitive поведение, перед использованием сверять текущую страницу SDK Guide.

## Crash investigation

Сохранять:
- exact plug-in build id;
- AE version/build;
- macOS version;
- architecture;
- crash report;
- symbolicated stack;
- minimal project;
- MFR/GPU state.

Без exact `.dSYM` shipped build symbolication может быть бесполезна.


## Loaded-image identity lesson

### Concrete LLDB breakpoint route

После version-appropriate launch/attach (не изменяя рабочую AE installation):

```text
(lldb) image list -v
(lldb) image lookup -n EffectMain
(lldb) breakpoint set --name EffectMain
(lldb) continue
(lldb) frame variable cmd
(lldb) thread backtrace
```

Применить конкретный effect/запросить кадр. Expected observations: named plugin
image path/UUID в image list; lookup разрешает exported dispatcher; breakpoint
показывает actual PF_Cmd. Optimized build может скрывать variable — это symbol/
optimization limit, не доказательство отсутствия cmd. Если breakpoint unresolved,
проверить loaded image и matching dSYM (`dwarfdump --uuid` для binary/dSYM), затем
export/resource/discovery; не брать случайный dSYM с тем же filename.

Для AEGP entry ставить breakpoint до launch, поскольку attach после загрузки
пропускает initializer; позднее command hook можно остановить при menu click.
Code signing attach denial относится к host policy, не к корректности entrypoint.
Этот walkthrough документирован, LLDB/AE execution здесь NOT_RUN.

The [AE Hot Loader reuse audit](../22-PROJECT-CASE-STUDIES/REUSE-AUDIT-2026-10-01.md) preserves a concrete debugging lesson: installation intent is not proof of the module AE actually loaded. When diagnosing path/version mismatches, record the **real loaded image path and identity** before reasoning from an installer destination.

The source project used macOS dyld enumeration for an experiment. Treat that as a platform diagnostic technique, not a cross-platform After Effects SDK contract.
