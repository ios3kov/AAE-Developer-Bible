# CEP -> ExtendScript JSON bridge

**SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.** Logic skeleton; manifest, Adobe `CSInterface.js`, reviewed ES3-compatible JSON dependency and signing configuration must be supplied separately. No installed-extension or AE execution claim.

## Canonical protocol

```json
{"protocol":1,"requestId":"session:1","command":"renameSelected","payload":{"prefix":"Bible_"}}
```

```json
{"protocol":1,"requestId":"session:1","ok":true,"result":{"changed":2}}
```

```json
{"protocol":1,"requestId":"session:1","ok":false,"error":{"code":"NO_ACTIVE_COMP","message":"No active composition.","outcome":"notApplied"}}
```

`renameSelected` prefixes all layers selected in the active composition **at execution time**. Repeating adds the prefix again; no deduplication or idempotency guarantee. String prefix is required (maximum 256 UTF-16 code units). Empty prefix is a no-op with `changed:0` after comp/selection validation. No implicit conversion of arbitrary values.

Startup `ping` with `{}` confirms dispatcher readiness. One call may be outstanding. A local 15-second waiting timeout does not cancel host work. Timeout, malformed response, bridge exception or `mayHaveApplied` blocks further mutations, including after a late callback; inspect the project before reloading. A confirmed `notApplied` command error permits a manual retry. Other scripts/user actions are not serialized by this panel.

`index.js` validates envelopes and explicitly accepts bounded null-ID bootstrap/internal fallbacks. `host/index.jsx` validates before routing, preserves primary and Undo-close errors, and uses fixed JSON fallbacks. Undo grouping does not roll back partial mutation. Limits (65536 message code units / 128 ID code units) are sample policies, not CEP transport limits.

## Package and bootstrap

The documentation site publishes the HTML source as `index.html.txt` beside this
chapter; rename the downloaded source to `index.html` when packaging. It is not an
executable extension in the site and cannot overwrite the chapter's generated index.

Follow the [manifest/JSON/bootstrap walkthrough and failure table](../../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md). HTML loads `./CSInterface.js`, then `./index.js`. Manifest `MainPath` should point to HTML; `ScriptPath` should point to your bootstrap JSX, which loads the vetted JSON implementation before `host/index.jsx`. HTML does not itself load JSX. Do not rely on JSON installed by another panel; record dependency version/hash/license and test the packaged copy against your AE/CEP targets.

No manifest or polyfill is bundled here. The walkthrough is a source integration example, not an install-ready extension.

## Portable verification

From repository root:

```sh
node scripts/test_cep_bridge.js
```

Runs real source in Node VM with fake DOM/AE objects/timers. Verifies parsing/types, bootstrap visibility, correlation, prefix semantics, escaping, single outstanding mutation, timeout/late replies, shutdown, primary/cleanup errors and serialization fallback. Does not prove ES3 parser compatibility, CEP scheduling, actual AE setters/Undo or packaged installation. Product host verification remains separate. See [evidence ledger](../../VERIFICATION.md#block-2-cep-protocol-and-failure-paths-2026-10-04).
