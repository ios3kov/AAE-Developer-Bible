# Composition recipes

**Primary Bible baseline:** Adobe After Effects SDK **25.6 build 61**.

**Baseline suite:** `AEGP_CompSuite12`.

`AEGP_CompSuite13` belongs to later-version research and must be feature/version-gated rather than silently replacing the 25.6 baseline.

## Create a composition

Companion [`CompLayerRecipes.cpp`](code/CompLayerRecipes.cpp) implements
`Bible_CreateComp` with fixed 1920×1080, PAR1:1, duration10s, fps25:1. It validates
only pica/name/output pointers; caller supplies folder legality, Unicode lifetime,
project freshness and Undo/exception boundary. It neither configures arbitrary
settings nor deletes its new project object after later command failure. The
remaining creation/configuration routes here are design guidance, not its code.

Conceptual call shape:

```cpp
A_Time duration{10, 1};
A_Ratio par{1, 1};
A_Ratio fps{25, 1};

AEGP_CompH compH = nullptr;
ERR(suites.CompSuite12()->AEGP_CreateComp(
    parent_folderH,
    utf16_name,
    1920,
    1080,
    &par,
    &duration,
    &fps,
    &compH));
```

Keep explicit:

- parent folder;
- UTF-16 name;
- dimensions;
- pixel aspect ratio;
- duration;
- frame rate;
- returned comp handle.

Do not replace rational time/frame-rate types with floating-point guesses.

## Item ↔ Comp

```text
ItemH
→ GetCompFromItem
→ CompH

CompH
→ GetItemFromComp
→ ItemH
```

Project item identity and composition handle are related but not interchangeable.

## Handle lifetime

`AEGP_CompH` is a host reference, not product-owned memory.

Do not:

- `delete` it;
- persist its raw pointer value;
- use it as cross-project database identity.

For long-lived product state, retain documented IDs/your own identifiers and re-resolve host refs when needed.

## Create a solid

Use the current `CompSuite12` declaration for exact signature/optional duration semantics.

Example shape:

```cpp
PF_Pixel color{};
color.alpha = 255;
color.red = 255;

AEGP_LayerH layerH = nullptr;
ERR(suites.CompSuite12()->AEGP_CreateSolidInComp(
    utf16_name,
    width,
    height,
    &color,
    compH,
    durationP0,
    &layerH));
```

Returned LayerH belongs to host model. Structural edits can invalidate assumptions about indices/order.

## Create camera / light / text

Current suite provides composition-level creation paths for camera/light/text-related layers.

Keep coordinate/time assumptions explicit:

- comp-space vs layer-space;
- 2D point vs 3D transform;
- current UI time vs explicit render/project time.

Do not infer coordinates from panel pixels.

## Composition marker stream

Composition marker data is exposed as a stream.

Pattern:

```text
CompH
→ GetNewCompMarkerStream
→ owned StreamRefH
→ Keyframe Suite for times
→ Stream Suite for values
→ Marker Suite for marker payload
→ DisposeStream
```

Stream ref/value/marker/memory handles have different cleanup families.

## Dimensions and duration

Validate product limits before mutation.

Do not let UI text fields directly become:

- width/height;
- time scale;
- frame rate numerator/denominator.

Normalize/validate first, then call host.

## Frame rate

Use rational representation from the API.

Examples like 23.976 are commonly represented as ratios rather than exact decimal float values.

Do not store product timing internally only as `double fps` if exact frame mapping matters.

## Active comp vs explicit comp

Do not build deep logic around “active comp” unless the feature explicitly targets the current UI context.

Better command model:

```text
resolve active comp at user action
→ normalize identity
→ pass explicit target into core operation
```

This improves stale-state handling and testability.

## Undo

User-visible comp creation/mutation should participate in deliberate undo grouping.

Validate all arguments first. Undo is not guaranteed transactional rollback for every partial failure.

## Feature gating: later CompSuite13

Later SDK research includes `AEGP_CompSuite13` and additional features such as parametric mesh creation.

Do not write baseline 25.6 code as:

```cpp
suites.CompSuite13()->...
```

unless the feature is explicitly version-gated.

Architecture:

```text
baseline feature → CompSuite12
optional later feature → acquire/use later suite only when supported
```

## Failure modes

Plan for:

- invalid parent folder;
- invalid dimensions/PAR/fps;
- unsupported later-suite feature;
- target project closed/changed;
- comp/item deleted between UI snapshot and command;
- partial operation followed by later failure.

## Product workflow

1. Resolve target project/folder.
2. Validate dimensions/timing/name.
3. Open undo group if user-facing.
4. Create comp/layers.
5. Store stable product identity, not raw refs.
6. Drop temporary refs after command.
7. Return fresh project/comp summary to UI.

## Version discipline

The supplied SDK 25.6 source review identifies `AEGP_CompSuite12` as the current baseline. Later suite notes must remain labeled as later-version research.

See [masks/text/footage SDK 25.6 review](../18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).

## Related chapters

- [Project/items](01-PROJECT-ITEMS.md)
- [Layers](03-LAYERS.md)
- [Streams/properties](05-STREAMS-PROPERTIES.md)
- [Lifetime/threading](14-LIFETIME-THREADING.md)

## Evidence boundary

Suite baseline and ownership statements are SDK-contract-reviewed. Bible does not claim runtime behavior of one specific composition-creation binary.
