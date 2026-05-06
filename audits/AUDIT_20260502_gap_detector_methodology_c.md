# AUDIT — Launch-Readiness Gap Detector V1 — Methodology (Auditor C)

Date: 2026-05-02
Auditor: C (independent; no coordination with parallel auditor)
Subject: 3-class taxonomy proposed in `LAUNCH_READINESS_GAP_DETECTOR_V1_20260429.md`
Verdict (overall methodology validity): **5/10**

---

## VERDICT SUMMARY

The taxonomy is a useful first-cut diagnostic vocabulary and is in fact "better than 'tuning fixes everything'" — but it is **not exhaustive, not disjoint, under-evidenced, and partly self-falsifying**. The four anchor commits, when read in full, do not support the lab's "route + coverage are dominant, tuning is secondary" claim — one of them (`6841f5d`) is centrally about whether to *do* tuning at all, and another (`fb5635d`) is a graph-compilation/pattern-matcher pass that does not cleanly belong to any of the three classes. The detector is also incomplete-by-construction without AMD trace access, and the docs do not say so plainly. Most defects are V2-patchable; the sample-size and disjointness defects are foundational.

---

## DEFECT 1 — Non-exhaustive taxonomy (foundational)

The 3 classes silently presume every gap reduces to "right kernel / right tune / right route." The following well-attested AMD/vLLM failure modes do not fit:

1. **graph-compilation gap.** `fb5635d` (PR #39242) is *literally* a `torch._inductor.pattern_matcher.register_replacement` post-grad pass. It is not a kernel coverage gap (the AITER kernel `fused_qk_rmsnorm` already exists in `aiter#2442`), not a tuning gap, and only weakly a route gap — the route into the fused op had to be *invented in the compiler graph*. The lab puts this under "real new fusion/kernel-path capability," collapsing fusion-pass authorship into "kernel coverage." That is a category error.
2. **numerical/correctness gap.** The PR descriptions repeatedly carry GSM8K accuracy gates (`>=0.90`); the W4A4 emulation path was *correct but slow*. A class is needed for "kernel exists, routes, but produces wrong outputs at scale" — public history includes ROCm FA correctness regressions and FP8 KV cache numerical drift cases not listed here.
3. **integration/API-shape gap.** When a model's modeling code uses an op vLLM does not yet wrap (e.g., new attention variants, new MoE router shapes), the failure looks like "kernel missing" but is actually a Python-level adapter gap. The lab folds this into `kernel_coverage_gap`, hiding cheap fixes.
4. **distributed-runtime gap.** TP/EP/PP collectives, RCCL all-to-all for MoE, MI300X-vs-MI355X NUMA effects. Public DeepSeek-V3 launch lag was partly EP-related; none of the 4 anchor commits touch this surface.
5. **memory/bandwidth/HBM gap.** Sharding strategy and KV cache dtype choice are architectural, not "tune the GEMM." The detector cannot recommend "switch to fp8 KV" because the class does not exist.
6. **driver/firmware gap.** ROCm version skew, hipBLASLt version pin, CK version mismatch — common real launch blockers.

**Patchable in V2?** Yes — extend to ~7–8 classes. Failure to do so will cause the detector to misclassify the modal real-world bug.

## DEFECT 2 — Classes are not disjoint (foundational)

The lab's own anchor commit `6841f5d` is admitted to be "route/policy plus tuned-GEMM enablement, partially tuning-adjacent." Reading PR #39987 directly: it (a) adds an env flag `VLLM_ROCM_USE_AITER_TUNED_UNQUANTISED_GEMM`, (b) adds `tgemm.mm` as a fallback in `layers/utils.py`, and (c) deletes `maybe_update_config(...)` so dynamic MXFP4 no longer auto-enables. That is simultaneously a route change, a tuned-asset exposure, and a *reversal of an earlier dispatch policy from `ec8ab9d`*. The "dominant_gap_class" rule is undefined — by attribution of LOC? By performance contribution? By which fix shipped first? No tiebreak rule is given.

Worse, the W4A4 fix (`944e138`) is presented as pure route. Reading PR #41175: the actual change is two lines adding `"w_mxfp4_a_mxfp4"` to `_AITER_NATIVE_OCP_MX_SCHEMES`. This is a *coverage-table* edit. Whether to call it route (the dispatcher consulted the wrong table) or coverage (the table omitted a supported scheme) is a definitional choice the doc never makes.

**Patchable in V2?** Partially — a tiebreak rule (e.g., "class of the smallest sufficient fix" or "class of the line whose revert reproduces the bug") would help, but multi-class bugs are intrinsic and the detector's single-dominant-class output will keep losing information.

## DEFECT 3 — n=4 is not evidence (foundational)

The "route + coverage dominate, tuning is secondary" claim rests on 4 commits selected by the lab itself for other reasons (they were the existing target set). This is textbook selection-on-the-dependent-variable. PR #39987 contains a microbench table where **`aiter tuned bf16` beats `mxfp4 + dynamic quant` at 16/20 shape-rows** — direct evidence that *tuning quality of the BF16 GEMM* is the load-bearing variable, not the route per se. The lab interprets the same data as a route win.

A defensible claim requires a stratified random sample (see Experiment below). Without it the dominance claim should be downgraded from "the public signal suggests" to "consistent with our 4-commit convenience sample."

## DEFECT 4 — Detector is incomplete-by-construction; doc is not honest about it

Inputs 1–4 are public; input 5 (trace evidence) requires AMD hardware. Without traces, the detector cannot distinguish `dispatch_route_gap` (runtime fell into emulation) from `tuned_config_gap` (right route, weak tune) — both produce "slow." The doc lists trace as "when available" and moves on. It should foreground that **without a trace, route-vs-tune is unidentifiable**, and mark such verdicts `unknown` instead of guessing. The `EMULATION_SIGNATURE_TAXONOMY` already has the right `fallback_detected=unknown` discipline; the gap detector spec does not import it.

**Patchable in V2?** Yes — add a `confidence` field and a `requires_trace=true` flag.

## DEFECT 5 — Retroactive classification accuracy

Verified against PR text/diffs:

| Commit | Lab class | Verified | Comment |
|---|---|---|---|
| `944e138` (#41175) | route/policy | **mostly correct** | But it is a 2-line table edit; equally readable as coverage-table fix. Caused by prior PR #39801 regression — i.e. a *route-via-incomplete-table* failure mode the taxonomy doesn't name. |
| `6841f5d` (#39987) | route + tuned-GEMM, tuning-adjacent | **understated** | It is *primarily* a tuning/policy reversal of `ec8ab9d`; the perf table (Geomean 1.058x) is driven by the BF16 tuned GEMM beating dynamic FP4. Calling this "tuning is secondary" inverts the data. |
| `fb5635d` (#39242) | new fusion/kernel-path | **miscategorized** | This is a graph-compilation/pattern-matcher pass; the underlying HIP kernel already exists in AITER. Belongs to the missing "graph-compilation gap" class. |
| `ec8ab9d` (#34157) | quant-path integration/policy | **correct** | True dispatch+integration commit; later partly reverted by `6841f5d`. Lineage matters: the *same surface* swung from "enable" to "disable" in 3 months — neither route nor coverage in the detector's vocabulary captures policy oscillation. |

## DEFECT 6 — Decision-rule edge cases unresolved

The user-supplied dtype example (fp16 kernel exists, fp8 doesn't, model uses fp8, falls back) maps to **both** kernel_coverage (no fp8 kernel) and route (route should refuse fp8 instead of silently degrading). The doc gives no precedence. Other unresolved cases: per-shape coverage holes within an existing tuned CSV (tune or coverage?); MoE expert-count out of tuned range (tune or coverage?); compile-time-vs-runtime dispatch (route or compilation?). Without a precedence table the detector's outputs will be inter-rater unreliable.

## DEFECT 7 — `likely_close_surface` is not actionable for a PM

The output `likely_close_surface ∈ {AITER kernel work, AITER tuned-config work, vLLM route/policy work}` requires the reader to already know which AMD team owns each surface, what staffing each requires, and what the typical fix lead-time is. A program manager cannot allocate engineers from this. To be PM-actionable the output needs: owning-team, estimated effort tier (S/M/L), and dependency on AITER vs vLLM PR cadence.

**Patchable in V2?** Yes — straightforward schema extension.

---

## CAN THE DEFECTS BE PATCHED?

| Defect | Foundational? | V2 patch path |
|---|---|---|
| 1 (non-exhaustive) | Yes | Extend taxonomy to 7–8 classes |
| 2 (non-disjoint) | Yes | Add tiebreak rule + multi-label output; accept information loss |
| 3 (n=4) | Yes | Replace with stratified random sample (see Experiment) |
| 4 (trace dependency) | No | Add `confidence`/`requires_trace` fields |
| 5 (misclassifications) | No | Re-label per evidence above |
| 6 (edge cases) | No | Precedence table |
| 7 (actionability) | No | Schema extension |

---

## ONE CONCRETE EXPERIMENT TO VALIDATE OR FALSIFY THE DOMINANCE CLAIM

**Stratified random-sample audit of vLLM ROCm-relevant commits.**

1. Define population: all merged vLLM PRs from 2025-10-01 to 2026-04-29 with label `rocm`, or touching `vllm/_aiter_ops.py`, `vllm/model_executor/layers/quantization/quark/**`, `vllm/compilation/passes/fusion/rocm_*`, or `vllm/model_executor/layers/fused_moe/rocm_*`. Estimate ~80–150 commits.
2. Stratify by surface: {quant, MoE, attention, fusion-pass, env-flag, other}.
3. Random-sample 40 commits (8 per stratum minimum).
4. Two raters (blind to each other) classify each into the proposed taxonomy plus an `other` bucket. Compute Cohen's kappa for inter-rater reliability — anything below 0.6 falsifies the claim that the taxonomy is even well-defined.
5. Tally class frequencies weighted by PR diff size and by reported perf delta (pulled from PR bodies where available).

**Falsification criterion:** if `tuned_config_gap`-attributed commits produce ≥40% of cumulative weighted perf delta, or if `other` exceeds 20% of the sample, the "route + coverage dominates" claim is rejected and the taxonomy needs the V2 expansion above before AMD-facing use.

The microbench table in PR #39987 alone is enough to suspect the experiment will land in that rejection region.

---

## EVIDENCE APPENDIX

- PR #41175 verified via `gh pr view` — `additions=4, deletions=7`, 2 files, body explicitly attributes the bug to PR #39801 regression. Two-line scheme-table edit.
- PR #39987 verified — `additions=28, deletions=103`, body contains both an end-to-end perf table (Kimi-K2 Geomean 1.058x) and a microbench table where `aiter tuned bf16` beats `mxfp4+dynamic quant` on attention-projection shapes for M ∈ {16,32,64}. Drops `tests/quantization/test_quark_maybe_update_config.py` (-63 lines), confirming policy reversal of `ec8ab9d`.
- PR #39242 verified — `additions=361`, body is explicit: "post-grad pattern-matcher pass," depends on existing AITER PR `ROCm/aiter#2442`. Geomean uplift 1.02x. This is a compiler pass, not a kernel.
- PR #34157 verified — introduces `dynamic_mxfp4_quant` with `maybe_update_config` for `deepseek_v3 + fp4`, the exact code path deleted by #39987.

Source docs read in full: `LAUNCH_READINESS_GAP_DETECTOR_V1_20260429.md`, `WHERE_WE_CAN_HELP_AMD_20260429.md`, `OPTIMIZATION_HYPOTHESIS_REGISTER_20260429.md`, `EMULATION_SIGNATURE_TAXONOMY_20260429.md`, plus the four prior `COMMIT_AUDIT_*_20260429.md` memos in `audits/`.
