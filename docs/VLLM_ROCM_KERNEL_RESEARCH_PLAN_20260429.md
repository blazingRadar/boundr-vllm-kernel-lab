# vLLM ROCm Kernel Research Plan

Date: 2026-04-29

## Goal

Build a public research lane for AMD ROCm/vLLM launch-readiness analysis focused on newer DeepSeek-family model paths and the reasons they land poorly.

## Why This Lab Exists

Recent public upstream changes strongly suggest the current performance frontier is not a single "GPU kernel" problem. It is likely a mixed surface involving:
- quantization-path selection
- AITER routing
- tuned GEMM enablement
- MoE emulation fallback avoidance
- MLA and related fusion paths
- wrapper and dispatch correctness

This lab is for turning those possibilities into a bounded research program and classifying them into the right gap class.

## Updated Thesis

The strongest current thesis is:
- AMD launch lag is likely driven primarily by:
  - kernel coverage
  - fusion availability
  - route correctness
- and only secondarily by:
  - tuned-config coverage

So the right v1 artifact is not an auto-tuning loop as the headline.

The right v1 artifact is a launch-readiness gap detector that labels new-model lag as:
- `kernel_coverage_gap`
- `tuned_config_gap`
- `dispatch_route_gap`

## Initial Commit Set

1. `944e138bcf39e9236bbfd49d98f00fb45e6cea54`
   - PR `#41175`
   - W4A4 MoE using emulation instead of AITER on MXFP4-supported hardware

2. `6841f5dc77e9200a2fa45a4bf935b23bd843bf30`
   - PR `#39987`
   - env flags for dynamic MXFP4 disablement and AITER tuned GEMMs for attention projection layers

3. `fb5635d3f90635ce9d1acbc975baab6e911a262b`
   - PR `#39242`
   - MLA dual RMS norm fusion for DeepSeek/Kimi-K2

4. `ec8ab9d254d3b2e6b919a55277da599a7b9ab146`
   - PR `#34157`
   - dynamic MXFP4 quantization for DeepSeek V2 projection layers

## Core Research Questions

1. Which touched code is real kernel-path logic versus wrapper or dispatch glue?
2. For a new model launch, which gap class dominates:
   - kernel coverage
   - tuned-config coverage
   - route correctness
3. Where does AMD lose ground:
   - backend selection correctness
   - quant format compatibility
   - model-architecture-specific routing
   - memory movement and layout
4. Which optimizations would require:
   - vLLM code changes
   - AITER/ROCm backend work
   - better benchmark and trace evidence only
5. Which improvements are likely high leverage for a small external research team?

## Deliverables

- commit audit packets
- touched-file classification ledger
- launch-readiness gap taxonomy
- retroactive case-study packet
- benchmark template
- trace checklist
- optimization hypothesis register

## First Sprint Boundary

Do only:
- commit targeting
- public-code classification
- benchmark/trace plan
- hypothesis framing
- launch-gap framing

Do not yet:
- claim kernel improvements
- clone or modify any private Boundr lab
- overfit to a single performance anecdote
- center the lane on upstream PR automation
