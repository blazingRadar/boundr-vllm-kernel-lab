# AITER Auto-Tuning Loop Design

## Goal

Turn new-model bring-up into a repeatable loop:

1. identify model shapes
2. detect tuned-config coverage gaps
3. run AITER tuning on the missing shapes
4. emit updated CSVs
5. prepare upstream PR material

## Role In The Lab

This is now a submodule, not the headline thesis.

The primary lab thesis is the launch-readiness gap detector. Auto-tuning matters only when the detector classifies the dominant issue as a `tuned_config_gap`.

## Why This Matters

This is the structural move that can outlive any single DeepSeek release.

If AMD and vLLM are moving faster than per-model tuning updates, the seam is not only kernel math. It is maintenance velocity across:
- model releases
- shape discovery
- tuned-config generation
- upstream integration

## Proposed Pipeline

### Stage 1

Input:
- model config or shape inventory

Output:
- normalized shape packet:
  - op family
  - `M/N/K`
  - dtype
  - batch regime

### Stage 2

Input:
- normalized shape packet
- existing tuned-config CSVs

Output:
- coverage delta:
  - shapes already tuned
  - shapes missing
  - shapes only covered by generic path

### Stage 3

Input:
- missing shapes
- target ROCm host

Output:
- new tuned results via:
  - `aiter/gradlib/gradlib/GemmTuner.py`
  - model-specific tune scripts

### Stage 4

Input:
- tuned results

Output:
- candidate merged CSVs
- before/after benchmark note
- PR-ready artifact packet

## First Prototype Boundary

The first prototype does not need to run tuning yet.

It only needs to:
- ingest model-shape inventory
- compare against tuned CSV coverage
- emit the missing-shape set

That is enough to create a differentiated artifact before compute is available.
