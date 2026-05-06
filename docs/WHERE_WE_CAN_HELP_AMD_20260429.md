# Where We Can Help AMD

Date:
- 2026-04-29

## Position

We should not claim immediate value by inventing a new ROCm kernel first.

We can credibly help AMD by reducing uncertainty around which launch-readiness gap class is actually blocking a new DeepSeek-family ROCm/vLLM path.

## Best Help Surfaces

### 1. Path-Execution Verification

Goal:
- prove which backend path is actually running

Why it matters:
- a supported path falling into emulation can erase large amounts of performance
- route mistakes are cheaper to fix than brand-new kernel development

### 2. Quant-Path Tradeoff Measurement

Goal:
- measure when dynamic MXFP4 helps versus hurts

Why it matters:
- public upstream changes strongly imply that dynamic MXFP4 was not always a net win
- this likely varies by layer shape, model family, and hardware

### 3. Tuned GEMM Opportunity Isolation

Goal:
- identify where AITER tuned GEMMs outperform generic fallback or dynamic quant paths

Why it matters:
- this may be the highest-leverage near-term speed surface on attention projection layers

### 4. MoE Native-vs-Emulation Audit

Goal:
- prove when MoE quant paths are native and when they are silently emulated

Why it matters:
- the public W4A4 fix suggests there may be more route correctness opportunities nearby

### 5. Fusion Impact Verification

Goal:
- test whether MLA dual RMS norm fusion produces meaningful end-to-end gains

Why it matters:
- if it does, similar architecture-specific fusion opportunities may be a better frontier than generic kernel work

## What We Need From AMD

- access to the exact model family and shapes that are underperforming
- hardware identity
- profiler traces or permission to collect them
- current flag/config surface
- target metric:
  - TTFT
  - decode latency
  - tokens/sec

## What We Can Deliver

- launch-readiness gap-classification report
- route-correctness audit
- benchmark matrix
- trace-backed bottleneck report
- optimization hypothesis register
- recommendation on whether the next work belongs in:
  - vLLM
  - AITER
  - tuning/config
  - or deeper kernel invention
