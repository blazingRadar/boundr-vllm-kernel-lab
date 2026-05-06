# First PR Implementation Memo

## Purpose

This memo turns the first-PR test strategy into an implementation-sized plan.

The aim is to make PR 1 small, reviewable, and zero behavior change.

## First PR Type

Scaffolding PR.

Not an optimization PR.
Not a diagnostics API PR.
Not a behavior-change PR.

## Planned Files

Primary touch set:

- `tests/kernels/moe/test_ocp_mx_moe.py`
- `tests/compile/passes/test_fuse_mla_dual_rms_norm.py`

Preferred rule:

- no production file changes in PR 1 unless a tiny test seam is absolutely necessary

## Proposed Test Names

### Quark

#### `test_ocp_mx_moe_supported_scheme_family_smoke`

Goal:

- lock down that supported OCP MX scheme-family cases stay in the intended supported bucket

Assertion shape:

- use a minimal layer or config surface already present in test helpers
- confirm supported scheme family resolves into the intended Quark MoE method class
- do not claim native execution, only correct method-class selection or support classification

#### `test_ocp_mx_moe_unsupported_scheme_family_rejected`

Goal:

- prove unsupported scheme families are not silently accepted as OCP MX native candidates

Assertion shape:

- feed a non-matching scheme/config combination
- assert wrong family does not map to the OCP MX path
- if route is rejected by exception or alternate class selection, assert that directly

#### `test_ocp_mx_moe_missing_fused_moe_support_blocks_native_path`

Goal:

- prove that missing fused-MoE support prevents the native AITER path from being treated as available

Assertion shape:

- patch `rocm_aiter_ops.is_fused_moe_enabled()` to `False`
- patch or control minimal platform support predicate as needed
- assert resulting method or state reflects non-native path selection

#### `test_ocp_mx_moe_route_sensitive_case_does_not_overclaim_native`

Goal:

- ensure a route-sensitive case does not silently claim native support when a required route predicate is absent

Assertion shape:

- choose one known-sensitive predicate:
  - platform MX support
  - fused MoE enabled
  - scheme class
- hold other conditions fixed
- assert that removing that single predicate prevents native-only assumptions

### MLA Fusion

#### `test_fuse_mla_dual_rms_norm_positive_control`

Goal:

- preserve the existing positive fused case

Assertion shape:

- keep the current fused success test
- optionally rename or leave intact
- this is the anchor for later negative tests

#### `test_fuse_mla_dual_rms_norm_disabled_gate_no_match`

Goal:

- prove that when fusion is disabled at the pass-config gate, the pass does not match

Assertion shape:

- set `fuse_mla_dual_rms_norm=False`
- build the same model pattern
- assert `matched_count == 0`
- assert fused op does not appear in post-pass checks

#### `test_fuse_mla_dual_rms_norm_missing_fused_op_no_match`

Goal:

- prove that missing fused-op availability prevents fusion cleanly

Assertion shape:

- monkeypatch `check_aiter_fused_qk_rmsnorm()` to `False`
- keep AITER broad enablement otherwise consistent
- assert `matched_count == 0`
- assert unfused graph remains valid

## Expected PR Size

Expected size:

- about 6 to 7 tests total
- about 150 to 300 lines

If the diff grows past that, cut scope before submitting.

## Preferred Assertion Style

For PR 1, prefer:

- class-selection assertions
- matched-count assertions
- before/after op assertions
- skip-clean behavior

Avoid:

- log-message assertions
- timing assertions
- hardware-route claims
- performance claims

## Suggested Implementation Order

1. Keep the existing MLA positive test intact.
2. Add the two MLA negative tests.
3. Add the Quark support/reject tests.
4. Add the Quark route-sensitive negative test last.
5. Run the test files only.
6. Trim any flaky or over-broad case before expanding scope.

## Local Verification Target

Minimum local verification target:

- targeted pytest pass or skip-clean on the touched tests
- no unrelated test churn

If a test cannot be made CPU-runnable, it must skip cleanly with an explicit prerequisite reason.

## Current Draft State

The draft test patch now exists in the lab workspace on:

- `tests/kernels/moe/test_ocp_mx_moe.py`
- `tests/compile/passes/test_fuse_mla_dual_rms_norm.py`

What is locally verified now:

- syntax compilation passes

What is not yet locally verified:

- full targeted `pytest` execution in the cloned upstream workspace

Current reason:

- shared test infrastructure still pulls in extra optional dependencies through `tests/conftest.py`

## Reviewer Surface

Likely reviewer-adjacent code surfaces from history:

- `tests/kernels/moe/test_ocp_mx_moe.py`
  - notable history from `fxmarty-amd`
- `tests/compile/passes/test_fuse_mla_dual_rms_norm.py`
  - introduced by Rita Brugarolas in the public history

This is not a maintainer map.
It is only a first-pass indication of who has recently touched these exact surfaces.

## What PR 1 Unlocks

After this PR lands, the next two patches become materially easier:

- deprecated AITER API replacement
- structured Quark route/emulation reason reporting

Then, once hardware exists:

- Quark preprocess vs forward timing instrumentation
- fused `M=16384` branch tracing and sweep

## Submission Standard

Submit PR 1 only if it remains:

- small
- test-only
- zero behavior change
- legible to a reviewer in one sitting

If it turns into a refactor, split it.
