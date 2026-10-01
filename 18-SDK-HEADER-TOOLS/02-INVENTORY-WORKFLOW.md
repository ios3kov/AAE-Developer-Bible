# Workflow — from exact SDK headers to a usable recipe

The purpose of the header tools is to tie native documentation and recipes to one identifiable SDK instead of a floating memory of the API.

They are a preflight layer, not a substitute for the compiler or After Effects.

## 1. Pin the SDK

Record:

- Adobe SDK version/build;
- archive/source identity;
- local path used for the run;
- relevant header/sample hashes where the review requires them.

Do not label an SDK directory only latest.

## 2. Generate inventory

Run ae_sdk_inventory.py over the target Headers/Include tree according to the tool README.

Output should be stored with the validation evidence for that SDK.

The inventory is useful for:

- suite names/generations;
- declared functions;
- constants/macros/types supported by the parser;
- comparing two SDK snapshots.

## 3. Treat parser limits as limits

The inventory parser intentionally fails closed for declaration shapes it does not support.

Therefore:

~~~text
symbol present in inventory
≠ complete ABI proof

symbol absent from incomplete parse
≠ automatically removed from Adobe SDK
~~~

When a result is ambiguous, open the exact header manually.

Do not teach the parser to guess through unsupported C/C++ syntax just to make a run green.

## 4. Verify recipe symbols

Run verify_recipe_symbols.py against the inventory and the cookbook/reference code.

This catches useful mistakes:

- wrong suite generation name;
- misspelled function;
- recipe copied from another SDK generation;
- documentation drift.

It does not establish:

- exact parameter types;
- calling convention;
- ownership;
- runtime suite availability;
- semantic correctness.

The compiler and host still own those gates.

## 5. Review the nearest official sample

For any nontrivial API family:

~~~text
header declaration
→ header comments
→ closest SDK sample
→ Bible recipe
~~~

If a bundled sample is historical and differs from the current header, record the version boundary instead of forcing one to look like the other.

## 6. Compile

After symbol preflight:

- compile Debug;
- compile release configuration;
- build resources/PiPL;
- link final native artifact.

Compiler/type errors outrank prose examples.

Do not cast an old function table into a new suite struct to silence the compiler.

## 7. Run inside the host

Compilation cannot prove:

- loader/PiPL correctness;
- suite runtime availability;
- project mutation semantics;
- render pixels;
- MFR safety;
- GPU lifecycle;
- panel behavior.

Use named host fixtures and preserve environment/artifact identity.

## 8. New SDK upgrade workflow

When the SDK changes:

~~~text
old inventory
+ new inventory
→ diff_sdk_inventory.py
→ classify changes
→ inspect changed headers/samples
→ compile
→ host regression
→ compatibility decision
~~~

Do not begin by blindly fixing compiler errors until the contract diff is understood.

## 9. Evidence package

For an accepted SDK baseline retain:

- SDK identity;
- inventory JSON;
- diff vs previous supported SDK;
- parser/tool version or Git SHA;
- recipe-symbol result;
- compiler result;
- host result;
- known parser gaps;
- known docs/sample discrepancies.

## CI gate

A mature native lane:

~~~text
header inventory
→ recipe symbol preflight
→ native compile/resources/link
→ pure tests
→ package
→ host smoke
→ release signing/package gates
~~~

The current repository does not claim that every stage is automated on every platform.

## Stop rule

If header tooling disagrees with compiler/manual header inspection, stop and investigate. Do not edit evidence to force agreement.

See [SDK diff policy](03-SDK-DIFF-POLICY.md) and [header-first rules](04-HEADER-FIRST-RULES.md).
