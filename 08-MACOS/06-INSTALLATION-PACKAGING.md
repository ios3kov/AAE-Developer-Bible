# macOS — installation and packaging

Development install, product install and delivery packaging are separate concerns.

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

The paths follow current AE SDK installer guidance. A correct path alone does not prove a safe installer. Full clean-machine install/upgrade/uninstall verification remains an open completion gate.
