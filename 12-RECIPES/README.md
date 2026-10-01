# Practical recipes

This section turns the architecture chapters into repeatable workflows.

A recipe is not a shortcut around verification. Every recipe ends with a concrete acceptance condition and points back to the deeper contract chapters.

## Read order

1. [First native effect](01-FIRST-EFFECT.md)
2. [MFR migration](02-MFR-MIGRATION.md)
3. [Plug-in does not load](03-DEBUG-PLUGIN-NOT-LOADING.md)
4. [CPU/GPU equivalence](04-CPU-GPU-EQUIVALENCE.md)
5. [Hybrid panel + native core](05-HYBRID-PANEL-NATIVE.md)
6. [Profiling a slow effect](06-PROFILING.md)

## Recipe rule

Use this sequence:

~~~text
preconditions
→ smallest reproducible change
→ observable checks
→ failure evidence
→ acceptance gate
~~~

Do not call a recipe complete because a compiler, documentation build or one manual preview was green.

For release evidence, see [Testing strategy](../10-TESTING/README.md) and [Release checklist](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md).
