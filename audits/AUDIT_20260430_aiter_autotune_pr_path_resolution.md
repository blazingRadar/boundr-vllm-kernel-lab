# Audit: AITER Autotune PR Path Resolution

Date: 2026-04-30
Topic: Resolution of the prior session's "no tune script for candidates A/B/C/D" blocker
Source of record: live verification against `boundr-vllm-kernel-lab/workspaces/aiter` HEAD
Audit class: false-alarm correction (prior conversation made an overstated claim; this memo retracts it with verification)

## Background

The prior session selected four tuned-config gaps in `aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv` as the candidate payload for a small upstream PR to `ROCm/aiter`, to be filled by autotuning on a leased MI300X (gfx942) instance. Late in that session, a read of `aiter/utility/pretune.py` surfaced this fragment:

```python
# blockscale_bpreshuffle variants: no tune script writes to the bpreshuffle CSV
"module_gemm_a8w8_blockscale_bpreshuffle_tune": None,
"module_gemm_a8w8_blockscale_bpreshuffle_cktile_tune": None,
```

The prior session interpreted this as: "the four candidates cannot be tuned by any existing script; a third repick is required." That conclusion was wrong.

## Claim under audit

> Candidates A/B/C/D are not autotunable with existing AITER infrastructure because the `_SCRIPT_FALLBACK` table in `aiter/utility/pretune.py` lists the relevant module entries as `None`.

## Verification

### Step 1 — confirm which family the candidate file actually belongs to

```bash
ls aiter/configs/model_configs/ | grep dsv3
# → dsv3_a8w8_bpreshuffle_tuned_gemm.csv     (plain bpreshuffle)
# → dsv3_a4w4_blockscale_*                   (different family)
# (no dsv3_*blockscale_bpreshuffle* file)
```

The candidate file is `dsv3_a8w8_bpreshuffle_tuned_gemm.csv` — plain `bpreshuffle`, not `blockscale_bpreshuffle`. The two are distinct families with distinct CSV paths and distinct module names in pretune.

### Step 2 — re-read pretune.py with that distinction in hand

`aiter/utility/pretune.py:59-73`:

```
# gemm_a8w8_blockscale_tune.py covers cktile and standard bpreshuffle
#   variants via --libtype all, but it writes to AITER_CONFIG_GEMM_A8W8_BLOCKSCALE.
#   The blockscale_bpreshuffle family uses a separate CSV that no existing .py
#   script writes to.
"module_gemm_a8w8_blockscale_cktile_tune": "module_gemm_a8w8_blockscale_tune",
# bpreshuffle_cktile: covered by bpreshuffle parent tuner
"module_gemm_a8w8_bpreshuffle_cktile_tune": "module_gemm_a8w8_bpreshuffle_tune",
# blockscale_bpreshuffle variants: no tune script writes to the bpreshuffle CSV
"module_gemm_a8w8_blockscale_bpreshuffle_tune": None,
"module_gemm_a8w8_blockscale_bpreshuffle_cktile_tune": None,
```

The `None` entries are for the `blockscale_bpreshuffle` family. The plain `bpreshuffle` family has a parent tuner (`module_gemm_a8w8_bpreshuffle_tune`), and `_cktile` redirects to the parent. The candidates' family is fully covered.

### Step 3 — confirm the tuner script exists and writes to the right CSV

```bash
find csrc -name '*bpreshuffle*tune*.py'
# → csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py
```

`csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py:188-196`:

```python
class GemmA8W8BpreShuffleTuner(GemmCommonTuner):
    ARG_DEFAULTS = {
        **GemmCommonTuner.ARG_DEFAULTS,
        "tune_file": f"{AITER_CONFIG_GEMM_A8W8_BPRESHUFFLE}",
        "untune_file": "aiter/configs/a8w8_bpreshuffle_untuned_gemm.csv",
        "config_env_name": "AITER_CONFIG_GEMM_A8W8_BPRESHUFFLE",
    }
```

`aiter/jit/core.py:80-83`:

