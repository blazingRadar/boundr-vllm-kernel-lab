# Publication Manifest

This repository is a public research artifact for ROCm/vLLM launch-readiness analysis. It studies whether launch-relevant public commits can be classified by failure surface before hardware benchmarking.

## Included

- Research plans and detector drafts for ROCm/vLLM/AITER launch-readiness analysis.
- Commit audits and touched-file ledgers for selected public commits.
- A pre-registered 79-PR classification corpus with two independent classifier outputs.
- Benchmark, trace, and commit-audit templates.
- Lightweight scripts for static coverage analysis and trace-collection scaffolding.

## Claim Boundary

The original three-class detector is preserved as a working hypothesis. The current public claim is narrower: the repo demonstrates an audit method for classifying public launch-relevant PRs, and the later corpus shows the method must include missing classes beyond kernel coverage, tuned config, and dispatch routing.

The repository does not claim production optimization, hardware-validated speedup, access to non-public AMD data, exhaustive taxonomy coverage, or causal proof of why any model launch lagged.

## Repository Hygiene

- Local upstream workspaces and virtual environments are ignored and are not part of the public artifact.
- Public docs should reference upstream source paths as code identifiers, not host-local file links.
- Outreach drafts, relationship strategy, and non-evidence planning notes are excluded from the public artifact.
- Historical docs remain preserved when they are part of the research/audit record, even if later audits narrowed their claims.

## Verification Surface

The public verification surface is Markdown link checking, JSON/JSONL/CSV parsing, Python bytecode compilation, shell syntax checks, high-signal secret scans, and internal-dialogue scans. Hardware trace validation and ROCm benchmark replay require a prepared GPU environment and are not treated as completed evidence here.
