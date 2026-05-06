# Metrics Contract

Every meaningful benchmark run must capture:

## Throughput

- `prompt_tokens_per_sec`
- `generation_tokens_per_sec`

## Latency

- `time_to_first_token_ms`
- `avg_output_token_latency_ms`
- `end_to_end_wall_ms`

## Resource

- `peak_memory_mb`

## Route Evidence

- `expected_backend_route`
- `observed_backend_route`
- `fallback_detected`

## Trace Evidence

- `trace_tool`
- `hottest_kernels`
- `kernel_launch_count`
- `suspected_stall_or_emulation_signature`

## Environment

- `gpu`
- `rocm_version`
- `vllm_commit`
- `aiter_commit`
- exact route flags

Runs lacking route evidence are incomplete.
Runs lacking trace evidence are weaker but still admissible for a first pass if route evidence is strong.
