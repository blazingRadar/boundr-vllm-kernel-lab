# Emulation Signature Taxonomy

## Purpose

`fallback_detected=true` is only useful if the team agrees on what fallback looks like.

This taxonomy defines the first-pass signatures for:
- native AITER route
- generic fallback route
- likely emulation route

It is intentionally conservative and should be refined after the first real ROCm trace.

## 1. Native AITER Signature

Expected indicators:
- kernel names or op names tied to AITER custom ops
- route evidence showing AITER toggles enabled
- low launch count for fused regions

Examples from public code surface:
- `fused_moe`
- `asm_moe_tkw1`
- `tgemm.mm`
- `fused_qk_rmsnorm`
- `gemm_afp4wfp4`
- `gemm_a16w16`

Likely trace fingerprint:
- one or two dominant kernels per fused region
- absence of explicit quantize/dequantize ladder before every linear op

## 2. Generic Fallback Signature

Expected indicators:
- route falls back to:
  - `torch.nn.functional.linear`
  - generic `aten::*` operators
  - eager-mode quant/dequant behavior

Likely trace fingerprint:
- more launches per logical layer
- more host-visible operator variety
- less evidence of fused kernels

## 3. Quant-Emulation Signature

Expected indicators:
- comments and code paths that describe:
  - simulated weight dequantization
  - activation QDQ
  - high-precision linear after quant handling

Public-code clues:
- `QuarkOCP_MX_MoEMethod` and `QuarkOCP_MX` both contain explicit emulation branches
- warning text refers to:
  - “Simulated weight dequantization”
  - “activation QDQ”
  - “computed in high precision”

Likely trace fingerprint:
- quant/dequant activity surrounding otherwise generic linear ops
- more launches than native fused paths
- weaker fused-MoE or FP4-kernel presence than expected

## 4. MoE Native-vs-Emulation Heuristic

Native expectation:
- dominant fused MoE kernels
- compact launch pattern

Emulation suspicion:
- multiple stage-separated kernels
- explicit high-precision compute after quant handling
- absence of native fused-MoE signatures despite route flags suggesting otherwise

## 5. MLA Fusion Signature

Native fused expectation:
- evidence of `fused_qk_rmsnorm`
- collapse of separate RMSNorm regions

Fallback suspicion:
- two independent RMSNorm regions remain visible
- no trace evidence of the fused op even when pass is enabled

## 6. Operational Rule

Mark `fallback_detected=true` only when at least one of these is true:
- expected native op family is absent
- generic eager/operator ladder is present where fused AITER op was expected
- explicit emulation warning or route evidence confirms fallback

Otherwise:
- mark as `fallback_detected=unknown`
- do not overclaim
