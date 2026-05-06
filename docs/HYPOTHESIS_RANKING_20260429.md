# Hypothesis Ranking

## Rank 1

`H1` Wrong backend route into emulation

Why:
- highest likely penalty
- easiest to confirm with traces
- public commit already proves this class is real

## Rank 2

`H2` Dynamic MXFP4 overhead dominates gains

Why:
- public rollback signal is strong
- directly relevant to the April 29 DeepSeek discussion

## Rank 3

`H3` AITER tuned GEMM is the better near-term path on target shapes

Why:
- public code now explicitly enables it
- AITER has substantial tuned GEMM infrastructure

## Rank 4

`H5` Fallback thresholds / shape-coverage gaps

Why:
- likely real
- depends on actual workload shapes

## Rank 5

`H4` MLA fusion is a cleaner frontier than generic kernel work

Why:
- promising but narrower
- likely architecture-specific

## Rank 6

`H6` Tuning asset coverage matters more than code changes

Why:
- plausible
- requires benchmark and trace evidence to elevate further
