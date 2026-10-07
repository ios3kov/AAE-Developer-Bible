# Windows — installation and packaging

A Windows plug-in installer must resolve Adobe's supported install paths, own only its files, handle upgrades deterministically and preserve signed payload integrity.

## Common Adobe plug-in path

## Worked upgrade/rollback design (NOT_RUN)

Example product-owned `BibleGain.aex` + matching private PDB archive (PDB is not
automatically customer payload). Resolve destination through registry guidance
below with explicit registry view/scope. Close AE and all hosts loading the common
plug-in before replacement; locked-file failure is not permission to kill processes.

1. Verify candidate Authenticode and package manifest hashes; stage outside live
   discovery. Archive prior owned binary/manifest outside MediaCore so duplicate
   effects are not discovered.
2. Reject unmanaged name collision, unexpected prior hash or path/reparse-point
   escape; elevate only for the selected installation scope, not for arbitrary paths.
3. Journal backup/copy/verification transitions; copy to staging on target volume,
   verify hash, replace only named owned files. For MSI use actual installer rollback
   semantics; this design is not a ready MSI implementation.
4. Launch exact AE; record loaded module path, matching build/symbol identity and
   smoke outcome. On failure close host and restore old bytes/manifest. Record failed
   candidate and rollback separately; successful recovery does not turn smoke PASS.
5. Uninstall only owned files whose identity still matches. Preserve presets/user
   settings/licenses per product policy; changed files produce a visible conflict.

Expected evidence: registry value/view → chosen path → candidate/installed hashes
→ loaded module → smoke result; upgrade adds prior/restored hashes and recovery
status. Execution is NOT_RUN; [worked pack](../13-TEMPLATES/examples/WORKED-EXAMPLE.md).

The AE SDK installer guidance documents the common path through the registry:

    HKLM\SOFTWARE\Adobe\After Effects\[version]\CommonPluginInstallPath

For AE-specific installation it also documents the corresponding PluginInstallPath value.

Do not derive production destinations only from a guessed Program Files string.

## Development path is not installer policy

The common development path:

    C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\

is useful while developing.

A production installer should use Adobe's registry guidance so it follows the installed host configuration instead of an assumption.

## 32-bit vs 64-bit registry view

Installer code must deliberately use the appropriate registry view for the target application/OS.

Do not let installer technology defaults redirect a lookup into a different registry view and then conclude that After Effects is not installed.

Log which key/view was queried.

## Installer technology

Possible implementations:

- MSI/WiX;
- signed bootstrapper;
- Inno Setup or another mature installer system.

Technology is less important than correct semantics:

- privileged copy;
- architecture selection;
- upgrade;
- rollback;
- repair;
- uninstall;
- logging;
- signed payload preservation.

## File ownership manifest

The installer should know exactly which files belong to the product.

Never recursively delete a shared Adobe plug-in directory.

Uninstall should remove:

- product-owned .aex;
- product-owned DLL/helper files;
- product-owned receipts/metadata.

User-created presets/config/license data require a separate explicit policy.

## Architecture selection

If both x64 and ARM64 payloads exist:

~~~text
detect supported host/machine architecture
→ choose intended payload
→ log decision
→ install only supported architecture/layout
→ verify installed binary architecture
~~~

Upgrade must correctly replace the previously installed architecture.

## Atomic install

Prefer staging and validation before final copy.

A failed install should not leave:

- half-copied .aex;
- mixed old/new DLLs;
- unsigned replacement next to signed old binary;
- orphaned architecture payloads.

If installer technology supports transactional rollback, test it.

## Upgrade

Required scenario:

~~~text
N-1 installed
→ N installer starts
→ detect old files/version
→ stage N
→ replace owned payload
→ preserve user data
→ verify
→ commit
~~~

If product filenames changed, explicitly remove the old owned file. Do not rely on directory cleanup.

## Installer signing

Sign executable payload and installer according to the Windows signing chapter.

Do not extract signed files, patch them, then install the modified copies.

## Runtime dependencies

Decide whether dependencies are:

- statically linked;
- product-local DLLs;
- installed through a Microsoft runtime prerequisite;
- another documented system dependency.

Do not make release success depend on whatever Visual Studio happened to install on the developer machine.

## Required tests

- fresh install;
- upgrade N-1 -> N;
- repair if supported;
- uninstall;
- reinstall;
- multiple AE versions;
- no AE installed;
- no admin rights;
- x64 and ARM64 decision;
- corrupted payload/checksum;
- locked file because AE is running;
- Unicode/long user paths for user-side data;
- antivirus/SmartScreen interaction;
- clean AE launch/load after install.

## AE-running policy

Define what happens if After Effects is running while replacing the plug-in.

Safe policies include:

- block install and ask user to close AE;
- schedule replacement only with a well-tested installer mechanism.

Do not silently overwrite a loaded module and report success without verifying the final on-disk state.

## Logs

Record:

- installer/product version;
- host versions detected;
- registry paths resolved;
- architecture selected;
- old version;
- files installed/removed;
- terminal result/error code.

Do not log license secrets.

## Verification boundary

Registry path guidance is documented by the AE SDK guide. Bible documents the Windows installer matrix; executing that matrix is product release evidence, not a completion requirement for the documentation.
