# 3D Channel Extract — Runtime Acceptance Protocol

Target: **After Effects 25.6.0.101 / macOS arm64**  
Binary identity from static capture: SHA-256 `412a6deefc1d7a710a9019b6a068180556417b0548d0703d34852bcd395dcab8`

Purpose: close only facts that static disassembly cannot prove. Record observed values; do not infer missing behavior.

## Required runtime gates

- [ ] UI menu item ↔ stored selector integer mapping
- [ ] Parameter defaults and ranges
- [ ] Anti-alias OFF → DPTH/DPAA identity
- [ ] Anti-alias ON → DPTH/DPAA identity
- [ ] Clamp Output behavior
- [ ] Invert Depth Map behavior
- [ ] Black Point == White Point
- [ ] reversed Black/White points
- [ ] Plus Infinity
- [ ] Minus Infinity
- [ ] missing channel behavior/error
- [ ] datatype mismatch behavior/error where a controlled fixture permits it
- [ ] 8-bpc pixel fixture
- [ ] 16-bpc pixel fixture
- [ ] 32-bpc pixel fixture
- [ ] Object ID boundary behavior
- [ ] alpha behavior
- [ ] CPU/GPU/MFR runtime status

## Evidence rule

For each observation record:

```text
Repository commit:
AE exact build:
OS:
Composition/project:
Renderer/source:
Project bit depth:
Effect parameter values:
Expected question:
Observed UI/output:
Pixel values or output hash:
Screenshot/log reference:
PASS / FAIL / UNAVAILABLE:
Notes:
```

## Phase A — parameter/UI inspection

On a layer where the effect is available, record the exact visible defaults and allowed values for:

1. 3D Channel
2. Black Point
3. White Point
4. Anti-alias
5. Clamp Output
6. Invert Depth Map

Cycle the 3D Channel popup through all eight entries and record any parameter enable/disable changes.

## Phase B — selector and DPTH/DPAA

Use LLDB only to observe, not patch, the target binary.

Break on the common channel-acquisition area after the channel FourCC has been selected. For each UI popup item record the selected machine FourCC. Repeat Z-Depth with Anti-alias OFF and ON.

Acceptance result should produce a table:

| UI item | stored selector | FourCC | datatype |
|---|---:|---|---|
| Z-Depth | | | |
| Object ID | | | |
| Texture UV | | | |
| Surface Normals | | | |
| Coverage | | | |
| Background RGB | | | |
| Unclamped RGB | | | |
| Material ID | | | |

## Phase C — depth edge fixtures

With a source that exposes depth data, capture the same pixels under:

1. normal Black < White;
2. Invert ON;
3. Clamp OFF/ON with samples outside range;
4. Black == White;
5. Black > White;
6. +Infinity sample if source can produce it;
7. -Infinity sample if source can produce it;
8. Anti-alias OFF/ON.

Record raw source depth where observable and output RGBA at 8/16/32 bpc.

## Phase D — channel fixtures

For every available channel select at least one known non-zero pixel and record output RGBA at 8/16/32 bpc.

Special cases:

- Object ID: test 0, 1, values around 32767/32768 if controllable, and max available.
- Texture UV: choose a pixel with non-equal U/V to establish component ordering.
- Normals: choose a non-symmetric normal to establish XYZ→RGB ordering.
- Coverage: choose fractional coverage if controllable.
- Background RGB: choose distinct R/G/B bytes.
- Unclamped RGB: include a component outside 0..1 if source permits.
- Material ID: test at least 0, 1 and a larger ID.

## Phase E — unavailable/error behavior

Apply the effect to a source without auxiliary 3D data and record:

- visible output;
- error text;
- return/error behavior;
- whether alpha/RGB are cleared or preserved.

If a controlled datatype mismatch can be produced without binary modification, record it. Otherwise mark it UNAVAILABLE rather than manufacturing evidence.

## Phase F — runtime architecture

Record:

- whether AE reports the effect as CPU/GPU accelerated;
- behavior under Multi-Frame Rendering;
- whether concurrent renders remain deterministic;
- whether 8/16/32 bpc produce equivalent normalized results within expected quantization.

## Completion condition

This protocol is complete only when every gate above is PASS or explicitly UNAVAILABLE with a reason. Static evidence may explain a runtime observation but may not replace it.
