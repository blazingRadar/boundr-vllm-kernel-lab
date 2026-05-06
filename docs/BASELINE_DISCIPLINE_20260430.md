# Baseline Discipline

## Why This Exists

Most fake optimization claims come from bad baselines, not good improvements.

## Baseline Requirements

The baseline run must record:
- model id
- model revision if applicable
- hardware id
- ROCm version
- vLLM commit
- AITER commit
- route flags
- prompt token count
- generation token count
- batch size
- temperature
- seed if used
- top_p if used
- GPU exclusivity snapshot at start
- GPU exclusivity snapshot at end

## Baseline Stability Rule

Do not compare against:
- memory of a past run
- a screenshot without route evidence
- a run from a different stack version

Compare only against:
- a captured baseline packet

## Determinism Rule

For benchmarking:
- set `temperature=0`

or:
- use a pinned seed with explicitly recorded stochastic settings

The goal is to keep token generation comparable across runs.

## Noise Floor Rule

Before the first optimization claim:
- run the same baseline workload repeatedly
- characterize variance

Do not treat `5%` or `10%` thresholds as meaningful until the lab has seen its own variance profile.

## First Baseline For This Lab

The first admissible baseline should be:
- one real DeepSeek-family run
- on one ROCm host
- with route evidence
- with trace if available

That baseline becomes the anchor for all later changes on that exact stack.
