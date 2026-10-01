# Performance report template

## Candidate

- product version:
- build:
- git SHA:
- binary SHA-256:
- compiler/toolchain:
- AE SDK:

## Baseline

- product version:
- build:
- binary SHA-256:

## Environment

- After Effects exact build:
- OS:
- CPU:
- CPU architecture:
- RAM:
- GPU:
- GPU driver:
- power/thermal mode notes:

## Scenario

- fixture/project:
- fixture hash/version:
- resolution:
- duration/frames:
- bit depth:
- working space if relevant:
- MFR:
- GPU backend:
- cache state: cold/warm
- repetitions:

## Correctness prerequisite

- golden fixture:
- comparison metric:
- tolerance:
- candidate correctness: PASS / FAIL
- diff artifact:

If FAIL, performance result cannot approve release.

## Results

| Metric | Baseline | Candidate | Delta | Threshold | Result |
|---|---:|---:|---:|---:|---|
| cold first frame | | | | | |
| warm median frame | | | | | |
| p95 frame | | | | | |
| p99 frame | | | | | |
| full render | | | | | |
| peak memory | | | | | |
| steady retained memory | | | | | |
| CPU utilization | | | | | |
| lock wait | | | | | |
| GPU transfer | | | | | |
| GPU compute | | | | | |
| cache hit rate | | | | | |

## Raw sample summary

- sample count:
- min:
- median:
- p95:
- max:
- standard deviation/noise estimate:

Raw results location:

## MFR scaling

| Mode/workers | Wall time | Speedup | Peak memory | Notes |
|---|---:|---:|---:|---|
| off | | 1.0x | | |
| on | | | | |

## GPU breakdown

| Stage | Baseline | Candidate |
|---|---:|---:|
| setup/buffer acquisition | | |
| upload | | |
| kernel/compute | | |
| sync | | |
| download/conversion | | |

## Profiling evidence

- profiler:
- trace:
- allocation report:
- lock/contention report:
- GPU trace:

## Interpretation

What changed and why?

Separate measured facts from hypothesis.

## Decision

- [ ] accept
- [ ] accept with documented tradeoff
- [ ] investigate
- [ ] reject

Reason:

Approved by:

Date:
