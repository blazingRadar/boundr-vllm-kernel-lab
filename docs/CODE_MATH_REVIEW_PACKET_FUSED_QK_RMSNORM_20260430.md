# Code And Math Review Packet — Fused QK RMSNorm

## File

- [fused_qk_norm_rope_cache_quant.py](/home/blazingradar/boundr-vllm-kernel-lab/workspaces/aiter/aiter/ops/fused_qk_norm_rope_cache_quant.py)

## Why This File

This is one of the simplest public kernel-adjacent files in the lane that still touches real fused math behavior.

It is useful because:
- the math idea is small enough to reason about
- the fallback threshold is explicit
- it connects directly to the MLA fusion story

## Critical Region

Start here:
- [fused_qk_norm_rope_cache_quant.py:66](/home/blazingradar/boundr-vllm-kernel-lab/workspaces/aiter/aiter/ops/fused_qk_norm_rope_cache_quant.py:66)

Important lines:
- fallback threshold:
  - [66](/home/blazingradar/boundr-vllm-kernel-lab/workspaces/aiter/aiter/ops/fused_qk_norm_rope_cache_quant.py:66)
- runtime branch:
  - [69](/home/blazingradar/boundr-vllm-kernel-lab/workspaces/aiter/aiter/ops/fused_qk_norm_rope_cache_quant.py:69)
- fallback path to separate RMSNorm calls:
  - [78](/home/blazingradar/boundr-vllm-kernel-lab/workspaces/aiter/aiter/ops/fused_qk_norm_rope_cache_quant.py:78)
- fused kernel path:
  - [83](/home/blazingradar/boundr-vllm-kernel-lab/workspaces/aiter/aiter/ops/fused_qk_norm_rope_cache_quant.py:83)

## What The Math Is Doing

At a very high level:
- normalize `Q`
- normalize `K`
- do it in one fused route when the shape is below a threshold
- otherwise fall back to separate RMSNorm calls

This is exactly the kind of code where a quant-minded reviewer can ask:
- why this threshold?
- what is the cost model?
- when does fusion help versus hurt?

## Review Questions

1. Is `_FUSED_QK_FALLBACK_M = 16384` likely conservative, aggressive, or unknown?
2. What math or memory reason might make the fused path worse above that threshold?
3. Is this threshold a likely candidate for future runtime-affecting experiments?
4. If the threshold moved, what trace evidence would we need before claiming improvement?

## Why This Packet Matters

This is the first code packet that gets your quants looking at:
- real math path branching
- a concrete threshold
- a fused op with a fallback boundary

That is much closer to optimization thinking than pure route diagnostics.
