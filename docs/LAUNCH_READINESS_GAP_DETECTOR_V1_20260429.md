# Launch-Readiness Gap Detector V1

## Historical Thesis

For a new model release on ROCm/vLLM, launch lag can often be usefully inspected through three primary gap classes:

1. `kernel_coverage_gap`
2. `tuned_config_gap`
3. `dispatch_route_gap`

This framing is better than treating all lag as a tuning problem, but later audits and the 79-PR classification corpus showed that it is not exhaustive. Treat this document as the V1 hypothesis that the later audit corpus stress-tested.

## Why This Reframe Exists

The lab's initial target commit set motivated it:

- `944e138...`
  - route/policy fix
  - not new math
  - not tuning
- `6841f5d...`
  - route/policy plus tuned-GEMM enablement
  - partially tuning-adjacent
- `fb5635d...`
  - real new fusion/kernel-path capability
- `ec8ab9d...`
  - quant-path integration/policy

In this small initial sample, the public signal suggested coverage and routing were load-bearing, with tuning secondary. Later corpus results narrowed that statement: tuning remains important, and a large `OTHER` bucket means correctness, distributed-runtime, CI/build, and model-support classes must also be tracked.

## Detector Inputs

- model architecture/config
- public AITER kernel inventory
- public AITER tuned-config inventory
- vLLM dispatch logic
- trace evidence when available

## Detector Outputs

For a given model release, emit:

- `dominant_gap_class`
- `secondary_gap_classes`
- `evidence`
- `likely_close_surface`
  - AITER kernel work
  - AITER tuned-config work
  - vLLM route/policy work

## Decision Rules

### Kernel Coverage Gap

Classify as `kernel_coverage_gap` when:
- model/op shape requires a kernel family not present in public AITER/vLLM substrate
- or the only available path is a generic fallback because no native kernel/fusion exists

### Tuned Config Gap

Classify as `tuned_config_gap` when:
- the right kernel family exists
- the route can reach it
- but tuned coverage for production-hit shapes is missing or weak

### Dispatch Route Gap

Classify as `dispatch_route_gap` when:
- native path exists
- tuned asset may exist
- but runtime falls into emulation, generic eager, or wrong backend path

## V1 Deliverable

Run the detector retroactively on three public launch-lag episodes:

1. DeepSeek-V3
2. Kimi-K2
3. Qwen3-MoE

For each:
- infer `t0` public gap state
- identify later public closing commits
- classify each closure by gap class

## Non-Goal

V1 does not attempt to solve AMD's internal PR-review velocity problem.

It produces a high-quality external diagnosis packet first.
