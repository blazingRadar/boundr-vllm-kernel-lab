# Touched File Ledger — `6841f5d...`

| File | Layer | Likely Performance Role | Evidence Needed |
|---|---|---|---|
| `vllm/_aiter_ops.py` | wrapper/binding | exposes `is_tgemm_enabled()` gate for AITER tuned GEMM path on `gfx950` | route evidence plus trace proving `tgemm` path ran |
| `vllm/envs.py` | route policy | adds env-controlled enablement surface for AITER tuned GEMM behavior | exact run flags and route logs |
| `vllm/model_executor/layers/quantization/quark/quark.py` | quant policy | removes DeepSeek-family auto-enable policy for dynamic MXFP4 quantization | benchmark comparing dynamic MXFP4 on/off |
| `vllm/model_executor/layers/utils.py` | runtime dispatch | inserts `tgemm.mm(...)` path before generic linear fallback | trace plus throughput delta |
| `tests/quantization/test_quark_maybe_update_config.py` | test | removed after policy reversal | none for performance, only lineage |

## Hot Path Hypothesis

The likely win is not new math. It is that some attention projection shapes run faster through tuned unquantized GEMM than through dynamic MXFP4 quantization plus its overhead.
