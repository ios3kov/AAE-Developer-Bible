# Verification matrix

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

Until then, code is **compile-shaped and SDK-contract verified**, not falsely labelled as host-tested.
