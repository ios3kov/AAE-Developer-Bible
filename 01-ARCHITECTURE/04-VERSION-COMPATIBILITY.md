# Version compatibility

Compatibility in After Effects development is not one boolean.

A plug-in can be:

- source-compatible but not binary-compatible;
- binary-loadable but semantically broken;
- compatible on one CPU architecture and not another;
- compatible in AE but not in another host;
- compatible for basic render but not for MFR/GPU/custom UI.

Define the contract explicitly.

## Compatibility layers

### 1. Source compatibility

Can the code compile against a given SDK/toolchain?

Affected by:

- removed/changed declarations;
- suite generations;
- calling conventions;
- platform headers;
- compiler language rules.

### 2. Binary/loader compatibility

Can the built artifact be discovered and loaded?

Affected by:

- PiPL/resource declarations;
- architecture;
- exported entry points;
- package layout;
- dependent libraries;
- signing/platform trust.

### 3. Runtime API compatibility

Do required suites/selectors/features exist at runtime?

Affected by:

- host version;
- suite acquisition/version;
- optional capabilities;
- host-product differences.

### 4. Semantic compatibility

Does the same operation still behave as the product expects?

Examples:

- project mutation semantics;
- color behavior;
- render/cache behavior;
- custom UI lifecycle;
- GPU backend behavior.

### 5. Project/data compatibility

Can projects created with one plug-in version reopen safely with another?

Affected by:

- parameter IDs;
- match names;
- sequence data;
- persistent schemas;
- defaults;
- migration logic.

## SDK baseline vs supported AE range

Do not write:

> built with SDK 25.6, therefore supports AE 25.6+

That inference is not automatic.

An SDK baseline tells you which source contracts you used. Product support range is a separate policy.

## Suite version gating

For PICA/AEGP suites:

~~~text
need feature
→ know suite name + public version
→ acquire
→ handle unavailable/older version
→ use
→ release
~~~

Do not cast an older suite pointer to a newer struct just to avoid branching.

If feature is optional, degrade gracefully.

If feature is fundamental, fail early with a useful compatibility message.

## Effect selectors and flags

Effect plug-ins also have compatibility contracts in:

- PiPL;
- API version fields;
- global outflags;
- selector handling;
- SmartFX/MFR/GPU capability declarations.

Advertising a capability can cause the host to call selectors/paths the plug-in must actually implement.

## Stable identity

Changing these can break existing projects:

- match name;
- parameter IDs;
- persistent data schema;
- effect registration identity.

Display name is not the same thing as persistent identity.

Plan renames separately from ABI/project identity.

## Parameter evolution

Safe parameter evolution requires deliberate IDs.

Typical rules:

- never recycle an old parameter ID for a different meaning;
- append/add parameters carefully;
- define migration/default behavior;
- preserve project interpretation.

UI index and persistent ID are different concepts.

## Persistent data

Version your own stored data.

Example:

~~~text
magic
schema version
payload size
payload
~~~

On load:

1. validate size/version;
2. migrate known old version;
3. reject/repair malformed state deliberately;
4. never reinterpret arbitrary old bytes as a new struct.

C/C++ struct layout is not a durable serialization format by default.

## Cross-architecture compatibility

### macOS

Universal support implies all native dependencies and nested components support required slices.

### Windows

ARM64 support is not implied by x64 source compiling.

Check:

- dependencies;
- installer paths;
- helper processes;
- GPU backends;
- code-generation assumptions.

## Host-product compatibility

Some AE SDK concepts overlap with Premiere or other Adobe hosts, but support must be explicit.

Do not infer Premiere compatibility from:

- shared headers;
- similar pixel structs;
- same MediaCore install path.

Check the exact host contract.

## Compatibility matrix

Product support statement should distinguish **supported** and **tested evidence**.

Example:

| Host | mac arm64 | mac x86_64 | Win x64 | Win ARM64 | Policy |
|---|---:|---:|---:|---:|---|
| AE 25.x | supported | no | supported | no | supported |
| AE 26.x | supported | no | supported | planned | supported with stated limits |
| Beta | lab | no | lab | lab | no customer support promise |

Avoid treating “Beta opened once” as a support claim.

## New AE release workflow

When a new AE release appears:

1. read Adobe release/SDK notes;
2. diff relevant SDK/header contracts if SDK changed;
3. identify changed high-risk areas;
4. load existing product artifact where policy allows;
5. exercise representative project/render workflows;
6. check MFR/GPU/UI paths used by the product;
7. check save/reopen and persistent state;
8. update support statement only after evidence is adequate.

This workflow belongs to the product team. Bible documents the method; it does not need to perform it for every version.

## New SDK adoption workflow

Do not begin with “fix compiler errors until green”.

Use:

~~~text
old SDK contract
+ new SDK contract
→ declaration diff
→ classify changes
→ inspect official samples/comments
→ update source/gating
→ update documentation/support policy
~~~

The [SDK contract tools](../18-SDK-HEADER-TOOLS/README.md) exist to help with this review.

## Version-sensitive documentation

When Bible names a specific suite generation or platform rule, include its boundary.

Good:

> SDK 25.6 exposes StreamSuite6 in the supplied baseline.

Bad:

> StreamSuite6 is always the current stream API.

Future editions may use another baseline.

## Deprecation and legacy samples

Official SDK bundles can contain old samples using older suite generations.

Treat them as:

- pattern evidence;
- lifecycle examples;
- historical compatibility examples.

Do not automatically treat sample signatures as the newest contract when current headers differ.

## Graceful degradation

Feature gating should be deliberate.

Example:

~~~text
if new suite available:
    enable advanced feature
else:
    use documented fallback
~~~

Do not silently run a partially equivalent fallback that changes project/render semantics.

## Compatibility failures to plan for

- suite unavailable;
- newer project data loaded by older plug-in;
- unsupported CPU architecture;
- missing nested dylib/DLL;
- changed GPU capability;
- host calls optional selector now advertised by flags;
- old sample copied with obsolete ABI;
- panel runtime migration;
- installer finds multiple AE versions.

## Documentation/release language

Prefer precise language:

- “supported”;
- “tested on”;
- “known issue”;
- “experimental”;
- “not supported”.

Avoid:

- “should work everywhere”;
- “compatible with all newer AE versions”;
- “future proof”.

## Related chapters

- [Environment matrix](../00-START-HERE/02-ENVIRONMENT-MATRIX.md)
- [PiPL and loading](03-PIPL-AND-LOADING.md)
- [SDK diff policy](../18-SDK-HEADER-TOOLS/03-SDK-DIFF-POLICY.md)
- [Compatibility matrix template](../13-TEMPLATES/COMPATIBILITY-MATRIX.md)
- [Distribution](../11-DISTRIBUTION/README.md)

## Evidence boundary

Current Bible native baseline is SDK 25.6 build 61. The chapter describes compatibility design methodology; it does not claim universal compatibility for Bible source examples.
