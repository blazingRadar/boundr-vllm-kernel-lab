# Second Target Staging

## Why This Exists

The first target is observability-focused and does not itself produce a performance delta.

That is acceptable, but it means the optimization protocol will not be exercised by the first PR alone.

## Requirement

Stage a second target behind the first that is:
- small
- reviewable
- and capable of changing runtime behavior

## Good Candidate Classes

1. route fix
2. fallback-threshold adjustment
3. shape coverage correction
4. tuned-config coverage diff tool that directly affects route decisions downstream

## Goal

The first observability PR should improve diagnosis.

The second target should be the first one that can produce:
- a baseline packet
- a candidate packet
- a route change or measurable perf change

That is the target that road-tests the protocol for real.
