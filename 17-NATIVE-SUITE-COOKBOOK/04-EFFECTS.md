# Effect recipes

**Primary Bible baseline:** Adobe After Effects SDK **25.6 build 61**.

**Current suite:** `AEGP_EffectSuite5`.

Historical/compatibility source examples may use the older `AEGP_EffectSuite4` subset. The canonical Bible effect recipe and ownership helper are now aligned to current SDK 25.6 `AEGP_EffectSuite5`. Never cast suite tables between generations.

## Layer effect refs are owned references

### Companion source and partial outcomes

[`EffectStreamRecipes.cpp`](code/EffectStreamRecipes.cpp) contains installed-match
lookup, apply-and-dispose and static OneD setting, not a complete effect-stack editor.
Lookup returns generic error for an absent match and leaves key `NONE`; do not use
that output after failure. `Bible_ApplyEffect` returns no effect ref to configure and
does not open Undo or remove the added instance if later cleanup fails. An error can
therefore mean **effect applied, reference cleanup failed**, not “nothing changed”.
The static setter rejects non-OneD or time-varying streams; it does not bake animation
or disable expressions. Both mutation helpers require caller target validation,
supported callback context and exception/Undo policy. Normal return paths preserve
the primary error, but these helpers are not RAII exception-cleanup examples.

Current header explicitly marks the `AEGP_EffectRefH` returned by `AEGP_GetLayerEffectByIndex` as:

> MUST dispose with `AEGP_DisposeEffect`

Pattern:

```cpp
A_long count = 0;
ERR(suites.EffectSuite5()->AEGP_GetLayerNumEffects(layerH, &count));

for (A_long i = 0; i < count && !err; ++i) {
    AEGP_EffectRefH effectH = nullptr;
    ERR(suites.EffectSuite5()->AEGP_GetLayerEffectByIndex(
        plugin_id, layerH, i, &effectH));

    // inspect/use effectH

    ERR2(suites.EffectSuite5()->AEGP_DisposeEffect(effectH));
}
```

Do not store the raw effect ref as long-lived product identity.

## Effect order/index is not durable identity

Effect stack can change through:

- add;
- delete;
- reorder;
- user edits;
- other tools/scripts.

If product needs long-lived target identity, store a product-level description and re-resolve current effect instance.

## Installed-effect enumeration

Installed-effect key is an enumeration handle/key from current host context.

Do not hardcode it between AE sessions.

Pattern:

```text
GetNextInstalledEffect(NONE)
→ key
→ GetEffectMatchName
→ compare stable match name
→ next
```

Use **match name**, not localized display name.

## Current EffectSuite5

SDK 25.6 current header exposes `AEGP_EffectSuite5`.

It includes the familiar effect enumeration/apply/delete/generic-call operations plus newer table members relative to historical generations.

New current-baseline prose should cite Suite5. Compatibility source can keep Suite4 when it intentionally needs only that older public surface.

## Find installed effect by match name

Conceptual helper:

```text
wanted match name
→ enumerate installed keys
→ GetEffectMatchName
→ exact match
→ return current key
```

If no effect exists, report a product-level “required effect unavailable” result rather than using arbitrary first match/display string.

## Apply effect

Current header explicitly marks the returned `AEGP_EffectRefH` from `AEGP_ApplyEffect` as **MUST BE DISPOSED with `AEGP_DisposeEffect`**.

```cpp
AEGP_EffectRefH effectH = nullptr;
ERR(suites.EffectSuite5()->AEGP_ApplyEffect(
    plugin_id,
    layerH,
    installed_key,
    &effectH));

// configure/inspect effect

ERR2(suites.EffectSuite5()->AEGP_DisposeEffect(effectH));
```

Dispose releases the reference; it does not mean “remove effect from layer”.

## Delete effect

`AEGP_DeleteLayerEffect(effect_refH)` is undoable.

Important ownership point:

- refs returned by Get/Apply are explicitly caller-disposable;
- DeleteLayerEffect comment does **not** say it transfers/consumes ownership of the reference.

Therefore do not invent a new ownership rule such as “delete means never dispose the ref”. Keep reference cleanup according to the acquisition contract and do not use the deleted effect ref for further effect operations.

