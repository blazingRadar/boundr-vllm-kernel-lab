# Abstraction Feedback Notes

## Source Shape

These notes capture a later theory-heavy feedback pass that stayed aligned with the lab's existing discovery geometry.

The key value of the feedback is not that it changes the first PR.
It does not.

Its value is that it sharpens the order of post-hardware runtime experiments.

## What It Confirms

The feedback converges with the lab's existing read:

- the opportunity is not a giant kernel rewrite
- the hidden object is a cost boundary or route boundary
- coarse booleans and scalar thresholds are likely standing in for richer decision surfaces
- the right move is to expose the real boundary before changing behavior

## Two Reinforced Decision Manifolds

### Quark OCP MX

The route is still treated too coarsely:

- native when MX support and the relevant dtype pair line up
- otherwise emulation

The feedback argues that this may be hiding a richer route/cost table involving:

- per-call activation quantization
- shuffle/reformat cost
- low-`M` amortization
- low-reuse regimes

### Fused QK RMSNorm

The scalar threshold:

- `_FUSED_QK_FALLBACK_M = 16384`

is likely acting as a proxy for a higher-dimensional break-even surface involving:

- token-row volume
- head dimension
- dtype
- launch count
- memory cost
- hardware/runtime version

## What Changes In The Plan

The first PR does not change.

It remains:

- tests first

What changes is the preferred order of measured runtime experiments after hardware access exists:

1. fused QK RMSNorm branch tracing around `M=16384`
2. Quark route/preprocess timing around native vs emulation
3. only then a small route or threshold behavior probe

## Why This Order Now Wins

The fused threshold trace is the most compact first measured-learning surface:

- one file
- one scalar cutoff
- bounded sweep region
- clear route evidence

The Quark route trace remains highly valuable, but it has more moving parts:

- route selection
- preprocessing/shuffle cost
- forward cost
- scheme and platform interaction

## What Still Must Not Happen

Do not:

- rewrite kernels from theory
- retune thresholds from theory
- collapse route logic based only on abstraction

The feedback strengthens the lab's existing discipline rather than weakening it.
