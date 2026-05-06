# First PR Scope: Tests

## First PR Target

Add negative-gating and route-selection tests.

This is the first PR because it is:

- zero behavior change
- locally verifiable
- high-probability for maintainer acceptance
- directly aligned with the lab's own claim that gating and route coverage are thinner than they should be

## Files

Primary test files:

- `tests/kernels/moe/test_ocp_mx_moe.py`
- `tests/compile/passes/test_fuse_mla_dual_rms_norm.py`

Possible light-touch support file:

- no production code change unless a test seam is absolutely necessary

## Quark Test Slice

Target size:

- 3 to 4 tests

Questions to lock down:

- does the route classification distinguish supported vs unsupported OCP MX scheme families cleanly
- does the gating surface behave correctly when a required feature is unavailable
- does the path skip cleanly when ROCm/AITER prerequisites are missing
- are native-only assumptions confined to the right scheme combinations

Best first cut:

- one test for supported scheme classification
- one test for unsupported scheme classification
- one negative-path test for missing or disabled fused MoE support
- one skip/guard test that proves the route-sensitive case is not silently over-claiming support

## MLA Fusion Test Slice

Target size:

- 2 to 3 tests

Questions to lock down:

- does the pass only activate when the intended high-level conditions are present
- do negative gating conditions prevent fusion cleanly
- does the pass avoid silently claiming success when the prerequisite surface is absent

Best first cut:

- one positive control that keeps the existing fused case
- one negative test for gating disabled
- one negative test for missing or unsupported fused op availability

## PR Size Goal

Keep the first PR small:

- roughly 150 to 300 lines total
- readable in one sitting
- no refactor
- no behavior change

## Acceptance Standard

The first PR is good enough if:

- the added tests express real route or gate claims
- they pass locally or skip cleanly without ROCm
- they make the next PR safer to review

It does not need to improve speed.

## What This Unlocks

Once these tests land, the next two PRs become easier to justify:

- deprecated AITER API replacement
- structured route/emulation reason reporting

Then, after hardware:

- measured Quark route instrumentation
- measured fused-threshold branch tracing around `M=16384`

## What Not To Do In PR 1

Do not:

- change runtime gating behavior
- change threshold values
- add broad new debug APIs
- claim performance improvement
