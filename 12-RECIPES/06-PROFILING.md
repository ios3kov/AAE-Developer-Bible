# Recipe — profiling a slow effect

1. Reproduce on fixed project/machine/AE build.
2. Measure full render baseline.
3. Disable GPU: compare.
4. Disable MFR: compare.
5. Time selectors/render stages.
6. Separate checkout/host time from own compute.
7. Profile allocations.
8. Profile lock contention.
9. For GPU: transfers, dispatch, sync, kernel.
10. Optimize one bottleneck.
11. Re-run correctness tests.
12. Re-run baseline.
13. Keep change only if measurable and no regression.
