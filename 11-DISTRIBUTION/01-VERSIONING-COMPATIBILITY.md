# Versioning and compatibility

A native AE product has several independent version domains. Treating them as one number creates migration and support bugs.

## Product version

A practical public version:

    MAJOR.MINOR.PATCH

Optionally attach a build identifier in internal manifests:

    1.4.2+1042

Do not overload the patch number with CI run IDs if customers/support need semantic meaning.

## Keep version domains separate

Track independently:

- marketing/product version;
- build number;
- native binary version metadata;
- PiPL/effect version where relevant;
- parameter layout/schema version;
- flattened sequence-data version;
- panel/native protocol version;
- installer schema/product code version;
- project-owned metadata version.

A change in one domain does not automatically require the same kind of change in all others.

## Effect project compatibility

When an old AE project contains an effect instance, compatibility depends on stable interpretation of persisted state.

Protect:

- parameter IDs;
- parameter semantic meaning;
- ordering assumptions where the host/API relies on them;
- sequence data;
- arbitrary/persistent data;
- custom marker/comment metadata used by scripts/panels.

Do not reuse an old parameter ID for a new meaning because a UI label was deleted.

## Sequence-data migration

Persisted binary data should start with an explicit schema/version and fixed-width fields.

Conceptual:

~~~cpp
struct Header {
    uint32_t magic;
    uint16_t schema_version;
    uint16_t header_size;
    uint32_t payload_size;
};
~~~

On load:

~~~text
validate magic/size
→ identify schema
→ migrate old schema to current in memory
→ reject unsupported/corrupt input safely
~~~

Never deserialize persisted files/projects directly into a compiler-dependent C++ struct with raw pointers, size_t or STL members.

## Bridge protocol compatibility

A CEP/UXP/script/native protocol should carry an explicit protocol version independent of product marketing version.

Example:

~~~json
{
  "protocol": 3,
  "requestId": "42",
  "command": "analyze"
}
~~~

When panel and native pieces can update independently, define:

- minimum supported protocol;
- maximum supported protocol;
- capability negotiation if needed;
- user-facing recovery when components are mismatched.

Fail with "component mismatch" rather than executing an unknown payload shape.

## Installer upgrade compatibility

Installer versioning must answer:

- can N upgrade N-1?;
- is downgrade allowed?;
- does uninstall of N remove only N-owned files?;
- what happens to shared user/license data?;
- what happens if old product filenames changed?;
- can x64 -> ARM64 migration occur safely?

Record upgrade policy as part of the release, not as tribal knowledge.

## Host support statement

Good:

> Tested with After Effects 25.6 and 26.x on macOS arm64; Windows x64 validation pending.

Bad:

> Works with all After Effects versions.

Separate:

- **tested** host/OS/architecture combinations;
- **expected compatible but not tested** combinations;
- **unsupported** combinations.

Do not turn compilation against one SDK into a claim for all future AE releases.

## Minimum and maximum host versions

A support policy should identify:

- oldest host you actively test;
- newest GA host tested;
- beta host observations, separately;
- architecture/OS constraints.

If the native API lets the binary load into a wider range than the product supports, documentation/support policy still needs to state the tested range.

## Beta versions

Beta smoke tests are valuable for early breakage detection.

They do not:

- replace GA validation;
- automatically expand the supported matrix;
- justify migrating production data formats without backward-compatibility tests.

Record beta observations as beta evidence.

## Deprecation

When dropping an AE version, OS or CPU architecture:

1. announce last supported product version;
2. stop claiming the platform in current docs;
3. keep installer/resource declarations consistent with shipped binaries;
4. preserve old release artifacts according to business/security policy;
5. define whether old versions continue receiving critical fixes.

## Compatibility test fixtures

Keep representative projects/assets from older supported versions.

At minimum test:

~~~text
create in old product
→ save project
→ open in new product
→ inspect params/state
→ render expected output
→ save/reopen again
~~~

Also test malformed/old sequence data if custom persistence exists.

## Verification boundary

A documented support matrix is not proof by itself. Every "tested" cell must ultimately link to build/install/host evidence for that exact platform/AE range.