Use an ownership wrapper/cleanup path rather than simply setting the variable to null and leaking the acquired reference.

## Reorder effect

Effect Suite can reorder an effect instance in the stack.

After reorder:

- numeric effect indices change;
- cached index→effect mapping is stale;
- re-query if subsequent logic depends on stack order.

## Effect flags

Effect flags can expose host state such as active/missing/audio-related status.

Do not treat flags as persistent identity.

Use them as current host-state observation.

## Installed key from layer effect

Current effect instance can be mapped back to installed effect key.

Useful when product needs to identify which registered effect implementation owns an instance.

Still prefer match name for product-level readable/stable identification when appropriate.

## Parameter access

`AEGP_GetEffectParamUnionByIndex` can return parameter-definition metadata, but current header explicitly warns not to use the value from that ParamDef union as the actual parameter value.

Actual values belong to stream/property APIs.

Do not mix Effect Suite metadata inspection with Stream Suite value ownership.

## Effect parameter streams

Typical path:

```text
EffectRefH
→ parameter/stream lookup
→ owned StreamRefH
→ read/write StreamValue
→ dispose value/ref
```

See [Streams/properties](05-STREAMS-PROPERTIES.md).

## AEGP → Effect generic call

Current EffectSuite5 retains `AEGP_EffectCallGeneric`.

Pattern:

```text
AEGP owns fresh EffectRefH
→ versioned POD message
→ AEGP_EffectCallGeneric
→ host dispatch
→ PF_Cmd_COMPLETELY_GENERAL
→ effect validates size/version/op
→ response/error
```

Message should use:

- fixed-width fields;
- explicit size/version;
- clear ownership;
- no STL/string/vector ABI;
- no borrowed host pointers.

## Generic-call time

Header says generic-call `A_Time` uses the timebase of the layer to which the effect is applied.

Do not silently pass comp time without conversion/intent.

## Mutation and Undo

Apply/delete/reorder are project mutations.

Wrap semantic user command in appropriate undo group.

Validate targets before opening destructive sequence where practical.

## Stale effect refs

Do not retain `AEGP_EffectRefH` through long UI workflows.

Safe pattern:

```text
store layer identity + effect match/position/product identity
→ on command: resolve fresh layer
→ enumerate/resolve current effect
→ use owned EffectRefH
→ DisposeEffect
```

## Missing effects

An effect instance/registration may be missing/unavailable.

Product should distinguish:

- required installed effect absent;
- project contains missing effect;
- match name changed/misconfigured;
- effect disabled/flag state.

Do not collapse all of these into “effect not found”.

## Failure modes

Handle:

- layer deleted;
- stack changed;
- installed effect unavailable;
- ApplyEffect failed after other mutations;
- generic protocol mismatch;
- parameter stream unavailable;
- cleanup/dispose error.

## Product workflow: apply and configure

```text
resolve fresh LayerH
→ find installed effect by match name
→ StartUndoGroup
→ ApplyEffect
→ configure via stream APIs
→ dispose stream values/refs
→ DisposeEffect ref
→ EndUndoGroup
→ re-query state
```

## Current Suite5 vs historical Suite4 source

Current Bible baseline and canonical source now use `AEGP_EffectSuite5`.

Older Adobe samples or explicitly compatibility-shaped source may still use Suite4 or earlier generations. Read those as historical/compatibility dependencies only:

- do not infer current generation from old sample source;
- do not cast Suite4 to Suite5;
- do not silently downgrade new baseline examples to an older table merely because the called member exists there.

The required-contract manifest pins `AEGP_EffectSuite5` for SDK 25.6.

## Related chapters

- [Layers](03-LAYERS.md)
- [Streams/properties](05-STREAMS-PROPERTIES.md)
- [Communication: AEGP → Effect](../15-COMMUNICATION/03-AEGP-TO-EFFECT.md)
- [Effect↔AEGP bridge template](../16-WORKING-TEMPLATES/effect-aegp-generic-bridge/README.md)
- [Lifetime/threading](14-LIFETIME-THREADING.md)

## Evidence boundary

`AEGP_EffectSuite5` current generation and explicit ref-disposal markers are read directly from SDK 25.6 headers. Runtime behavior of one product/effect stack is not claimed by this source recipe.
