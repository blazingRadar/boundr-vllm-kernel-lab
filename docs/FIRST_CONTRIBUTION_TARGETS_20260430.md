# First Contribution Targets

## Principle

The first contribution should be:
- small
- reviewable
- traceable to a real bottleneck class
- plausible for an AMD reviewer to accept

It should not be:
- a speculative giant kernel rewrite

## Best Initial Target Classes

### 1. Tests That Lock Down Route / Gating Behavior

Why:

- highest acceptance probability
- zero behavior change
- useful before ROCm hardware
- builds reviewer trust

Ideal shape:

- negative-gating tests
- route-selection tests
- skip-clean tests for unsupported surfaces

## 2. Mechanical API Cleanup

Why:

- low-risk follow-up after tests
- easy for maintainers to review
- improves code health without claiming perf

Ideal shape:

- deprecated AITER call replacement

## 3. Route / Dispatch Diagnostics

Why:
- highest leverage
- but more design discussion than tests
- best after a trust-building first PR

Ideal shape:
- route evidence capture
- trace metadata capture
- emulation signature checker

## 4. Coverage / Config Audit Tooling

Why:
- useful even before compute
- reduces reviewer uncertainty
- helps AMD know whether a runtime shape is covered

Ideal shape:
- shape-to-config diff tool
- model-family coverage report

## 5. Benchmark / Trace Tooling

Why:

- makes later kernel work auditable
- directly useful to review and regression discipline

Ideal shape:

- route evidence capture
- trace metadata capture
- emulation signature checker

## 6. Small Policy Correction

Why:

- can be performance meaningful
- but should wait for measured evidence

Ideal shape:

- adjust enablement or fallback logic for a known supported family

## Worst First Target

- net-new fused kernel with no benchmark and no hardware evidence
- speculative behavior-change PR justified only by theory

That is the fastest path to wasting reviewer time.
