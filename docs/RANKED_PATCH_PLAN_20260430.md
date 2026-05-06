# Ranked Patch Plan

## Purpose

This document turns the latest two-agent exploration results into one ranked patch sequence.

The goal is to:

- pick the best first PR target
- keep the first contribution reviewable
- avoid pretending we are ready for kernel rewrites
- stage a second target that can later exercise the optimization protocol

This plan is now informed by:

- the two-agent code exploration memo
- the external audit recommending tests as the best first PR
- the abstraction-focused feedback that the Quark route split and fused `M=16384` cutoff are both hidden decision manifolds that should be measured before behavior changes

## Ranking Criteria

Patch candidates are ranked by:

- alignment with dominant gap class
- reviewability
- risk of behavioral regression
- usefulness before ROCm compute access
- value for later route/trace/perf work

## Rank 1

### Target

Add route-selection and negative-gating tests for Quark OCP MX and MLA fusion paths.

### Why It Ranks First

This is the best first PR target because it:

- has zero behavior change
- is CPU-runnable and locally verifiable
- has the highest acceptance probability for a new contributor
- directly addresses the lab's own claim that route/gating coverage is weaker than it should be
- will naturally expose which later route and gating fixes are actually justified

### Scope

Likely code surfaces:

- `tests/kernels/moe/test_ocp_mx_moe.py`
- `tests/compile/passes/test_fuse_mla_dual_rms_norm.py`

### Proposed Patch Shape

Add a small first-cut test packet:

- 3-4 Quark route/gating tests
- 2-3 MLA fusion gating or negative-path tests
- total PR size kept in the reviewable range
- no runtime behavior changes

The best first cut is not a giant matrix of cases.
It is a narrow set of tests that lock down the current gating surfaces cleanly enough to support later diagnostic or route fixes.

### Why This Beats Other First Targets

Because it builds reviewer trust first, lands without ROCm hardware, and gives later diagnostic or route PRs a stronger footing.

## Rank 2

### Target

Replace deprecated AITER API usage on the Quark FP4 path.

### Why It Ranks Second

This is concrete and likely low-risk, but it is slightly less foundational than route reasoning.

If the first PR lands, this is a strong second PR because it:

- reduces technical debt
- aligns vLLM with current AITER surface
- gives a reviewer a simple correctness-oriented diff

## Rank 3

### Target

Structured route/emulation reason reporting for ROCm Quark OCP MX paths.

### Why It Ranks Third

This is still a strong target, but it should not lead.

Reasons:

- it introduces or extends an API/logging surface
- it raises design-shape questions that tests do not
- it is easier to defend after the test foundation lands
- it benefits from later real ROCm traces

## Rank 4

### Target

Add debug-only fallback diagnostics around the fused QK RMSNorm fallback threshold.

### Why It Ranks Fourth

Useful, but still a debug-surface change rather than a first-contributor trust builder.

It should follow tests and likely follow the first Quark observability pass too.

## Rank 5

### Target

Tighten MLA dual RMS norm fusion gating to specific subfeature checks.

### Why It Ranks Fifth

This is a real behavior change and should wait for hardware evidence.

It may be correct, but without ROCm traces it is still speculative.

## Not Yet Ranked As Patch Candidates

These are not good early patch candidates before hardware:

- changing dynamic MXFP4 policy
- changing the fused fallback threshold value
- replacing hardcoded tuned lists with a new route policy
- changing kernel math or fusion geometry
- tightening runtime gates that materially change fused/native behavior

These should wait for:

- first ROCm trace
- first baseline packet
- first route-evidence-backed runtime packet

## Selected First PR Target

### Choice

**Rank 1: route-selection and negative-gating tests**

### Why This Is The Single Best First PR

It is the cleanest combination of:

- high value
- low risk
- high acceptance probability
- strong alignment with the lab's own discovered weakness
- immediate usefulness to AMD-style reviewers without hardware

It also creates better ground truth for any later attempt to answer:

- which route predicates are really load-bearing
- which broad gates deserve tightening later
- which observability surface is justified by real test coverage

## Proposed First PR Acceptance Standard

The first PR should be considered successful if:

- Quark route or gating cases are covered explicitly
- MLA fusion negative-path or gating cases are covered explicitly
- tests are CPU-runnable or skip-clean without ROCm
- no behavioral regression is introduced

The first PR does not need to prove a speedup.
It is a scaffolding PR, not an optimization PR.

## Staged Second PR

The best staged second PR after Rank 1 is:

- **deprecated AITER API replacement**

or

- **structured route/emulation reason reporting**

The likely order is:

- PR 1: tests
- PR 2: deprecated API replacement
- PR 3: Quark observability

That sequence maximizes reviewer trust while still moving toward better route diagnostics.

## How This Connects To Optimization

This ranked plan is not separate from optimization work.
It is how the lab earns the right to make later optimization claims.

Sequence:

- PR 1 builds test foundation
- PR 2 lands a mechanical cleanup
- PR 3 improves route observability
- first ROCm packet then measures real route and threshold geometry
- only after that should the lab attempt a runtime-affecting gate or threshold change

The abstraction-focused review adds one more important rule:

- do not edit the fused `M=16384` threshold or Quark native/emulation split until one measured crossover is real

## Honest Status

The lab now has a concrete first PR target.
It still does not have hardware-backed optimization evidence.

That is the correct state.
