# Execution Plan

Date:
- 2026-04-29

## Objective

Turn the current public-code audit lane into a compute-ready ROCm/vLLM performance investigation focused on DeepSeek-family bottlenecks.

## Phase 1: Public Surface Hardening

### Step 1

Produce exact touched-file ledgers for:
- `6841f5d...`
- `944e138...`
- `fb5635d...`
- `ec8ab9d...`

Output:
- one per-commit ledger showing:
  - file
  - layer
  - likely performance role
  - likely evidence needed

### Step 2

Map vLLM touched files to AITER substrate files.

Output:
- dependency matrix connecting:
  - `tgemm`
  - dynamic MXFP4 quant
  - fused QK RMS norm
  - a4w4 / a16w16 paths

### Step 3

Create a benchmark manifest format for real ROCm runs.

Output:
- a machine-readable benchmark manifest template

### Step 4

Create a trace collection checklist and wrapper stub.

Output:
- one trace collection script stub
- one trace interpretation checklist

## Phase 2: Compute-Ready Experiment Design

### Step 5

Define the first experiment pack:
- native AITER MoE vs emulation
- tuned GEMM on vs off
- dynamic MXFP4 on vs off
- MLA dual RMS norm fusion on vs off

Output:
- one experiment matrix with expected flags and measured outputs

### Step 6

Define the exact metrics contract.

Output:
- required fields for:
  - TTFT
  - prompt tokens/sec
  - generation tokens/sec
  - latency per output token
  - peak memory
  - observed backend route

### Step 7

Define success/failure criteria for each experiment.

Output:
- thresholds for:
  - meaningful improvement
  - route mismatch
  - likely emulation signature

## Phase 3: Optimization Thesis Building

### Step 8

Build a hypothesis register.

Candidate hypothesis classes:
- wrong route selection
- quant overhead dominates gains
- tuned GEMM shape coverage gap
- fusion helps more than quantization
- hidden fallback path in MoE

### Step 9

Rank hypotheses by expected leverage and implementation cost.

Output:
- ordered optimization target list

### Step 10

Prepare the first AMD-facing recommendation packet.

Output:
- what to measure first
- what to disable first
- what to trace first
- what not to overinvest in yet

## Immediate Execution Boundary

I can execute all of Phase 1 and Phase 2 scaffolding inside this lab without external hardware.

Phase 3 ranking can also begin now.

The only blocked step is real benchmark execution, which depends on compute and access to the target ROCm environment.
