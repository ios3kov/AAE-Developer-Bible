# Install locations cheat sheet

Paths below are routing guidance, not permission to blindly copy into every Adobe directory.

## Native C++ — macOS development

AE SDK recommended per-user development path:

    ~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/

Use this for normal Xcode development to avoid writing build output into the root-owned system Library.

## Native C++ — macOS common release

Common MediaCore:

    /Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/

Use when the plug-in is intended to be available to compatible Adobe video hosts.

The historical CC version directory remains 7.0.

## Native C++ — macOS AE-specific

    /Applications/Adobe After Effects [version]/Plug-ins/

Use only when product policy intentionally targets a specific AE installation/version.

## Native C++ — Windows development

Typical SDK development output:

    C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\

Adobe sample projects also support AE_PLUGIN_BUILD_DIR for the development output path.

Do not turn this hardcoded development path into installer logic.

## Native C++ — Windows release

Resolve the common install path through Adobe's registry guidance:

    HKLM\SOFTWARE\Adobe\After Effects\[version]\CommonPluginInstallPath

AE-specific path is available through the corresponding PluginInstallPath value.

Installer must deliberately use the correct registry view.

## CEP — macOS

System:

    /Library/Application Support/Adobe/CEP/extensions

User:

    ~/Library/Application Support/Adobe/CEP/extensions

## CEP — Windows

System:

    C:\Program Files (x86)\Common Files\Adobe\CEP\extensions

User:

    %AppData%\Roaming\Adobe\CEP\extensions

CEP runtime/version and signing/debug-mode policy still apply. A directory existing does not prove the host accepts the package.

## UXP

After Effects UXP is in a transition period in this 2026 snapshot. Do not invent AE UXP install paths from another Adobe host.

When AE UXP public beta/GA documentation is available, follow the AE-specific packaging/install workflow and update this chapter with a dated source.

## Common vs AE-specific policy

Prefer common MediaCore only when the plug-in can safely be discovered by other compatible Adobe video hosts.

Use AE-specific placement when the product depends on After Effects-only suites/behavior and discovery by another host would be misleading or unsafe.

## Installer rules

Regardless of path:

- resolve documented platform/registry path;
- verify destination before privileged copy;
- install only product-owned files;
- never recursively clean a shared Adobe directory;
- log final path/version;
- test upgrade/uninstall;
- verify the installed signed binary, not only the source package.

## Verification boundary

These paths follow current AE SDK/CEP guidance. Host discovery, permissions and installer behavior still require actual clean-machine tests.
