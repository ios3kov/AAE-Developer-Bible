# Performance report template

## Decision

- Report ID:
- Date:
- Candidate:
- Baseline:
- Owner:
- Goal:
- Predefined regression/improvement threshold:

## Build identity

### Baseline

- Product version/build:
- Git SHA:
- Binary hash:

### Candidate

- Product version/build:
- Git SHA:
- Binary hash:

## Environment

- After Effects version/build:
- OS version/build:
- CPU:
- RAM:
- GPU:
- Driver/runtime:
- Power mode:
- Thermal notes:
- Toolchain if relevant:

## Scenario

- Project/fixture:
- Fixture hash/version:
- Resolution:
- Duration/frames:
- BPC:
- MFR:
- GPU backend:
- ROI/render path:
- Cache state:
- Warmup procedure:

## Method

- Number of warmup runs:
- Number of measured runs:
- Timing source/tool:
- Outlier policy defined before run:
- Other processes controlled:
- Same environment for baseline/candidate: yes / no

## Results

| Metric | Baseline | Candidate | Delta | Threshold | Pass |
|---|---:|---:|---:|---:|---|
| Cold/first frame | | | | | |
| Warm median frame | | | | | |
| p95 frame | | | | | |
| Full render | | | | | |
| Peak memory | | | | | |
| Retained memory after run | | | | | |
| CPU utilization | | | | | |
| Lock wait | | | | | |
| GPU upload/prep | | | | | |
| GPU kernel | | | | | |
| GPU sync/readback | | | | | |

Use only metrics relevant to the feature.

## Raw evidence

- Raw samples:
- Profiler trace:
- Benchmark command:
- Logs:
- Chart/report artifact:

## Correctness gate

Performance result is invalid unless correctness still passes.

- Golden fixture:
- Expected/tolerance:
- Max diff:
- RMS/mean diff:
- Alpha diff:
- Pixels above tolerance:
- NaN/Inf:
- Result: PASS / FAIL

## MFR notes

- MFR off result:
- MFR on result:
- Scaling:
- Peak memory change:
- Global serialization observed:
- Race/stability test reference:

## GPU notes

- CPU baseline:
- GPU backend:
- Upload:
- Kernel:
- Sync:
- Download:
- Crossover resolution/workload:
- CPU fallback verified:

## Analysis

What changed and which measured stage explains it?

Do not infer cause from total time alone when a profiler can separate stages.

## Decision

Choose one:

- [ ] accept optimization
- [ ] reject optimization
- [ ] investigate further
- [ ] acceptable regression approved for another product reason

Rationale:

## Follow-up

- Regression test/update:
- Performance budget update:
- New risk introduced:
- Next measurement:
