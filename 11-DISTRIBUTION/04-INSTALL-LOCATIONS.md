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

    %AppData%\Adobe\CEP\extensions

CEP runtime/version and signing/debug-mode policy still apply. A directory existing does not prove the host accepts the package.

## UXP

After Effects UXP is in a transition period in this 2026 snapshot. Do not invent AE UXP install paths from another Adobe host.

AE-specific documentation is already published (landing reread 2026-10-07);
publication is not installed beta/GA evidence. Follow exact AE-specific packaging/
install contracts for the chosen host/runtime; this cheat sheet does not invent a
cross-host UXP filesystem location. See [transition boundary](../07-PANELS/02-UXP-TRANSITION.md)
and the [shared packaging/install workflow](../07-PANELS/04-UXP-PLATFORM.md).

## Common vs AE-specific policy

Prefer common MediaCore only when the plug-in can safely be discovered by other compatible Adobe video hosts.

Use AE-specific placement when the product depends on After Effects-only suites/behavior and discovery by another host would be misleading or unsafe.

**PPro/AME discovery — DOCUMENTED, review 2026-10-08.**
[Pinned installation note](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/plug-in-installation.md)
предупреждает: установка только в каталог Premiere Pro не обеспечивает рендер эффекта
в отдельном процессе Adobe Media Encoder. Для заявленного общего маршрута нужен
подходящий common payload, включая его зависимости. По
[installer guide](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/intro/where-installers-should-put-plug-ins.md)
PPro не обходит macOS aliases и Windows shortcuts. Символическая ссылка или alias
не заменяют подтверждённое размещение; правила одного host не переносить на другой.

**Разные preview assets.** Историческая
[Premiere Elements page](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/ppro/premiere-elements.md)
описывает иконку 60×45 PNG с именем `AE.<match-name>.png`. Это не новая схема
PPro Beta27 preview: в [PiPL chapter](../01-ARCHITECTURE/03-PIPL-AND-LOADING.md)
она привязана к имени binary. Не переносить размеры, filename key или destination
между этими двумя host-контрактами; старый Elements path не объявляет поддержку
современного выпуска Elements.

## Installer rules

Native installer path guide reread 2026-10-07; CEP paths retain dated platform
source review. Concrete owned-file upgrade/conflict/rollback designs:
[macOS](../08-MACOS/06-INSTALLATION-PACKAGING.md),
[Windows registry/view](../09-WINDOWS/06-INSTALLATION-PACKAGING.md).
Path existence is not discovery or permission evidence; no installer executed here.

Regardless of path:

- resolve documented platform/registry path;
- verify destination before privileged copy;
- install only product-owned files;
- never recursively clean a shared Adobe directory;
- log final path/version;
- test upgrade/uninstall;
- verify the installed signed binary, not only the source package.

## Verification boundary

Пути — документированная схема размещения. Разработчик продукта подтверждает
discovery, permissions и поведение своего installer для заявленной среды;
эта глава не заявляет нового install/host результата Библии.
