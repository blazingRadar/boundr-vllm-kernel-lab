# Touched File Ledger — `944e138...`

| File | Layer | Likely Performance Role | Evidence Needed |
|---|---|---|---|
| `vllm/model_executor/layers/fused_moe/rocm_aiter_fused_moe.py` | runtime dispatch | classifies MXFP4 MoE quant method and routes to native AITER fused MoE | trace showing native fused MoE kernels instead of emulation |
| `vllm/model_executor/layers/quantization/quark/quark_moe.py` | quant/backend policy | expands `_AITER_NATIVE_OCP_MX_SCHEMES` to include `w_mxfp4_a_mxfp4` | route evidence plus tokens/sec comparison |

## Hot Path Hypothesis

The largest gain here should come from removing emulation on a path that was already supposedly supported.
