# Second Target Candidate

## Candidate

Measure and instrument the hidden decision geometry around:

- `fused_qk_rmsnorm` fallback around `M=16384`
- Quark native vs emulation route choice

File:
- `aiter/ops/fused_qk_norm_rope_cache_quant.py`

## Why This Is A Good Next Runtime Target

- small
- runtime-affecting
- math-adjacent
- directly exerciseable by the optimization protocol once ROCm compute is available
- reinforced by both abstraction-focused reviewers as the highest-value measured-learning surface

## Why It Is Not Chosen As The First PR

Because it needs hardware and it is not a safe zero-behavior-change contribution.

The first PR should build trust and test coverage.
This target is where the first real runtime measurement work should begin.

## What Needs To Happen Before Behavior Change

1. one real ROCm trace
2. structured branch tracing around the fused cutoff
3. timers around Quark preprocess vs forward
4. a small capability or cost table before any threshold edit

## Immediate Measured Experiments

### First Runtime Priority: Fused QK RMSNorm

Instrument and sweep first:

- branch choice at `_FUSED_QK_FALLBACK_M = 16384`
- values around the threshold
- hold dtype, head-dim, hardware, and route flags fixed
- record route, launch count, memory, and throughput

### Second Runtime Priority: Quark

Instrument and sweep after the fused threshold pass:

- `process_weights_after_loading`
- `apply_weights`
- `M={1,8,32,64}` or equivalent small-row regimes
- compare native vs emulation
- compare scale computation inside vs outside the op where possible

## Success Condition

The candidate is only worth patching if we can defend:

- that a measured crossover exists
- that the current split is too blunt
- that the proposed behavior change is better on real evidence
