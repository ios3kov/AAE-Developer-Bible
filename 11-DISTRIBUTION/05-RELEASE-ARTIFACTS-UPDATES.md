# Release artifacts, installers and update strategy

Distribution is the point where a technically correct plug-in becomes a supportable product.

## Release set

Worked [NOT_RUN Gain pack](../13-TEMPLATES/examples/WORKED-EXAMPLE.md) separates
source lesson from hypothetical product artifact. Platform designs bind unsigned
candidate → signed binary → package → installed/loaded identity, with matching
[macOS UUID/dSYM](../08-MACOS/07-CI.md) or [Windows PDB](../09-WINDOWS/07-CI.md).
Owned-file [macOS](../08-MACOS/06-INSTALLATION-PACKAGING.md)/
[Windows](../09-WINDOWS/06-INSTALLATION-PACKAGING.md) rollback restores prior bytes,
not automatically downgraded project schemas. Candidate FAIL remains FAIL after recovery.

A release should have a defined artifact set, for example:

```text
macOS installer/container
Windows installer
checksums
build manifest
support matrix
changelog
known issues
rollback artifact
symbols stored privately
```

Do not treat the binary copied from a developer plug-ins folder as the release artifact.

## Build manifest

Record at least:

- product version/build;
- Git commit/tag;
- Adobe SDK version/build;
- compiler/toolchain versions;
- target OS/architectures;
- exact binary hashes;
- installer/package hashes;
- signing/notarization status;
- supported AE versions;
- schema/protocol versions where relevant.

The manifest belongs to the release, not only to CI logs that may expire.

## Installer ownership

Maintain an explicit inventory of files the installer owns.

Uninstall must remove only those files plus documented product-created caches/config where policy allows.

Never recursively delete a broad Adobe/Common/Plug-ins directory.

## Upgrade

Define upgrade semantics before shipping v1:

- in-place replace;
- side-by-side versions;
- migration of settings;
- migration of licenses/account tokens;
- preservation/removal of caches;
- downgrade policy.

A version comparison bug in an installer can be more destructive than a rendering bug.

## Rollback

Retain at least one known-good previous release and its manifest.

Rollback procedure should answer:

1. which files are replaced;
2. whether settings/schema downgrade safely;
3. whether old AE projects remain compatible;
4. whether user data needs backup;
5. how to verify the rollback loaded correctly.

## Auto-update

A native AE plug-in should not self-update its loaded binary in place while After Effects is using it.

Safer model:

```text
check metadata
 -> download to staging
 -> verify signature/hash
 -> ask for/coordinate AE shutdown
 -> installer performs controlled owned-file upgrade with journal/rollback
 -> next AE launch loads new build
```

If a helper performs updates, authenticate and version that helper separately.

## Download integrity

At minimum:

- HTTPS delivery;
- platform code signing;
- published/recorded cryptographic hashes;
- signed update metadata if building an auto-updater;
- strict artifact/version matching.

Do not trust only a filename such as `MyPlugin-latest.zip`.

## Compatibility statement

Every release should publish a support matrix with explicit status:

```text
AE version
OS version
architecture
GPU/backend if relevant
tested/not tested
known limitations
```

"Works with Creative Cloud" is not a compatibility matrix.

## Beta/pre-release

Pre-release packages should be unmistakably identified:

- distinct version/build;
- separate update channel if used;
- expiration only if intentional and documented;
- explicit project/file compatibility warning when schemas may change.

Do not accidentally allow beta builds to overwrite production settings without migration policy.

## Customer diagnostics

A supportable release should expose enough information to identify:

- product version/build;
- architecture;
- loaded module path;
- protocol/schema version;
- relevant GPU/backend;
- helper/service version if any.

Avoid collecting unrelated personal data.

## Final release gate

Before publishing:

1. build from clean source;
2. run platform signing gates;
3. install the exact packaged artifact;
4. run host smoke tests on the supported matrix;
5. verify upgrade from previous release;
6. verify uninstall;
7. verify rollback;
8. archive artifacts/manifests/symbols;
9. publish changelog/support matrix/checksums.

See [release checklist](03-RELEASE-CHECKLIST.md).
