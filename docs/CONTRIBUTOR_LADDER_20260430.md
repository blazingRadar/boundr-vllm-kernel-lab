# Contributor Ladder

## Goal

Move from:
- interested outsider

to:
- useful public contributor

without pretending to be a production kernel engineer on day one.

## Level 1: Observer

You understand:
- ROCm as the AMD GPU software base
- AITER as the optimized kernel/tuning layer
- vLLM as the serving/runtime layer

You can do:
- read commit diffs
- classify changes as:
  - kernel coverage
  - tuned-config
  - route/dispatch
- explain why a fix matters

## Level 2: Diagnostic Contributor

You can do:
- trace route selection
- identify fallback or emulation
- compare runtime shapes against tuned coverage
- write high-quality issue reports and benchmark packets

This is the first level that is immediately useful to AMD.

## Level 3: Integration Contributor

You can do:
- patch route logic
- patch config coverage
- improve benchmark and trace tooling
- submit small reviewable PRs that change behavior without inventing new math

This is the most realistic near-term upstream contribution level for the lab.

## Level 4: Kernel-Adjacent Contributor

You can do:
- reason about shape coverage
- reason about launch-count reduction
- reason about fusion opportunities
- propose where a new kernel or fused path would pay off

This level still does not require writing a brand-new kernel immediately.

## Level 5: Kernel Contributor

You can do:
- modify or add low-level AITER kernel implementations
- justify changes with trace and benchmark evidence
- validate correctness and performance on real hardware

This is possible, but it is not the right first milestone.

## Recommended Path For This Lab

The lab should aim first for:
- Level 2
- then Level 3

That is enough to create:
- useful AMD-facing artifacts
- real reviewable PRs
- a credible path to deeper kernel work later
