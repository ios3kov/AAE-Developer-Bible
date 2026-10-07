# Release notes template

# Product X.Y.Z

Filled [source-lesson release example](examples/WORKED-EXAMPLE.md) declares
no tested AE/OS support range and no installable release artifact. Documentation
completion is not permission to turn NOT_RUN cells into customer support promises.

Release date:

Build:

## Highlights

Short user-facing summary of the release.

## Added

- 

## Changed

- 

## Fixed

- 

Each fix should be written in user-observable terms. Internal issue IDs may be added in parentheses.

## Performance

State only measured changes.

Good:

- Reduced median render time by X% on the named fixture/environment.

Avoid:

- Much faster.

If performance evidence is internal, keep the report ID available to support/release engineering.

## Compatibility

### Tested After Effects

- 

### macOS

- OS versions:
- arm64:
- x86_64:
- GPU notes:

### Windows

- OS versions:
- x64:
- ARM64:
- GPU notes:

Do not list a platform as tested if its matrix cell is NOT RUN.

## Project/data compatibility

- Opens projects from:
- State/schema migration:
- Downgrade warning:
- Project changes that older product versions cannot understand:

## Panel/protocol compatibility

If applicable:

- panel version:
- native version:
- protocol:
- helper version:
- minimum compatible component versions:

## Installation / upgrade notes

- Fresh install:
- Upgrade from:
- Restart AE required:
- Old files automatically removed:
- Manual action:
- Rollback notes:

## Known issues

For each issue:

- affected environment;
- symptom;
- workaround if safe;
- data-loss/crash risk;
- tracking/support reference.

Do not hide a release-blocking defect in known issues.

## Security / licensing

Only if relevant to the release:

- security fixes:
- changed network endpoints:
- licensing/offline policy changes:
- updater/signing changes:

Avoid disclosing secrets or exploit details that create unnecessary risk before a fix is broadly available.

## Checksums

List the actual published artifact hashes:

~~~text
macOS package SHA-256:
Windows x64 package SHA-256:
Windows ARM64 package SHA-256:
~~~

## Support

- Documentation:
- Support contact/process:
- Diagnostic information to include:

## Internal release evidence

Not necessarily published to users:

- release commit/tag:
- artifact manifest:
- compatibility matrix:
- test run/evidence IDs:
- symbols archive:
- signing/notarization record:
- rollback artifact:
