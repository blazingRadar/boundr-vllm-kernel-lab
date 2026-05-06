# Commit Audit — `ec8ab9d254d3b2e6b919a55277da599a7b9ab146`

PR:
- `#34157`

Title:
- `[ROCm] Add dynamic mxfp4 quantization for DeepSeek V2 projection layers`

## Touched Files

- `vllm/model_executor/layers/quantization/quark/quark.py`
- `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py`

## Classification

- dispatch logic: **yes**
- quant path: **yes**
- fusion path: **no**
- wrapper/op binding: **yes**
- backend integration: **yes**
- benchmark or test only: **no**

## What Actually Changed

This earlier commit introduced dynamic MXFP4 quantization for DeepSeek-family projection layers.

Important behaviors:
- `maybe_update_config(...)` detected `deepseek_v3` + `fp4`
- enabled `dynamic_mxfp4_quant`
- selectively re-quantized attention projection layers
- added dynamic quant handling inside `QuarkOCP_MX`
- changed weight creation and loading behavior for this path

The low-level external dependency route includes:
- `aiter.ops.triton.quant.dynamic_mxfp4_quant`
- `gemm_afp4wfp4`
- optional `gemm_a4w4` ASM path

## Read

This appears to be the origin point for a later policy reversal.

By April 29, the follow-up commit `6841f5d...` effectively disabled this auto-enable logic and replaced it with explicit tuned GEMM routing for some layers.

That suggests:
- the original idea was technically viable
- but the net performance tradeoff was not consistently favorable

## Likely Performance Surface

- quantize-on-the-fly overhead
- attention projection layer compute savings
- weight packing/shuffle effects
- hardware and shape sensitivity

## Research Value

High, but mostly as lineage.

This is valuable because it frames the later question:
- was the problem the quant kernel itself
- the dispatch policy
- the model/layer selection
- or the total cost of dynamic re-quantization

## Suggested Benchmark

- reproduce dynamic MXFP4 on the targeted projection layers
- compare against:
  - tuned unquantized GEMM
  - static/non-dynamic alternatives if available
- watch TTFT and per-token latency separately

## Suggested Trace Question

How much time is spent in dynamic quantization itself relative to the GEMM it is supposed to accelerate?
