# Optimization Hypothesis Register

## H1

Wrong backend route is forcing supported quantized MoE paths into emulation.

Expected leverage:
- high

Evidence to seek:
- trace showing fallback/emulation before fix and native path after fix

## H2

Dynamic MXFP4 quantization overhead outweighs its savings on some DeepSeek-family attention projection layers.

Expected leverage:
- high

Evidence to seek:
- time spent in quantization region versus end-to-end speedup

## H3

AITER tuned GEMM coverage is a larger near-term win than deeper quant-path work for selected BF16/FP16 shapes.

Expected leverage:
- high

Evidence to seek:
- `tgemm` route plus benchmark delta

## H4

Fusion opportunities on MLA-heavy paths may yield cleaner wins than generic low-level kernel work.

Expected leverage:
- medium to high

Evidence to seek:
- trace collapse and launch-count reduction

## H5

Some AITER fallback thresholds or shape-coverage gaps are too conservative for real DeepSeek-family workloads.

Expected leverage:
- medium

Evidence to seek:
- route logs plus tuned-file misses on common shapes

## H6

The next best improvement belongs in AITER tuning assets and CSV/config coverage rather than in vLLM code.

Expected leverage:
- medium

Evidence to seek:
- repeated tuned-path misses for common shapes despite correct vLLM routing
