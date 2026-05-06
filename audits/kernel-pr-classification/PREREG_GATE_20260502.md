# Pre-Registration Gate: Kernel PR Gap-Class Classification

Date: 2026-05-02
Status: PRE-REGISTERED, BEFORE CLASSIFICATION
Researchers: orchestrator + 2 independent classifier agents
Repository: `boundr-vllm-kernel-lab/audits/kernel-pr-classification/`

---

## Goal

Test whether the lab's "Launch-Readiness Gap Detector" 3-class taxonomy holds up against a balanced sample of real launch-relevant PRs, and whether the lab's empirical claim ("route + coverage dominate, tuning is secondary") survives a larger sample than the original n=4 commits.

## Target Claim (the lab's existing position)

> "For new model releases on ROCm/vLLM/AITER, the dominant gap classes are `dispatch_route_gap` and `kernel_coverage_gap`. `tuned_config_gap` is secondary."

## Anti-Claim Auditor C raised

> "PR #39987 microbench shows tuned BF16 beating dynamic FP4, suggesting tuning is load-bearing. The 4-commit evidence base is too small and may be selection-biased."

This pre-reg tests both.

## Corpus

`corpus_v1.jsonl` — 79 unique merged PRs across:
- `vllm-project/vllm` (24)
- `ROCm/aiter` (29)
- `ROCm/ATOM` (26)

Sampling rule: top 6 most-recently-updated merged PRs per (repo, model) pair, where model ∈ {deepseek-v3, dsv3, kimi-k2, qwen3-moe, qwen3-next, gpt-oss} and merge date ∈ [2025-05-01, 2026-05-02]. Deduped by URL.

Corpus SHA256: see `corpus_v1.sha256` (committed before classification).

Rate-limit gap: vllm-project/vllm queries for `deepseek-v3` and `dsv3` were rate-limited; remaining 4 model queries against vllm covered the model surface. Documented; not a defect.

## Classification Rubric

For each PR, classifier must emit ONE primary class and may add ONE secondary class if the PR genuinely spans two:

### `kernel_coverage_gap` (KC)
Required kernel/op family did not exist as a native ROCm/AITER kernel; PR adds it OR enables a previously-missing path. Evidence: new kernel file, new fused op, new model architecture support, "support X kernel" framing, "implement Y" framing.

### `tuned_config_gap` (TC)
Right kernel exists, route reaches it, but tuned coverage missing for production shapes. PR adds tuning configs (CSV updates), retunes existing configs, or runs autotuner output. Evidence: CSV-only changes in `model_configs/` or `tuned/`, "retune" framing, "tuning for {model}" framing.

### `dispatch_route_gap` (DR)
Native path exists, tuned asset may exist, but runtime falls into emulation, generic eager, or wrong backend path. PR fixes routing logic, env-var gating, backend selection, fallback conditions. Evidence: changes to dispatch/route code, env-var renames, fallback condition fixes, "use AITER on X" framing, route-correctness fixes.

### `OTHER_<name>` (OTH)
PR doesn't fit any of the three. Classifier must propose a name (e.g., `OTHER_correctness`, `OTHER_distributed_runtime`, `OTHER_ci_only`, `OTHER_docs`, `OTHER_test_only`). Use sparingly; if the PR is a routine bugfix that doesn't change kernel/tuning/route, prefer `OTH:correctness`.

### Multi-class handling

If a PR genuinely spans two classes, set `primary` to the dominant one and `secondary` to the other. If it's truly ambiguous (e.g., the lab's own `6841f5d` was "route/policy plus tuned-GEMM enablement"), use `primary=DR, secondary=TC, multi_class=true, confidence=medium`.

### Confidence

`high` — PR title + body + a sample of diff make the classification obvious
`medium` — required reading the diff carefully; could defensibly land in adjacent class
`low` — required guessing; the PR description didn't make the gap class clear

## Output Format (per classifier)

JSONL, one row per PR, schema:

```json
{
  "url": "https://github.com/...",
  "repo": "...",
  "number": 12345,
  "primary": "DR" | "KC" | "TC" | "OTH:<name>",
  "secondary": "DR" | "KC" | "TC" | "OTH:<name>" | null,
  "multi_class": true | false,
  "confidence": "high" | "medium" | "low",
  "evidence_excerpt": "<one sentence from the PR title/body/diff that drove the call>",
  "is_launch_closure": true | false,
  "classifier_id": "A" | "B"
}
```

`is_launch_closure` = true if the PR closed a launch-readiness gap (a model is now performant or supported because of this PR), false if it's routine maintenance/CI/docs.

## Hypotheses

**H1 (lab's claim):** Among `is_launch_closure=true` PRs, the distribution of `primary` classes has `DR + KC ≥ 0.60` and `TC ≤ 0.30`.

**H2 (Auditor C's counter-claim):** TC ≥ 0.40, OR the OTHER bucket (missing classes) ≥ 0.20 — either of which falsifies the lab's "3-class taxonomy is exhaustive and route/coverage dominates" framing.

**H3 (taxonomy completeness):** OTHER bucket should be < 0.15. If higher, the 3-class framing is non-exhaustive in a meaningful way.

**H4 (inter-rater agreement):** Classifier A and Classifier B should agree on `primary` for ≥ 0.70 of PRs. Below 0.50 means the rubric is too vague to be operationally useful.

## Pre-registered Falsification Thresholds

The lab's claim is **falsified** if any of:
- F1: TC ≥ 0.40 in launch-closure PRs (route/coverage doesn't dominate)
- F2: OTHER bucket ≥ 0.20 (taxonomy isn't exhaustive)
- F3: Inter-rater agreement < 0.50 (rubric isn't operational)
- F4: Confidence distribution skews >50% to `low` (rubric requires guesswork)

The lab's claim is **partially supported** if:
- DR + KC ≥ 0.50 AND TC ≤ 0.40 AND OTHER < 0.20 AND inter-rater ≥ 0.60

The lab's claim is **fully supported** if:
- DR + KC ≥ 0.60 AND TC ≤ 0.30 AND OTHER < 0.15 AND inter-rater ≥ 0.70

## Analysis Plan

1. Per-class distribution overall and within `is_launch_closure=true`
2. Inter-rater agreement (Cohen's κ on primary class, plus simple agreement rate)
3. Per-repo breakdown (does aiter skew TC vs vllm skewing DR?)
4. Per-model breakdown (does each model release have a dominant gap?)
5. Confidence distribution per class (does any class have systematically lower confidence?)
6. List of PRs with disagreement between classifiers — these are rubric-stress cases worth reading
7. The OTHER bucket: enumerate all proposed `OTHER_<name>` values; if a class shows up multiple times (e.g., `OTHER_correctness` × 5), that's a missing taxonomy class.

## Counterfactual Question

If the detector had been running pre-launch on each model: would it have correctly identified the dominant gap class? Operationalized as: for each model in the corpus, compute the modal primary class. The detector "would have helped" for a model if the modal class is consistent and `confidence ≥ medium`.

## Out-of-Scope

- Time-to-close per gap class (would need issue-creation timestamps; corpus only has PR merge times)
- Hardware-trace-based gap classification (requires AMD hardware)
- Causal claims about why certain classes are over/under-represented

## Replication Protocol

Two classifier agents (A, B) classify the same 79 PRs independently using this rubric. No coordination during classification. Outputs land at `runs/A_<timestamp>.jsonl` and `runs/B_<timestamp>.jsonl`. Orchestrator runs the analysis after both finish.

## Sign-off

Pre-reg locked at corpus_v1.sha256 = (see corpus_v1.sha256). Classification begins after this gate is committed.
