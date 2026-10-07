# macOS — signing and notarization

macOS has two different concerns:

1. code signing establishes identity/integrity;
2. notarization submits the distributable software to Apple's notary service and produces a ticket recognized by Gatekeeper.

For a commercial external release, treat both as release gates.

## Development signing

Ad-hoc signing is suitable for local development and load testing:

~~~bash
codesign --force --deep --sign - "/path/to/MyPlugin.plugin"
~~~

The AE SDK guide currently notes that macOS 15+ prevents loading unsigned plug-ins, making a development signing step important.

Ad-hoc signing is not the release trust model.

## Release identity

### Конкретный PKG маршрут (commands, NOT_RUN)

Пример — собственный staged `BibleGain.plugin`, не vendor Skeleton с неизменённым
match name. `STAGE`/`OUT` — подготовленные product-owned directories;
`APP_ID`/`INSTALLER_ID` — точные identity strings из вашего Keychain,
`NOTARY_PROFILE` — заранее сохранённые credentials. Placeholders не сертификаты.
Вложенный code, если он есть, подписать явно inside-out до outer bundle:

```bash
security find-identity -v -p codesigning
codesign --force --timestamp --sign "$APP_ID" "$STAGE/BibleGain.plugin"
codesign --verify --deep --strict --verbose=2 "$STAGE/BibleGain.plugin"
codesign -d --verbose=4 "$STAGE/BibleGain.plugin"
pkgbuild --component "$STAGE/BibleGain.plugin" \
  --install-location '/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore' \
  --identifier com.example.biblegain.pkg --version 1.0.0 \
  --sign "$INSTALLER_ID" "$OUT/BibleGain.pkg"
pkgutil --check-signature "$OUT/BibleGain.pkg"
xcrun notarytool submit "$OUT/BibleGain.pkg" \
  --keychain-profile "$NOTARY_PROFILE" --wait --output-format json
```

Проверить actual TeamIdentifier/Authority, bundle identity и отсутствие debug
entitlements. `pkgbuild --component` — учебная single-bundle упаковка, не реализация
owned-file upgrade/rollback. Общий MediaCore destination допустим только при
соответствующей host policy; AE-only product выбирает version-specific destination.
Helpers/app/CLI Hardened Runtime и entitlement requirements проверять отдельно;
подпись plug-in не меняет права host.

Из returned JSON сохранить submission ID в `SUBMISSION_ID`; требовать `Accepted`,
а не только успешную отправку/exit. Затем:

```bash
xcrun notarytool log "$SUBMISSION_ID" --keychain-profile "$NOTARY_PROFILE" "$OUT/notary-log.json"
xcrun stapler staple "$OUT/BibleGain.pkg"
xcrun stapler validate "$OUT/BibleGain.pkg"
spctl --assess --type install --verbose=4 "$OUT/BibleGain.pkg"
shasum -a 256 "$OUT/BibleGain.pkg"
```

Читать log даже при Accepted. Зафиксировать submitted hash отдельно от final
stapled hash. Signature/notary/stapler/assessment failures останавливают promotion;
эти команды не подтверждают AE load, offline install или rollback. ZIP нельзя
staple напрямую: staple supported contained items и заново создать delivery ZIP,
сохранив обе identities. Custom third-party/network installers требуют отдельного
review payload/installer notarization, не автоматически этого single-PKG маршрута.

Источник перепрочитан **2026-10-07**: [Apple custom workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow)
(официальный DocC data endpoint): signed flat PKG/UDIF/ZIP submissions, log on
success, supported stapling и ZIP limitation. Signing/submission здесь NOT_RUN.

Apple's distribution documentation uses Developer ID for software distributed outside the Mac App Store.

Depending on what you ship, release artifacts can include:

- Developer ID Application-signed plug-in/helper binaries;
- Developer ID Installer-signed installer packages;
- a notarized ZIP, DMG or PKG delivery artifact.

Choose the exact certificate type for the artifact being signed.

## Sign only final contents

Signing establishes integrity. Any later content mutation can invalidate the signature.

Correct order:

~~~text
compile
→ copy runtime resources
→ embed final dependencies
→ strip only if intended
→ finalize Info.plist/resources
→ sign nested code
→ sign outer plug-in bundle
→ verify
~~~

Do not sign and then patch the binary/version/resource.

## Nested code

If the product contains helpers, dylibs or executables:

- sign inner code first;
- sign the containing bundle afterward;
- use the intended identity consistently;
- keep entitlements minimal;
- verify nested signatures.

Avoid using --deep as a substitute for understanding nested code in a release script. It is useful for verification and some workflows, but explicit signing order is easier to audit.

## Hardened Runtime and entitlements

Apple's notarization guidance requires modern Developer ID distribution software to meet signing/notarization requirements including Hardened Runtime where applicable.

Important release rules:

- no accidental get-task-allow entitlement in production;
- no broad entitlement copied from a debug build without review;
- use secure timestamps for release signatures;
- document every non-default entitlement.

A successful local load does not prove correct release entitlements.

## Verify code signature

Example verification:

~~~bash
codesign -vvv --strict "/path/to/MyPlugin.plugin"
codesign -d --entitlements :- "/path/to/MyPlugin.plugin"
~~~

Inspect the actual shipping copy.

## Notarization

Apple no longer accepts the old altool notarization workflow. Use notarytool or the Notary API.

Typical command-line pipeline:

~~~text
signed plug-in
→ create supported submission archive/container
→ notarytool submit
→ inspect result/log
→ staple where applicable
→ verify Gatekeeper/signatures
~~~

Example shape:

~~~bash
xcrun notarytool submit "MyPlugin.zip"   --keychain-profile "notary-profile"   --wait
~~~

Credentials belong in Keychain/CI secret storage, not the repository or shell history.

## Read the notarization log

"Accepted" should not end the investigation automatically.

For release automation:

- capture the submission ID;
- store the final status;
- fetch the log on rejection;
- fail on rejection;
- archive enough metadata to reproduce the exact submitted artifact.

Do not resubmit a silently modified build under the same internal build identity.

## Source and version boundary — 2026-10-04

[Apple Developer ID](https://developer.apple.com/developer-id/), [notarization prerequisites](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) и [custom workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow) перепроверены. Hardened Runtime requirement для app/CLI targets и запрет release `get-task-allow` не означают, что plug-in может сам изменить entitlements Adobe host. Development re-sign copy из debugger guide не является release distribution workflow. Apple DocC text прочитан через официальный data endpoint; signing/submission в этой итерации NOT RUN. [Review](../BLOCK-5-REVIEW-2026-10-04.md).

## Stapling

Apple can publish the ticket online, and supported distributable containers can be stapled where applicable.

Whether the plug-in bundle itself, PKG or DMG is the stapled object depends on the delivery format. Test the exact offline/online installation path your users receive.

## Gatekeeper testing

A release should include a clean-machine test with an artifact that carries normal download quarantine behavior.

Do not prove only:

~~~text
local build directory
→ copied manually by developer
→ AE loaded it
~~~

That bypasses important distribution conditions.

## Release gate

The macOS release job fails if any required condition is false:

- wrong signing identity;
- missing architecture;
- invalid nested code signature;
- unexpected entitlement;
- notarization rejected;
- package changed after signing/notarization;
- clean install fails;
- AE cannot load the installed plug-in;
- release symbols/manifest are missing.

## Verification boundary

This chapter follows current Apple Developer ID/notarization guidance and AE SDK development-signing guidance. The Bible has not yet performed the complete Developer ID + notarization + quarantined clean-machine host cycle for every reference artifact.
