# Verification matrix

## v1.1 compiled baseline

All six `code/*.cpp` recipes pass strict syntax/type checks with **SDK 25.6 on macOS arm64**. Sources use CompSuite12, StreamSuite6, KeyframeSuite5 and RQItemSuite3 where applicable. Narrative sections may describe newer generations; acquire only suites supplied by the SDK/host you target. See [reproducible checks](../VERIFICATION.md).

The table below records historical public-documentation review, not compiler or host evidence. No host execution is claimed.

| Area | Public SDK signature checked | Adobe sample pattern | Host executed here |
|---|---:|---:|---:|
| Project / Item | yes | Projector | no |
| Composition / Layer | yes | Projector | no |
| Effect / Stream | yes | Streamie-style | no |
| Keyframes | yes | Easy Cheese-style | no |
| Masks / Text / Markers | yes | SDK guide | no |
| Frame checkout | yes | Grabba/render samples | no |
| Render Queue | yes | QueueBert | no |
| Guide / ItemView 26.5 | release-notes + guide | n/a/new | no |

## Meaning

`yes` in the first column means the public declaration/contract used by the recipe was checked. It does **not** mean the snippet was compiled against Adobe's proprietary 26.5 headers inside this sandbox.

The final engineering verification step is:

```text
official 26.5 SDK headers
→ build macOS
→ build Windows x64
→ build Windows ARM64 where targeted
→ launch target AE
→ exercise recipe
→ record result in compatibility matrix
```

Current source is **SDK 25.6 syntax/type-checked**; linking, host execution and other SDK/platform versions remain pending.
