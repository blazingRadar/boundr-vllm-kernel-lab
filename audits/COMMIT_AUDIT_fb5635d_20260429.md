# Commit Audit — `fb5635d3f90635ce9d1acbc975baab6e911a262b`

PR:
- `#39242`

Title:
- `[ROCm] Add MLA dual RMS norm fusion (Q, KV) pass for DeepSeek/Kimi-K2`

## Touched Files

- `vllm/_aiter_ops.py`
- `vllm/compilation/passes/fusion/rocm_aiter_fusion.py`
- `vllm/compilation/passes/pass_manager.py`
- `vllm/config/compilation.py`
- `vllm/config/vllm.py`
- plus docs/tests not repeated here

## Classification

- dispatch logic: **some**
- quant path: **no**
- fusion path: **yes**
- wrapper/op binding: **yes**
- backend integration: **yes**
- benchmark or test only: **no**

## What Actually Changed

This is the cleanest example in the current target set of a real optimization pass rather than a route-policy fix.

It introduces:
- a new AITER-backed custom op:
  - `fused_mla_dual_rms_norm`
- pass-manager wiring
- config flags:
  - `fuse_mla_dual_rms_norm`
- ROCm-only enablement logic

Under the hood, the AITER op binds to:
- `aiter.ops.fused_qk_norm_rope_cache_quant.fused_qk_rmsnorm`

## Read

This is a graph/fusion level optimization that likely reduces:
- kernel launch count
- intermediate memory traffic
- separate normalization overhead across Q and KV paths

It is closer to “real kernel-path optimization” than the other two April 29 commits, even though the low-level implementation still lives through AITER.

## Likely Performance Surface

- MLA-heavy DeepSeek/Kimi-K2 inference path
- decode/prefill sections where Q/KV normalization is hot
- fusion-related reduction in overhead and traffic

## Likely Correctness Surface

- pass matching correctness
- safe ROCm-only gating
- graph-shape compatibility

## Research Value

High.

This commit suggests a second research frontier distinct from quant routing:
- model-architecture-specific fusion opportunities

## Suggested Benchmark

- DeepSeek/Kimi-K2 MLA-enabled model path
- compare compile pass on vs off
- measure:
  - TTFT
  - decode latency
  - kernel launch count
  - memory bandwidth pressure if available

## Suggested Trace Question

Does this pass measurably collapse two RMS-norm shaped regions into one fused region in the trace, and is the benefit material at the token-throughput level?
