# vLLM To AITER Dependency Matrix

## 1. Tuned GEMM

vLLM surface:
- `vllm/model_executor/layers/utils.py`
- `vllm/_aiter_ops.py`

AITER surface:
- `aiter/tuned_gemm.py`
- `aiter/configs/bf16_tuned_gemm.csv` path family
- `gradlib/gradlib/GemmTuner.py`

Dependency shape:
- vLLM decides whether `tgemm.mm(...)` is reachable
- AITER decides whether a tuned config exists for the shape and what backend implementation runs:
  - torch
  - skinny
  - hipblaslt
  - asm
  - flydsl

## 2. Dynamic MXFP4 Quant + FP4 GEMM

vLLM surface:
- `vllm/model_executor/layers/quantization/quark/quark.py`
- `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py`

AITER surface:
- `aiter/ops/triton/quant`
- `aiter/utility/fp4_utils.py`
- `aiter/ops/triton/gemm_afp4wfp4`
- `aiter` optional:
  - `gemm_a4w4`
  - `per_1x32_f4_quant_hip`

Dependency shape:
- vLLM chooses whether dynamic MXFP4 is used
- AITER performs quantization and the downstream FP4 GEMM path

## 3. MoE Native Path

vLLM surface:
- `vllm/model_executor/layers/fused_moe/rocm_aiter_fused_moe.py`
- `vllm/model_executor/layers/quantization/quark/quark_moe.py`

AITER surface:
- fused MoE runtime exposed through `vllm/_aiter_ops.py`
- AITER fused MoE kernels and quant types behind lazy bindings

Dependency shape:
- vLLM scheme classification decides native versus emulation
- AITER provides the native fused MoE implementation

## 4. MLA Dual RMS Norm Fusion

vLLM surface:
- `vllm/compilation/passes/fusion/rocm_aiter_fusion.py`
- `vllm/config/vllm.py`
- `vllm/config/compilation.py`
- `vllm/_aiter_ops.py`

AITER surface:
- `aiter/ops/fused_qk_norm_rope_cache_quant.py`
  - `fused_qk_rmsnorm`

Dependency shape:
- vLLM compiler pass recognizes the graph pattern
- AITER provides the fused kernel
- AITER itself contains a fallback threshold:
  - `_FUSED_QK_FALLBACK_M = 16384`

## Working Conclusion

The highest-leverage external research lane is likely at the seam:
- vLLM route policy
- AITER tuned asset availability
- AITER fallback thresholds
- shape-specific enablement gaps
