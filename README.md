# Boundr vLLM Kernel Lab

Public research lab on ROCm/vLLM launch-readiness analysis for DeepSeek-class model deployments.

This repo asks a narrow question: when a new model is slow, broken, or missing a fast path on AMD ROCm/vLLM, can the failure be classified from public artifacts into a useful engineering bucket before spending GPU time?

## Current Status

The original lab hypothesis was a three-class detector:

- `kernel_coverage_gap`: a needed kernel or fused op is missing.
- `tuned_config_gap`: the right kernel exists, but tuned coverage is missing for production shapes.
- `dispatch_route_gap`: a native path exists, but runtime routing falls into emulation, generic eager, or the wrong backend.

That framing is useful, but the lab does not present it as a settled causal account. Later audits and a 79-PR pre-registered classification corpus forced the claim to be narrower:

- The taxonomy is a working diagnostic lens, not an exhaustive model of ROCm/vLLM launch lag.
- Public commit evidence can distinguish some route, tuning, and coverage failures.
- The later corpus found a large `OTHER` bucket, so correctness, distributed-runtime, CI/build, and model-support issues also matter.
- Hardware trace evidence is still required before making optimization or performance claims.

## What This Lab Proved

- Public ROCm/vLLM/AITER commits can be audited into repeatable gap classes with evidence excerpts.
- The original four-commit detector was too small to support broad dominance claims.
- A larger pre-registered PR corpus can stress-test the taxonomy and expose missing classes.
- The strongest contribution is the public, reproducible method: classify launch-relevant PRs by failure surface, preserve disagreements, and treat the rubric itself as an object under audit.

## What This Lab Did Not Prove

- It did not prove a new ROCm kernel optimization.
- It did not run a full before/after hardware benchmark.
- It did not validate production performance on MI300X or later hardware.
- It did not prove that route and coverage gaps dominate all launch-readiness failures.
- It did not prove the three-class taxonomy is exhaustive.
- It did not claim access to non-public AMD data.

## How To Read This Repo

Start here:

1. [PUBLICATION_MANIFEST.md](PUBLICATION_MANIFEST.md) - public claim boundary and verification surface.
2. [docs/AUDIT_READY_STATUS_20260430.md](docs/AUDIT_READY_STATUS_20260430.md) - what was and was not empirically closed before the audit handoff.
3. [audits/kernel-pr-classification/PREREG_GATE_20260502.md](audits/kernel-pr-classification/PREREG_GATE_20260502.md) - pre-registration for the 79-PR taxonomy stress test.
4. [audits/kernel-pr-classification/runs/A_20260502T161003Z.jsonl](audits/kernel-pr-classification/runs/A_20260502T161003Z.jsonl) and [audits/kernel-pr-classification/runs/B_20260502T161052Z.jsonl](audits/kernel-pr-classification/runs/B_20260502T161052Z.jsonl) - independent classifier outputs.
5. [audits/AUDIT_20260502_gap_detector_methodology_c.md](audits/AUDIT_20260502_gap_detector_methodology_c.md) - methodology audit that downgrades the original claim.
6. [audits/AUDIT_20260502_gap_detector_prior_art_a.md](audits/AUDIT_20260502_gap_detector_prior_art_a.md) - prior-art and novelty audit.
7. [docs/LAUNCH_READINESS_GAP_DETECTOR_V1_20260429.md](docs/LAUNCH_READINESS_GAP_DETECTOR_V1_20260429.md) - original detector proposal, preserved as historical input, not final truth.

## Repository Layout

```text
audits/      independent audits, commit audits, touched-file ledgers, and the PR classification corpus
docs/        research plans, status memos, review packets, and claim-boundary documents
fixtures/    small CSV fixture for untuned-shape analysis
scripts/     lightweight local analysis and trace-collection stubs
templates/   benchmark, manifest, and commit-audit templates
traces/      placeholder for trace artifacts; no large traces are committed
```

## Verification

The public repo is intentionally lightweight. The local verification surface is:

```bash
python3 -m py_compile scripts/analyze_aiter_config_coverage.py
bash -n scripts/collect_rocm_trace_stub.sh
python3 scripts/analyze_aiter_config_coverage.py
```

Full ROCm/vLLM hardware validation is outside this repository's completed evidence. This lab records the method and the audit trail, not a shipped optimization.
