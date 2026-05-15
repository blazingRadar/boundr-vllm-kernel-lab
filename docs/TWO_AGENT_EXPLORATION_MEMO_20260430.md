# Two-Agent Exploration Memo

## Purpose

This memo records the results of a bounded two-agent exploration pass over the public ROCm/vLLM/AITER code surfaces already under study in this lab.

The goal was not to invent a new kernel.
The goal was to identify the best near-term ways to improve the lane before hardware-backed optimization claims:

- better route correctness
- better feature gating
- better emulation diagnostics
- better test coverage
- better first-PR target selection

## Boundary

This work stayed inside the existing public-only lab boundary:

- public `vllm-project/vllm`
- public `ROCm/aiter`
- no other Boundr lab touched
- no non-public AMD code
- no hardware-backed claims

## Inputs

The exploration was anchored to the code/math packets already prepared in this lab:

- `docs/CODE_MATH_REVIEW_PACKET_QUARK_OCP_MX_20260430.md`
- `docs/CODE_MATH_REVIEW_PACKET_FUSED_QK_RMSNORM_20260430.md`
- `docs/SECOND_TARGET_CANDIDATE_20260430.md`
- `docs/QUANT_REVIEW_PROMPT_20260430.md`

## Agent Scope

### Agent 1

Explored the ROCm Quark OCP MX route/emulation surface in:

- `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py`
- linked AITER FP4 / Triton / quant surfaces

### Agent 2

Explored the fused QK RMSNorm / MLA fusion surface in:

- `aiter/ops/fused_qk_norm_rope_cache_quant.py`
- `vllm/compilation/passes/fusion/rocm_aiter_fusion.py`
- `vllm/_aiter_ops.py`

## Findings

### Finding 1

The strongest contribution surface is still route correctness and observability, not new kernel math.

This agrees with the public commit evidence already driving the lab:

- `944e138...`
- `6841f5d...`
- `fb5635d...`
- `ec8ab9d...`

The new agent pass reinforces that read at the file level.

### Finding 2

The Quark OCP MX path still relies on brittle routing mechanisms.

The most important issues found were:

- hardcoded tuned-shape gating instead of stronger capability-driven checks
- a deprecated AITER call still used from vLLM
- a coarse `emulate` state with weak structured reasoning
- weak route-selection test coverage

This means the code is still harder to audit than it should be, even before discussing performance.

### Finding 3

The fused QK RMSNorm / MLA surface has good positive-path intent but weaker gating and fallback transparency.

The most important issues found were:

- broad feature gating
- symbol-presence probes that are weaker than true capability probes
- a hardcoded fallback threshold with little diagnostic surface
- thin negative / fallback-path test coverage

This means the fusion path may be functionally correct while still being difficult to reason about when it does not activate cleanly.

### Finding 4

The best first contributions remain small, reviewable, and diagnostic-heavy.

The exploration did not surface a credible first move of the form:

- rewrite the kernel
- change low-level math geometry
- retune thresholds blindly

Instead it surfaced safe near-term contribution classes:

- route/emulation reason reporting
- deprecated API cleanup
- negative-path test coverage
- tighter feature gating
- debug-only fallback diagnostics

## Quark OCP MX Detail

### Hardcoded route gating

The path into preshuffled Triton kernels is still partly governed by hardcoded shape gating.

That is a code smell because it couples route choice to a static list rather than a clearer capability or tuned-config query.

This is probably important, but changing it is not the right first PR without hardware evidence.

### Deprecated AITER API usage

vLLM still appears to call a deprecated AITER API on the FP4 path.

This is a high-quality first-fix candidate because it is:

- concrete
- local
- reviewable
- low political surface area

### Emulation-state opacity

The route state is still too coarse.

We need a structured answer to questions like:

- why native was rejected
- why emulation was chosen
- whether the blocker was dtype, shape, backend, capability, or policy

That is exactly the kind of reviewer-facing improvement that can land before deeper optimization work.

### Test weakness

The route-selection test surface looks thinner than it should be for a path this sensitive.

That means the lane needs more negative-path assertions before it should attempt bolder runtime behavior changes.

## Fused QK RMSNorm / MLA Detail

### Broad pass gating

The fusion pass appears enabled by broad availability checks rather than the narrowest subfeature checks.

That is a classic integration risk:

- pass present
- symbol present
- but the exact subfeature state may still be wrong

Tightening that gate is a good contributor-level improvement.

### Hardcoded fallback threshold

The fallback threshold is a fixed constant.

That alone is not bad, but today it lacks:

- structured diagnostics
- a clean debug seam
- strong negative-path tests

The first move should be visibility, not numerical change.

### Probe weakness

Checking that a symbol imports is weaker than checking that the runtime capability is actually ready.

This is another good contributor-level target because it improves correctness expectations without pretending to tune the kernel.

## What The Exploration Changes

Before the two-agent pass, the lab already suspected that route correctness dominated.

After the two-agent pass, the lab has stronger code-level support for this claim:

- the first patch should not be a performance patch
- the first patch should improve auditability of runtime path choice
- the second patch should be a small runtime-affecting route or gate improvement
- threshold and policy changes should wait for ROCm evidence

## Recommended Ranked Actions

### Tier 1

Do now, before hardware:

- add structured route/emulation reason reporting to Quark OCP MX
- replace deprecated AITER API usage in vLLM
- add negative-path and route-selection tests
- tighten MLA fusion gating to specific subfeature checks
- add debug-only diagnostics for fused fallback selection

### Tier 2

Do after first ROCm evidence:

- revisit hardcoded tuned-shape route gating
- revisit dynamic MXFP4 path policy
- evaluate fallback threshold behavior under real trace data

### Tier 3

Do not do yet:

- speculative kernel rewrites
- blind threshold retuning
- low-level math changes without route and trace evidence

## Best First PR Direction

The best first PR direction is still:

- **structured route/emulation reason reporting for Quark OCP MX**

Why:

- it aligns with the top lab thesis:
  - `dispatch_route_gap`
- it is small enough for external review
- it helps all later perf work
- it improves reviewer trust
- it does not require us to overclaim hardware results

## Honest Status

This memo improves the lab's reasoning quality.
It does not by itself prove a performance win.

The correct claim remains:

- the lab is getting better at choosing the right first contribution surfaces
- the lab is not yet claiming ROCm optimization results

## Next Artifact

The next artifact after this memo is a ranked patch plan that chooses one concrete first PR target and stages the next patch behind it.
