# Code And Math Review Packet — Quark OCP MX

## File

- `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py`

## Why This File

This is the clearest current bridge between:
- route logic
- quantization format
- emulation
- and real GEMM path selection

It is the best first file for quants to review because it is close to the actual runtime decision but still readable.

## Critical Region

Start here:
- `vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx.py:205`

Important lines:
- emulation decision:
  - `205`
- missing-kernel dependency gate:
  - `214`
- emulation warning path:
  - `222`
- dynamic MXFP4 weight processing:
  - `261`
- runtime path split:
  - `271`

## What The Math Is Doing

At a very high level:
- represent weights and maybe activations in MXFP4 or MXFP6 forms
- if native path is unavailable, simulate low-precision behavior using higher-precision math
- otherwise prepare the data layout for lower-precision GEMM

This is where the “4-bit versus 8-bit versus high-precision fallback” story becomes real code.

## Review Questions

1. Is the emulation decision too coarse?
2. Are there dtype combinations that should be native but are currently forced into emulate?
3. Does dynamic MXFP4 preprocessing look like it could erase the expected speed win?
4. Is there an obvious place where route explanation should be made more explicit?

## What A Good Quant Review Looks Like

Not:
- “rewrite the kernel”

Instead:
- identify where a native route is blocked
- identify where quant overhead may dominate gains
- identify where the route logic looks too blunt for the actual dtype/shape space
