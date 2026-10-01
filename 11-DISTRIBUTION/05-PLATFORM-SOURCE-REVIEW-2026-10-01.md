# Scripting, panels and platform distribution source review — 2026-10-01

## Scope

This record covers the editorial pass over:

- 06-SCRIPTING;
- 07-PANELS;
- 15-COMMUNICATION scripting/panel bridge chapters;
- 08-MACOS build/sign/package/CI;
- 09-WINDOWS build/sign/package/CI;
- 11-DISTRIBUTION.

It is a documentation/source-review milestone. It does not claim a new native build, signed release, notarization, Windows compiler run, installer run or After Effects host test.

## Primary public sources

### Adobe CEP

Adobe CEP Resources:

- https://github.com/Adobe-CEP/CEP-Resources
- CEP 12 HTML Extension Cookbook in that repository

Reviewed contract:

- the CEP HTML engine and host ExtendScript engine are separate JavaScript engines;
- CSInterface.evalScript is the host scripting bridge;
- evalScript/ScriptPath JSX executes in the host ExtendScript engine on the host main thread;
- CEP events also depend on host main-thread scheduling, so long scripts should be split;
- CSXS events are the documented substitute when ExtendScript needs to communicate toward the HTML extension.

Adobe CEP Samples:

- https://github.com/Adobe-CEP/Samples
- AfterEffectsPanel sample uses host ID AEFT and demonstrates invoking After Effects ExtendScript from a CEP panel.

### Adobe UXP / CEP transition

Adobe Developer Blog, 2026-09-24:

- https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications

Snapshot used in this edition:

- After Effects UXP public beta planned by November 2026;
- phased CEP transition is multi-year;
- AE/Illustrator/Media Encoder stop accepting new CEP Marketplace submissions and move CEP disabled-by-default in December 2028;
- CEP retirement across flagship desktop applications begins at the end of 2029;
- ExtendScript is not included in the CEP retirement statement.

The Bible treats these as dated planning milestones, not proof of an After Effects UXP API before the beta exists.

### After Effects SDK guide — build and install

Relevant pages:

- https://ae-plugins.docsforadobe.dev/intro/how-to-start-creating-plug-ins/
- https://ae-plugins.docsforadobe.dev/intro/sample-projects/
- https://ae-plugins.docsforadobe.dev/intro/pipl-resources/
- https://ae-plugins.docsforadobe.dev/intro/apple-silicon-support/
- https://ae-plugins.docsforadobe.dev/intro/windows-on-arm-support/
- https://ae-plugins.docsforadobe.dev/intro/debugging-plug-ins/
- https://ae-plugins.docsforadobe.dev/intro/where-installers-should-put-plug-ins/

Reviewed contract:

- graft product code into an existing sample rather than rebuilding host-specific project machinery from scratch;
- Windows sample projects contain custom PiPL resource generation that must be preserved;
- macOS development output is recommended in the per-user MediaCore path;
- Windows samples use AE_PLUGIN_BUILD_DIR for convenient development output;
- release installers should use documented Adobe install-path guidance;
- macOS Universal support requires matching binary architecture slices and PiPL entry declarations;
- Windows-on-Arm support requires an ARM64 target and CodeWinARM64 declaration for a native ARM host;
- macOS 15+ development loading requires signed plug-ins according to current debugging guidance.

Docs for Adobe is maintained outside Adobe itself; exact compile-time contracts still defer to the supplied SDK headers/samples used elsewhere in this Bible.

### Apple distribution

Apple Developer ID:

- https://developer.apple.com/developer-id/

Apple notarization:

- https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- https://developer.apple.com/documentation/security/customizing-the-notarization-workflow

Reviewed contract:

- Developer ID is the normal identity mechanism for software distributed outside the Mac App Store;
- Apple notarization checks Developer ID-signed software and produces a ticket recognized by Gatekeeper;
- altool uploads are no longer accepted by the notary service; current command-line workflows use notarytool;
- signing/notarization applies to plug-ins and installer/delivery artifacts as appropriate;
- final release contents must not be mutated after signing.

### Microsoft signing

Microsoft SignTool:

- https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool

Reviewed contract:

- SignTool signs, timestamps and verifies Authenticode signatures;
- current guidance requires explicit file digest and timestamp digest algorithms;
- SHA-256 is the recommended baseline;
- RFC 3161 timestamping uses /tr with /td;
- verification must run on the final shipping file.

## Editorial changes

The pass expanded previously short notes into production-oriented chapters covering:

- one-based scripting collections, stable match names, invalidated references and command-layer separation;
- ScriptUI window/panel architecture and long-operation limits;
- CEP request/response protocol, stale-response handling, path/data-plane boundaries and security;
- UXP migration inventory without pretending the future AE beta API is already available;
- native/script/panel control-plane vs data-plane architecture;
- Xcode and Visual Studio sample-first build workflows;
- Universal/x64/ARM64 artifact rules;
- macOS Developer ID/notarization and Windows Authenticode pipelines;
- installer file ownership, upgrade/uninstall and architecture selection;
- CI provenance, symbols, manifests and clean-host gates;
- project/schema/protocol compatibility and an expanded release checklist.

## Evidence boundary

NOT RUN in this editorial pass:

- new SDK 25.6 native compilation;
- link/package of a new .plugin or .aex;
- Developer ID signing;
- Apple notarization submission;
- Windows Authenticode signing;
- macOS/Windows installer execution;
- CEP panel execution in After Effects;
- UXP execution in After Effects;
- clean-machine host load;
- Windows x64/ARM64 AE host matrix.

No release/test status is upgraded from this source review alone.
