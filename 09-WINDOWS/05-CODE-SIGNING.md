# Windows — code signing

Windows Authenticode signing establishes publisher identity and lets Windows verify that the signed file has not changed since signing.

It does not prove the plug-in is functionally correct.

## Tool

Microsoft SignTool is part of the Windows SDK.

Current SignTool guidance requires explicit file digest and timestamp digest algorithms. SHA-256 is the normal baseline.

Conceptual signing command:

~~~bat
signtool sign /fd SHA256 /td SHA256 /tr <RFC3161_TIMESTAMP_URL> /a MyPlugin.aex
~~~

Actual certificate selection depends on release infrastructure:

- certificate store;
- hardware token/HSM;
- PFX in a protected environment;
- managed/trusted signing service.

Do not encode a private-key deployment strategy into the product repository.

## Verify

~~~bat
signtool verify /pa /v MyPlugin.aex
~~~

Verify the exact staged/shipping file after all mutations are complete.

## Sign final binaries

Correct order:

~~~text
compile/link
→ final resource/version metadata
→ dependency staging
→ sign .aex / helper .dll/.exe
→ verify
→ build installer
→ sign installer
→ verify installer
~~~

Any post-sign binary/resource patch changes the file and invalidates the signature.

## What to sign

Sign executable code you distribute:

- .aex;
- product DLLs;
- helper EXEs;
- installer EXE/MSI or bootstrapper as applicable.

Do not assume signing only the outer installer is equivalent to signing the native code inside it.

## Timestamp

Use an appropriate timestamp service so the signature retains meaningful validation after the signing certificate itself expires, subject to Windows trust policy.

A timestamp failure should fail a release signing job unless your release policy explicitly defines a safe recovery path.

## Certificate security

Release key rules:

- never commit private keys;
- do not expose signing credentials to pull-request jobs;
- protect the release environment;
- require least privilege;
- log the certificate identity/serial metadata needed for audit, not the private material;
- rotate/revoke according to incident policy.

## Reproducibility vs signing

Two separately signed binaries can differ even if built from identical source because signing adds metadata.

Track both:

~~~text
unsigned/staged binary hash
signed binary hash
signing identity
timestamp metadata
source git SHA
~~~

This preserves provenance.

## SmartScreen reputation is not correctness

A valid Authenticode signature can improve identity/trust UX, but it does not guarantee an installer will never receive a SmartScreen warning.

Do not weaken signing/security to chase reputation behavior.

## Failure cases to test

- signature valid;
- binary modified after signing -> verification fails;
- timestamp unavailable -> release job fails;
- wrong certificate selected -> release job fails;
- certificate expired/revoked scenario is understood;
- installer contains only intended signed payload.

## Verification boundary

This chapter follows current Microsoft SignTool/AuthentiCode guidance. This chapter documents the Windows signing workflow. Bible does not claim that its reference source has been shipped as signed Windows artifacts, and such binaries are not required for editorial completion.