```python
AITER_CONFIG_GEMM_A8W8_BPRESHUFFLE = os.getenv(
    "AITER_CONFIG_GEMM_A8W8_BPRESHUFFLE",
    "aiter/configs/a8w8_bpreshuffle_tuned_gemm.csv",
)
```

The output CSV path is overridable via the `AITER_CONFIG_GEMM_A8W8_BPRESHUFFLE` env-var, and the tuner additionally exposes `--tune_file` / `--untune_file` CLI flags via the `GemmCommonTuner` base class (`aiter/utility/base_tuner.py:107-122`). Both mechanisms can be used to redirect output to `aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv`.

### Step 4 — confirm the dtype the candidates use is on a supported tuner path

Existing rows at candidate A's (N=1280, K=8192) on gfx942:

```
q_dtype_w values: {'torch.float8_e4m3fnuz'}
libtype values:   {'ck'}
M values present: [1, 32, 64, 128, 192, 256, 320, 512, 1024, 2048, 4096, 8192, 16384]
```

`csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py:324-325` shows the FP8 path branches on `eval(q_dtype_w) != dtypes.fp8`, where `aiter.dtypes.fp8 == torch.float8_e4m3fnuz` on AMD ROCm builds (`aiter/ops/triton/utils/types.py:62`). The dtype is supported.

### Step 5 — confirm the merge behavior is non-destructive

`aiter/utility/base_tuner.py:295-302`:

```python
merge_df = (
    merge_df.sort_values("us")
    .drop_duplicates(subset=dedup_keys, keep="first")
    .reset_index(drop=True)
)
new_file_path = f"/tmp/{merge_name}.csv"
merge_df.to_csv(new_file_path, index=False)
```

The tuner reads the existing `tune_file`, concatenates new rows, deduplicates by tuning keys keeping the lowest `us`, and writes back. Pointing `--tune_file` at the existing dsv3 CSV is safe — existing rows are preserved (or replaced only if the new tuning result is faster, which is the desired behavior).

## Verified gaps (re-confirmed in this audit)

```
A: N= 1280 K= 8192 M=   16 on gfx942 → MISSING (neighbors at M=1 then M=32, gap in decode regime)
B: N= 8192 K= 1024 M=   16 on gfx942 → MISSING (neighbors at M=1 then M=32, gap in decode regime)
C: N= 4608 K= 4096 M=  512 on gfx942 → MISSING (neighbors at M=128 then jump, gap in mid regime)
D: N= 9216 K= 4096 M=  512 on gfx942 → MISSING (neighbors at M=128 then jump, gap in mid regime)
```

All four gaps are real. All four use `q_dtype_w=torch.float8_e4m3fnuz`, `libtype=ck`. All four are tunable by `csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py`.

## Resolution

- The prior session's blocker is **withdrawn**. The "no tune script" claim applied to a different family (`blockscale_bpreshuffle`) than the candidate file (`bpreshuffle`).
- No third repick is needed.
- The remaining session work — droplet playbook with exact CLI, untuned CSV stub, PR description template — is unblocked and proceeds against candidates A/B/C/D unchanged.

## Failure pattern worth preserving

The error was a substring confusion: `bpreshuffle` and `blockscale_bpreshuffle` share a suffix and both refer to "B-matrix preshuffle" kernels, but they are distinct AITER families with distinct CSVs, distinct C++ kernel directories (`csrc/ck_gemm_a8w8_bpreshuffle/` vs `csrc/ck_gemm_a8w8_blockscale_bpreshuffle/`), and distinct tuner availability. Any future "is this CSV tunable" check must inspect the **family directory** under `csrc/`, not just match on the family name in pretune's `_SCRIPT_FALLBACK` table.

## Claims still not allowed

- That the four candidate gaps will produce a kernel selection different from whatever fallback is in use today on gfx942 (this requires running the tuner on hardware and inspecting the kernelId output).
- That the gaps are launch-blocking for any production deployment (the lab's gap-class taxonomy still classifies tuned-config gaps as secondary; this PR establishes contributor footing, not a perf claim).
- That the resulting PR will be merged. The CSV-only PR is intentionally small and reviewable, but ROCm/aiter merge cadence and reviewer attention are not under our control.
