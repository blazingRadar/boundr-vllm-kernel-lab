# Optimization Test Protocol

## Purpose

Define exactly how this lab decides whether a change is a real optimization.

## Core Rule

A change only counts as an optimization if:

1. the same workload is run before and after
2. the route evidence is captured both times
3. the performance metric improves
4. the improvement is not explained by a different uncontrolled workload or environment

If route evidence is missing, the run is incomplete.

## Test Shape

Every optimization test is a paired comparison:

- `baseline_run`
- `candidate_run`

Both must share:
- same model
- same hardware
- same ROCm version
- same prompt and generation lengths
- same batch shape
- same decoding settings
- same serving stack except for the intended change

## Repetition Requirement

Each condition must be run multiple times.

Minimum:
- `N >= 3`

Preferred:
- `N >= 5`

Report:
- median
- a spread measure

Preferred spread measure:
- median absolute deviation

Do not claim a meaningful win from a single baseline/candidate pair.

## Required Evidence

### Performance

- `time_to_first_token_ms`
- `prompt_tokens_per_sec`
- `generation_tokens_per_sec`
- `avg_output_token_latency_ms`
- `end_to_end_wall_ms`

### Route

- `expected_backend_route`
- `observed_backend_route`
- `fallback_detected`

### Trace

- `trace_tool`
- `hottest_kernels`
- `kernel_launch_count`
- `suspected_stall_or_emulation_signature`

### Environment

- `gpu`
- `rocm_version`
- `vllm_commit`
- `aiter_commit`
- exact route flags
- `temperature`
- `seed` if used
- `top_p` or equivalent sampling controls if relevant
- GPU exclusivity evidence at run start
- GPU exclusivity evidence at run end

## Admissible Change Types

- route/dispatch change
- tuned-config change
- fusion enablement change
- kernel or backend change

## Invalid Comparison Cases

A result is invalid if any of these are true:

- another workload was active on the same GPU and not recorded
- prompt shape changed
- generation length changed
- model revision changed unintentionally
- route changed unexpectedly and was not captured
- trace was expected but not collected
- decoding settings changed
- run count below minimum

## Interpretation Rules

### Case 1: Faster and better route

Counts as a strong optimization:
- performance improved
- and the route moved from fallback/emulation to native/tuned

### Case 2: Faster but same route

Counts as a plausible optimization:
- performance improved
- route remained the same

This may indicate:
- a tuned-config improvement
- reduced overhead inside the same path
- fusion benefit within the same route family

### Case 3: Same speed, better route

Counts as unresolved:
- route improved
- but benchmark delta is not material

May still matter for larger workloads.

### Case 4: Slower but better route

Counts as a diagnostic result, not a win:
- route improved
- but overhead elsewhere dominates

## Thresholds

Use provisional thresholds:
- `>= 5%` worth attention
- `>= 10%` meaningful
- `>= 20%` high leverage

These thresholds are provisional until the lab measures its own noise floor.

## Noise Floor Requirement

Before claiming a real optimization, run the exact same workload repeatedly with no code or flag changes.

Minimum:
- `N = 10` repeated baseline runs

Output:
- median
- MAD
- observed best/worst range

This establishes whether a claimed delta is above the lab's own benchmark noise.

## First-Pass Practical Rule

For this lab, the first convincing win will usually look like:
- native path reached
- fallback/emulation removed
- and at least one core speed metric improves by `>= 10%`

And:
- the candidate distribution must cleanly exceed the baseline distribution under the chosen summary rule
