# Layer Classification

## Current Read

The public AMD ROCm/vLLM DeepSeek-family work splits into four layers:

### 1. Route Policy

Examples:
- `944e138...`
- `6841f5d...`

This layer decides:
- whether a supported path reaches AITER or falls into emulation
- whether dynamic MXFP4 is enabled or not
- whether tuned GEMM is allowed to run

This is likely where large avoidable losses occur.

### 2. Wrapper And Binding Layer

Examples:
- `vllm/_aiter_ops.py`
- `vllm/model_executor/layers/utils.py`
- `vllm/model_executor/layers/quantization/quark/*.py`

This layer exposes AITER ops into vLLM and decides which backend path is called.

It is not the deepest kernel layer, but it can still dominate outcomes if it selects the wrong path.

### 3. Fusion / Compiler Pass Layer

Example:
- `fb5635d...`

This layer changes graph shape and execution structure before runtime dispatch.

This is a meaningful optimization surface independent of quant routing.

### 4. Low-Level AITER / ROCm Kernel Substrate

Observed public evidence in `ROCm/aiter`:
- tuned GEMM infrastructure in `aiter/tuned_gemm.py`
- dynamic MXFP4 quant in `aiter/ops/triton/quant` and utility paths
- fused QK RMS norm path
- a4w4 and a16w16 tuning infrastructure

This is where actual kernel math and tuning assets live, but the current vLLM target commits mostly touch the upper integration and routing surfaces.

## Working Thesis

The first realistic external contribution surface is not inventing a brand-new kernel immediately.

It is:
- proving route correctness
- measuring path selection
- classifying when emulation or generic fallback occurs
- identifying where AITER tuned assets are underused or wrongly gated
