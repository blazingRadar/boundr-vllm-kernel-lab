# Touched File Ledger — `fb5635d...`

| File | Layer | Likely Performance Role | Evidence Needed |
|---|---|---|---|
| `vllm/_aiter_ops.py` | wrapper/binding | registers `fused_mla_dual_rms_norm` custom op backed by AITER fused QK RMS norm | trace proving custom op region appears |
| `vllm/compilation/passes/fusion/rocm_aiter_fusion.py` | fusion pass | pattern-matches MLA dual RMS norm and rewrites graph | compile logs plus trace region collapse |
| `vllm/compilation/passes/pass_manager.py` | compiler wiring | enables the pass under pass config | run config evidence |
| `vllm/config/compilation.py` | config gating | ROCm-only validation for fusion pass | config state capture |
| `vllm/config/vllm.py` | optimization policy | includes the fusion in optimization levels | run config plus benchmark |
| `tests/compile/passes/test_fuse_mla_dual_rms_norm.py` | test | validates pass shape | none for perf |
| `docs/design/fusions.md` | docs | describes pass | none |
| `docs/design/optimization_levels.md` | docs | lists enablement | none |

## Hot Path Hypothesis

This should help by reducing launch count and normalization overhead on MLA-heavy DeepSeek/Kimi-K2 paths.
