# Open Items

## Blocked On Compute

- first real ROCm trace
- native-vs-emulation benchmark proof
- tuned GEMM on/off benchmark proof
- fused `M=16384` branch sweep around the current fallback cutoff

## Ready Without Compute

- launch-readiness gap detector design
- retroactive episode framing
- AITER tuned-config coverage audit
- emulation signature taxonomy
- auto-tuning loop prototype design
- model-shape to tuned-config diffing
- two-agent code exploration memo
- ranked first-PR patch plan

## Next Non-Compute Build Step

- draft the first PR patch plan in file-level detail before touching upstream code
- record abstraction feedback that refines post-hardware experiment ordering

## Current Local Test Blocker

- upstream `pytest` targets currently fail early in this lab clone because `tblib` is missing from the test environment
- after lab-local bootstrap, the next shared import blocker is `openai_harmony`
- after further bootstrap, the next shared import blocker is `pybase64`

## In-Progress Contribution State

- first PR code draft exists in the cloned `vllm-upstream` workspace
- lightweight syntax validation passed on the two touched test files
- full targeted pytest execution remains blocked by shared upstream test-environment breadth

## Recommended Tight Scope

Do not add new lanes until:
- at least one real ROCm trace exists
- or the launch-gap retroactive v1 packet is built
