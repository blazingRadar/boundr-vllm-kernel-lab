# AITER Tuned-Config Coverage Audit

## Scope

This is a static audit of public AITER tuned-config assets already present in:
- `aiter/aiter/configs/` in a local ignored checkout of `ROCm/aiter`
- `aiter/aiter/configs/model_configs/` in that checkout
- `aiter/op_tests/op_benchmarks/triton/model_benchmarking_tool/model_shapes.json` in that checkout

## Strong Finding

The public AITER tree already contains model-specific tuned-config inventory for exactly the families we care about:
- DeepSeek / DSV3
- Kimi-K2
- Qwen3 / Qwen3.5

This means the next contribution surface is not speculative. There is already a live tuning-asset substrate to extend.

## Evidence

Present model-specific tuned files include:
- `dsv3_bf16_tuned_gemm.csv`
- `dsv3_a4w4_blockscale_tuned_gemm.csv`
- `dsv3_fp4_tuned_fmoe.csv`
- `kimik2_bf16_tuned_gemm.csv`
- `kimik2_fp4_tuned_fmoe.csv`
- `qwen3_5_397b_fp4_tuned_fmoe.csv`
- `a8w8_blockscale_tuned_gemm_ds_v3.csv`
- `a8w8_blockscale_tuned_fmoe_ds_v3.csv`

This is already richer than a generic “ROCm supports vLLM” claim. It suggests AMD/AITER are maintaining per-model shape packs, but the seam between those assets and actual route selection is still where external research can add value.

## Sample Observations

### DeepSeek-family BF16 GEMM coverage exists

Example from `dsv3_bf16_tuned_gemm.csv`:
- tuned rows for `K=7168`
- low-`M` decode-like shapes
- `libtype=flydsl`

This is consistent with the April 29 tuned-GEMM path work in `6841f5d...`.

### DeepSeek-family FP4 FMoE coverage exists

Example from `dsv3_fp4_tuned_fmoe.csv`:
- tuned rows for:
  - `model_dim=7168`
  - `inter_dim=256`
  - `topk=9`
- kernel names include both FlyDSL and CK MoE components

This matters because it shows the route-selection problem is occurring in a landscape where tuned assets already exist.

### Kimi-K2 has its own BF16 tuned GEMM surface

Example from `kimik2_bf16_tuned_gemm.csv`:
- tuned rows with `N=384`, `K=7168`

That makes the MLA fusion lane more interesting, because Kimi-K2 is not just a DeepSeek-adjacent architecture; AITER already contains family-specific shape coverage for it.

## Why This Matters

The strongest implication is:
- if performance is still poor, it may not be because tuned assets do not exist
- it may be because:
  - the wrong route is selected
  - the target runtime shape falls outside the tuned subset
  - the tuned assets are present but not integrated into the actual vLLM path being exercised

## Immediate Next Questions

1. For the exact underperforming AMD workload, do the runtime shapes hit existing tuned entries?
2. If not, is the miss because of:
   - `M` mismatch
   - `N/K` mismatch
   - dtype mismatch
   - route mismatch
3. If yes, why is the tuned path still not winning?

## Use In AMD Conversation

This gives a stronger external posture:
- “We are not guessing whether tuned assets exist.”
- “We can already see public model-specific tuned coverage for DeepSeek/Kimi/Qwen families.”
- “Our job is to prove whether production shapes are actually reaching that coverage.”
