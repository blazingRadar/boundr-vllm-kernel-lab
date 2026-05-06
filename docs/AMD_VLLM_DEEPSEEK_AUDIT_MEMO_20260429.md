# AMD vLLM DeepSeek Audit Memo

Date:
- 2026-04-29

Scope:
- public ROCm/vLLM DeepSeek-family commits merged on or around 2026-04-29
- focus on quant-kernel routing, AITER pathing, and performance-relevant backend changes

## What Shipped

### 1. Dynamic MXFP4 path pressure was reduced

Commit:
- `6841f5dc77e9200a2fa45a4bf935b23bd843bf30`

Effect:
- adds a path to use AITER tuned GEMMs for unquantized attention projection layers
- removes the earlier auto-enable logic for DeepSeek-family dynamic MXFP4 quantization in `quark.py`

Read:
- this is a signal that dynamic MXFP4 overhead was hurting net performance on some DeepSeek-family paths

### 2. A native W4A4 MoE path stopped falling into emulation

Commit:
- `944e138bcf39e9236bbfd49d98f00fb45e6cea54`

Effect:
- extends the native AITER MoE path to include `w_mxfp4_a_mxfp4`
- avoids emulation on supported hardware for a quantized MoE path

Read:
- this is a route-correctness and performance fix, not a brand new kernel

### 3. A real ROCm MLA fusion pass shipped

Commit:
- `fb5635d3f90635ce9d1acbc975baab6e911a262b`

Effect:
- adds `fused_mla_dual_rms_norm`
- wires a ROCm/AITER compile pass for DeepSeek/Kimi-K2 style MLA paths

Read:
- this is a genuine graph/fusion optimization surface

## Current Thesis

The strongest current performance story is not:
- "one missing kernel"

It is:
- backend-path selection
- emulation avoidance
- tuned GEMM enablement
- quant policy correctness
- architecture-specific fusion

## Best External Contribution Surface

Before attempting new kernel invention:
- prove which path is executing
- benchmark native versus emulated routes
- benchmark dynamic MXFP4 versus tuned GEMM
- trace MLA fusion impact

That is the shortest path to finding real speedups.
