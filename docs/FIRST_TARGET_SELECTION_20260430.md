# First Target Selection

## Selected First Target

Add clearer route-diagnostic reporting for ROCm Quark OCP MX paths that fall into emulation or native execution.

Primary code surfaces:
- `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py`
- `vllm/model_executor/layers/quantization/quark/quark_moe.py`

## Why This Target

This is the best first target because it is:
- small
- reviewable
- directly tied to the dominant gap class:
  - `dispatch_route_gap`
- useful even before we have stable ROCm compute access

## What Problem It Addresses

Today, the public code does log warning text for emulation, but the route state is still scattered across:
- `supports_mx`
- quant dtype combinations
- `use_rocm_aiter_moe`
- backend enum state
- scheme strings like `w_mxfp4_a_mxfp4`

That makes it harder to answer a simple reviewer question:
- why exactly did this path go native versus emulated?

## Why Not A Kernel First

Because the commit history already shows large wins from route correctness without new math.

Examples:
- `944e138...`
- `6841f5d...`

So the right first contribution is to improve observability on that route surface, not to speculate about deeper math immediately.

## What Success Would Look Like

A reviewer can see:
- exact path classification
- exact reason native path was or was not selected
- enough evidence to debug route issues faster

## What This Unlocks Next

If accepted, this sets up stronger future work in:
- route evidence tooling
- trace correlation
- smaller route fixes with better diagnostics
