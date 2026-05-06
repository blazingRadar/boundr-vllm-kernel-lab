# Retroactive Episodes V1

## Purpose

Build a falsifiable retroactive packet instead of a speculative infrastructure claim.

## Candidate Episodes

### Episode 1

- model family: DeepSeek-V3 / DeepSeek-R1-adjacent ROCm bring-up
- likely surfaces:
  - route correctness
  - tuned GEMM policy
  - MXFP4 quant policy

### Episode 2

- model family: Kimi-K2
- likely surfaces:
  - MLA fusion
  - BF16 tuned GEMM coverage
  - FP4 FMoE coverage

### Episode 3

- model family: Qwen3-MoE / Qwen3.5 large MoE
- likely surfaces:
  - MoE tuned-config coverage
  - dispatch route classification

## For Each Episode

Capture:
- `t0` public model shape inventory
- `t0` public AITER kernel inventory
- `t0` public AITER tuned-config inventory
- `t0` public vLLM route state
- later public closing commits

Output:
- dominant gap class at `t0`
- secondary gap classes
- public close events over time

## Success Condition

At least one episode should yield a defensible answer to:
- was launch lag mostly:
  - coverage
  - tuning
  - route

That is enough to direct v2 correctly.
