# First Sprint Closeout

## Completed

- isolated top-level lab created
- non-interference boundary written
- public workspaces cloned:
  - `vllm-project/vllm`
  - `ROCm/aiter`
- four target commits pinned and audited
- touched-file changes classified by layer
- benchmark matrix drafted
- trace checklist drafted

## Strongest Current Finding

The public DeepSeek-family ROCm/vLLM optimization story is not primarily “one missing kernel.”

It is a mixed control surface of:
- backend-path selection
- emulation avoidance
- tuned GEMM enablement
- quant policy reversal
- one real architecture-specific fusion pass

## Why This Matters

That means a small outside team can contribute real value before attempting any new low-level kernel math:
- prove wrong-path routing
- produce trace-backed benchmark evidence
- identify where AITER tuned assets are underused
- separate policy mistakes from genuine kernel limitations

## Recommended Next Sprint

1. generate commit-level touched-file ledgers with exact hot-path hypotheses
2. pin public AITER files linked to:
   - tuned GEMM
   - dynamic MXFP4 quant
   - fused QK RMS norm
3. build the first benchmark manifest
4. build the first trace collection wrapper
5. prepare for real compute runs once hardware is available
