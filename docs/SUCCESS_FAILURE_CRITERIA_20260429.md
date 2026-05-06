# Success And Failure Criteria

## Experiment 1: Native MoE vs Emulation

Success:
- native AITER route is proven
- emulation signature disappears
- throughput improves materially

Failure:
- route remains ambiguous
- no measurable delta
- native path still not reached

## Experiment 2: Tuned GEMM vs Generic Linear

Success:
- `tgemm` route is proven on target shapes
- TTFT or per-token latency improves materially

Failure:
- route does not change
- tuned path exists but offers no gain

## Experiment 3: Dynamic MXFP4 vs Tuned GEMM

Success:
- quant overhead versus compute gain is measurable
- one path clearly dominates for the tested shape family

Failure:
- measurement cannot separate quant overhead from downstream GEMM

## Experiment 4: MLA Fusion

Success:
- fused path appears in trace
- launch count or latency meaningfully decreases

Failure:
- pass does not trigger
- no material end-to-end improvement

## Material Improvement Threshold

Initial threshold:
- `>= 5%` for “worth attention”
- `>= 10%` for “meaningful”
- `>= 20%` for “high-leverage”

These are provisional and can be tightened once AMD provides target workloads.
