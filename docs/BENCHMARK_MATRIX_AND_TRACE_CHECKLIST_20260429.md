# Benchmark Matrix And Trace Checklist

## Benchmark Matrix

The first benchmark matrix should isolate route-policy effects before broader optimization work.

### Axis A: Commit Family

- baseline before `ec8ab9d...`
- `ec8ab9d...`
- `6841f5d...`
- `944e138...`
- `fb5635d...`

### Axis B: Path Mode

- dynamic MXFP4 enabled
- dynamic MXFP4 disabled
- AITER tuned GEMM enabled
- AITER tuned GEMM disabled
- AITER MoE enabled
- forced fallback / emulation if reproducible

### Axis C: Model Family

- DeepSeek-family attention-projection-heavy path
- DeepSeek-family MoE-heavy path
- MLA/Kimi-K2 style path if available

### Axis D: Metrics

- prompt tokens/sec
- generation tokens/sec
- TTFT
- latency per output token
- peak memory
- observed backend route
- hottest kernels

## Trace Checklist

For every serious run, capture:

1. hardware id
   - exact GPU
   - ROCm version

2. software id
   - vLLM commit
   - AITER commit
   - container/build notes

3. route evidence
   - env flags used
   - whether AITER is enabled
   - whether tuned GEMM is enabled
   - whether MoE path is native or emulated

4. profiler evidence
   - tool used
   - hottest kernels
   - launch counts
   - suspicious stalls
   - fallback signatures

5. layer attribution
   - attention projection
   - MoE
   - MLA fusion region
   - dynamic quant region

## First Questions To Settle

1. Does native AITER MoE remove a dominant emulation cost?
2. Does tuned GEMM beat dynamic MXFP4 in the target DeepSeek-family attention projection layers?
3. Is the MLA dual RMS norm fusion visible in trace and material in end-to-end metrics?

## Exit Condition For Sprint 2

Have at least one benchmark packet and one trace packet that cleanly proves:
- which route was expected
- which route actually ran
- what performance changed
