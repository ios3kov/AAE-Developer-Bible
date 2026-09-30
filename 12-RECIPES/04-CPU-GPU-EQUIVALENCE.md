# Recipe — CPU/GPU equivalence

1. Freeze CPU reference implementation.
2. Define test images and parameter vectors.
3. Define numeric tolerance before GPU comparison.
4. Render CPU outputs to raw/high-precision fixtures.
5. Render GPU outputs.
6. Compute per-channel diff stats.
7. Visualize heatmap for failed pixels.
8. Fix edge/alpha/clamp/order issues.
9. Repeat for 8/16/32-bpc.
10. Repeat under MFR.
11. Test fallback after simulated GPU init failure.

Do not accept «на глаз одинаково» for core render correctness.
