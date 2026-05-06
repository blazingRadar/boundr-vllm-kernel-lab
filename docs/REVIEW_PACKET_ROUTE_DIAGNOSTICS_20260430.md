# Review Packet — Route Diagnostics For Quark OCP MX

## Patch Class

- route diagnostics
- benchmark / trace tooling support

## Problem

The current ROCm Quark OCP MX path has meaningful native-versus-emulation branching, but the route explanation is spread across multiple booleans and warnings.

This makes it harder to answer:
- why did this path emulate?
- why did it select native?
- which exact condition blocked native execution?

This matters because the lab's highest-ranked bottleneck class is `dispatch_route_gap`.

## Evidence

### Public commit lineage

- `944e138...` fixed a native path that was incorrectly treated as unsupported
- `6841f5d...` changed route policy for dynamic MXFP4 versus tuned GEMM

### Public code surfaces

In `quark_ocp_mx.py`:
- route depends on:
  - `current_platform.supports_mx()`
  - `input_dtype`
  - `weight_dtype`
  - availability of `dynamic_mxfp4_quant`
  - availability of `gemm_afp4wfp4`

In `quark_moe.py`:
- route depends on:
  - `ocp_mx_scheme`
  - `_AITER_NATIVE_OCP_MX_SCHEMES`
  - `use_rocm_aiter_moe`
  - backend enum state

## Proposed Change

Small change only:
- introduce a structured route-reason helper or equivalent debug string assembly
- emit a single, explicit route summary for the relevant path

Example information to expose:
- `native` or `emulate`
- `supports_mx`
- `ocp_mx_scheme`
- `input_dtype`
- `weight_dtype`
- `use_rocm_aiter_moe`
- `native_scheme_supported`
- `missing_kernel_dependency`

## Expected Runtime Effect

No intended math-path speed change by itself.

Expected effect:
- faster diagnosis
- clearer trace-to-code correlation
- lower reviewer uncertainty on future route patches

## Risk

Low, if kept to diagnostics only.

Main risk:
- noisy logging
- too much detail in non-debug paths

That can be managed by:
- debug-level route reporting
- or a concise single summary line

## Why This Is A Good First Contribution

- does not pretend to solve kernel math first
- directly targets the dominant gap class
- creates a better base for later route fixes
- plausibly reviewable by an AMD engineer without demanding large validation burden

## Questions For Reviewer

1. Would a structured route summary be useful in practice for ROCm quant-path debugging?
2. Should it live as:
   - warning text
   - debug text
   - or a helper method returning a structured reason string?
3. Is there a preferred place to surface native-versus-emulation route state for future trace tooling?
