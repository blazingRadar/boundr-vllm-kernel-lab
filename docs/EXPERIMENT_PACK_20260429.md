# Experiment Pack

## Experiment 1: Native MoE vs Emulation

Goal:
- prove whether the target W4A4/MXFP4 MoE path is running native AITER or falling into emulation

Primary commits:
- `944e138...`

Expected toggles:
- `VLLM_ROCM_USE_AITER=1`
- `VLLM_ROCM_USE_AITER_MOE=1`

Primary outputs:
- generation tokens/sec
- TTFT
- trace evidence of native fused MoE path

## Experiment 2: Tuned GEMM vs Generic Linear

Goal:
- prove whether `tgemm` improves DeepSeek-family attention projection layers

Primary commits:
- `6841f5d...`

Expected toggles:
- `VLLM_ROCM_USE_AITER=1`
- `VLLM_ROCM_USE_AITER_LINEAR=1`
- `VLLM_ROCM_USE_AITER_TRITON_GEMM=1`

Comparison:
- `tgemm` enabled
- AITER disabled or route disabled as baseline

## Experiment 3: Dynamic MXFP4 vs Tuned GEMM

Goal:
- settle whether dynamic MXFP4 overhead outweighs its savings on the target layer family

Primary commits:
- `ec8ab9d...`
- `6841f5d...`

Primary outputs:
- TTFT
- prompt tokens/sec
- trace time spent in quantization region

## Experiment 4: MLA Dual RMS Norm Fusion

Goal:
- prove whether the fusion pass materially improves MLA-heavy DeepSeek/Kimi-K2 style paths

Primary commits:
- `fb5635d...`

Primary outputs:
- TTFT
- per-token decode latency
- kernel launch count
- trace collapse of separate RMSNorm regions
