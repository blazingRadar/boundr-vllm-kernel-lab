# Touched File Ledger — `ec8ab9d...`

| File | Layer | Likely Performance Role | Evidence Needed |
|---|---|---|---|
| `vllm/model_executor/layers/quantization/quark/quark.py` | quant policy | introduces dynamic MXFP4 enablement for DeepSeek-family projection layers | benchmark and trace separating quant overhead from GEMM savings |
| `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py` | quant/backend integration | wires dynamic MXFP4 quantization, packed weight handling, and AITER GEMM route | trace of quant region plus end-to-end latency |

## Hot Path Hypothesis

This was the originating experiment that later appears to have been partially rolled back in favor of tuned GEMM for some attention paths.
