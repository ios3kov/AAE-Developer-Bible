# macOS — installation and packaging

Development install, product install and delivery packaging are separate concerns.

## Worked upgrade/rollback design (NOT_RUN)

Example own product `BibleGain.plugin`, not Adobe Skeleton installed under a new
filename with its old match identity. Resolve intended scope/path below; close AE
and compatible Adobe hosts before replacing loaded code. Package manifest lists
only this product bundle plus its identifier/version and hashes; user presets and
license state are not payload files.

1. Stage signed/notarized candidate outside live discovery directories; verify
   signature and expected bundle identity/hash. Archive prior owned bundle and
   its manifest in backup outside discovery. A second live backup bundle risks
   duplicate match-name discovery.
2. Refuse conflicting unmanaged destination, symlink escape or unexpected prior
   hash; never delete all MediaCore to resolve a collision.
3. Copy candidate to a sibling staging location outside discovery, preserve bundle
   permissions, verify copy, then perform controlled same-volume replacement.
   Journal each transition; filesystem rename does not make the entire installer atomic.
4. Launch exact supported AE, verify loaded path/UUID and smoke fixture. On failure
   close host, restore prior owned bundle/manifest, verify restored bytes and record
   rollback result separately. A failed smoke test remains failed after rollback.
5. Uninstall only manifest-owned unmodified files. If bytes changed unexpectedly,
   stop/report conflict rather than erasing another installation. Keep user data
   according to separately declared policy.

Expected record: candidate hash → installed hash → loaded UUID → smoke outcome;
if rollback, old hash → restored hash and separate recovery outcome. All observations
here are NOT_RUN; see [worked evidence pack](../13-TEMPLATES/examples/WORKED-EXAMPLE.md).

## Development location

The AE SDK guide recommends the per-user MediaCore path during development:

    ~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/

This avoids writing Xcode output directly into the root-owned system Library path.

## Common release location

For plug-ins intended for compatible Adobe video hosts, the documented common location is:

    /Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/

The 7.0 directory is the historical CC convention.

A plug-in placed here may also be discovered by other compatible Adobe hosts. That is useful only if the plug-in is actually compatible with those hosts.

## AE-specific location

If the product depends on After Effects-only suites or behavior, the app-specific path remains available:

    /Applications/Adobe After Effects [version]/Plug-ins/

This path is version-specific and creates more installer maintenance when multiple AE versions are supported.

Do not install into every detected host blindly. Decide product host policy first.

## Package choices

Common delivery patterns:

- signed/notarized PKG installer;
- DMG containing installer or documented manual-install payload;
- ZIP only when manual installation is an explicit supported product choice.

The package format should support the required permissions, upgrade semantics and uninstall policy.

## Installer ownership model

Maintain an explicit manifest of files owned by the installer.

Installer may own:

- native plug-in bundle;
- helper binary;
- shared product resources;
- receipt/version metadata.

Installer must not delete:

- user projects;
- user presets unless explicitly product-owned and removable;
- unrelated plug-ins;
- entire shared Adobe directories;
- license/user data unless uninstall policy explicitly asks and the user agrees.

Never implement uninstall as "delete parent folder" when that folder can contain third-party/user files.

## Upgrade

Define upgrade from at least the previous supported release.

Test:

~~~text
N-1 installed
→ install N
→ old binary removed/replaced correctly
→ user data preserved
→ AE loads only intended version
→ rollback plan still exists
~~~

If filenames/bundle IDs change, explicitly remove only the old product-owned artifact.

## Multiple AE versions

If using common MediaCore, one installed binary may be loaded by several Adobe host versions.

Therefore compatibility is a property of the installed binary, not just the installer UI.

If the plug-in is AE-version-specific, prefer a design that cannot accidentally expose an incompatible build to another host/version.

## Atomicity

Install into a staging location first when possible, validate payload, then perform the final privileged copy.

Avoid leaving half-copied bundles when install fails.

A plug-in bundle must be treated as one versioned artifact.

## Signing and notarization order

For a PKG-based release:

~~~text
build final plug-in
→ sign plug-in/nested code
→ verify
→ construct installer payload
→ sign installer
→ notarize distributable
→ staple where applicable
→ verify clean install
~~~

Do not modify signed nested plug-in contents during installer generation.

## Installer logs

Log:

- product version/build;
- target path;
- previous version detected;
- files installed/removed;
- signature/notarization preflight result where useful;
- success/failure code.

Do not log secrets or license tokens.

## Required tests

- fresh install;
- upgrade;
- uninstall;
- reinstall after uninstall;
- multiple AE versions;
- no AE installed;
- insufficient permissions;
- disk-full/error injection where practical;
- Unicode user/product paths for user-side assets;
- quarantine/Gatekeeper path;
- AE launch and plug-in load after install.

## Verification boundary

The paths follow current AE SDK installer guidance. A correct path alone does not prove a safe installer. Clean-machine install/upgrade/uninstall verification belongs to a concrete product's release evidence, not to Bible editorial completion.
