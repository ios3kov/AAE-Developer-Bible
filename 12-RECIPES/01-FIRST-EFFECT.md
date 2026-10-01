# Recipe — first native effect

## Goal

Get one minimal native effect from clean source to a real After Effects host with the smallest possible number of moving parts.

Adobe SDK guidance recommends starting from the supplied Skeleton sample rather than reconstructing the host-specific project and Windows PiPL build machinery from scratch.

## Preconditions

Record:

- target After Effects version/build;
- target AE SDK version/build;
- OS and CPU architecture;
- compiler/toolchain;
- intended development install path.

Do not begin by renaming everything, adding dependencies and changing build output at once.

## Phase 1 — prove the untouched sample

~~~text
copy Skeleton
→ build untouched
→ install into development plug-in path
→ launch target AE
→ find/apply sample
→ render one deterministic frame
~~~

If the untouched sample does not load, stop. Product code is not yet the problem.

Capture:

- binary hash;
- build command/configuration;
- AE version;
- install path;
- load/render result.

## Phase 2 — fork identity only

Change only product identity:

- project/target name;
- effect display name;
- match name where intentionally chosen;
- category;
- bundle/file metadata;
- entry point only if necessary and consistently updated;
- version metadata.

Keep render behavior unchanged.

Rebuild and load again.

This separates identity/PiPL mistakes from algorithm mistakes.

## Phase 3 — preserve PiPL and entry-point contract

Cross-check:

~~~text
PiPL entry declaration
↔ exported effect entry symbol
↔ architecture declaration
↔ actual binary architecture
~~~

On macOS inspect the final executable slices. On Windows verify the PiPL resource is generated and linked into the .aex.

Do not copy only C++ files from Skeleton and discard resource build steps.

## Phase 4 — introduce an internal core

Keep host glue thin:

~~~text
PF callback / SmartFX adapter
        ↓
validate AE inputs
        ↓
convert to internal image/parameter views
        ↓
RenderCore
        ↓
write output
~~~

RenderCore should avoid AE handles where practical. That lets most algorithm tests run outside the host.

## Phase 5 — first deterministic operation

Choose deliberately simple behavior:

- copy/pass-through;
- gain/multiply;
- channel swap;
- another operation with an obvious expected result.

Create a synthetic fixture and expected output before adding UI complexity.

For a gain example:

~~~text
input pixel + gain
→ expected channel values
→ compare exact/tolerance according to pixel format
~~~

## Phase 6 — pixel formats

Add only the formats the product intends to support.

For every claimed depth verify separately:

- 8-bpc;
- 16-bpc;
- 32-bpc float if claimed;
- alpha;
- odd dimensions;
- nontrivial rowbytes/origin where relevant.

Do not mark 32-bpc supported because 8-bpc code compiled under a generic template.

## Phase 7 — save/reopen

Create a project with the effect:

~~~text
apply
→ change parameters
→ save
→ close AE
→ reopen
→ inspect parameters
→ render same frame
~~~

This catches parameter identity/persistence problems early.

## Phase 8 — only then add advanced features

Recommended order:

~~~text
basic CPU correctness
→ parameter/UI behavior
→ SmartFX/ROI
→ MFR
→ GPU
→ custom UI/panel/native bridges
~~~

Each stage inherits the previous correctness fixtures.

## Failure evidence

If load fails, preserve:

- exact artifact;
- AE log/crash report;
- architecture;
- signature state;
- PiPL/resource result;
- dependencies;
- install path.

If pixels fail, preserve the rendered output and diff rather than only a screenshot.

## Acceptance gate

The first-effect baseline is accepted only when every platform the current product actually claims has:

- clean native build/link;
- correct resource/entry contract;
- development install;
- AE discovery/load;
- deterministic render fixture;
- save/reopen;
- matching symbols archived.

A platform not yet tested remains pending; do not widen the support statement.

## Next

- [MFR migration](02-MFR-MIGRATION.md)
- [Render correctness](../10-TESTING/02-RENDER-CORRECTNESS.md)
- [macOS build](../08-MACOS/README.md)
- [Windows build](../09-WINDOWS/README.md)
