# Playbook: First AITER Autotune PR — Droplet Run

Date: 2026-04-30
Target: ROCm/aiter, single CSV-only PR
Hardware: AMD Developer Cloud MI300X droplet (gfx942), $1.99/hr
Estimated wall time end-to-end: 60–90 minutes (most of it tuner runtime)
Estimated GPU spend: under $5

## What this PR is

Add four missing tuned-config rows to `aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv` for DeepSeek-V3 A8W8 BPreShuffle GEMM on gfx942 (MI300X). All four shapes use `torch.float8_e4m3fnuz`, libtype `ck`. The file already covers 1403 gfx942 rows; this PR closes four specific small/mid-M gaps:

| Label | M   | N    | K    | regime         | nearest existing M's |
|-------|-----|------|------|----------------|----------------------|
| A     | 16  | 1280 | 8192 | decode batch   | 1, 32                |
| B     | 16  | 8192 | 1024 | decode batch   | 1, 32                |
| C     | 512 | 4608 | 4096 | mid prefill    | 128, 1024            |
| D     | 512 | 9216 | 4096 | mid prefill    | 128, 1024            |

Justification for these gaps is in `audits/AUDIT_20260430_aiter_autotune_pr_path_resolution.md`.

## Pre-flight (run on droplet, do not skip)

### 1. Confirm hardware

```bash
rocm-smi --showproductname
rocminfo | grep -E 'Name:.*gfx|Marketing'
# expect: gfx942, MI300X
```

If gfx is not gfx942, **stop**. The candidates are gfx942-specific.

### 2. Clone aiter at a known revision

```bash
git clone https://github.com/ROCm/aiter.git
cd aiter
git submodule update --init --recursive
git rev-parse HEAD > /tmp/aiter_head_sha.txt
cat /tmp/aiter_head_sha.txt   # record this in the PR body
git checkout -b dsv3-a8w8-bpreshuffle-coverage-gfx942
```

### 3. Build / install aiter

```bash
pip install -e . --no-build-isolation
python -c "import aiter; print(aiter.__file__)"
python -c "from aiter.dtypes import fp8; import torch; assert fp8 is torch.float8_e4m3fnuz; print('fp8 ok')"
```

### 4. Confirm the tuner script imports cleanly

```bash
python -c "
import importlib.util, sys
spec = importlib.util.spec_from_file_location(
    'gemm_a8w8_bpreshuffle_tune',
    'csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print('tuner importable:', m.GemmA8W8BpreShuffleTuner.__name__)
"
```

### 5. Snapshot the target CSV before changes

```bash
TARGET=aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv
wc -l "$TARGET"           # expect 1535 lines (1 header + 1534 rows)
sha256sum "$TARGET" > /tmp/target_csv_before.sha256
cp "$TARGET" /tmp/target_csv_before.csv
```

## Stage the untuned-input CSV

Create `/tmp/untuned_gaps.csv` with exactly these contents (also staged in the lab at `boundr-vllm-kernel-lab/fixtures/dsv3_a8w8_bpreshuffle_untuned_gaps_20260430.csv`):

```csv
M,N,K,q_dtype_w
16,1280,8192,torch.float8_e4m3fnuz
16,8192,1024,torch.float8_e4m3fnuz
512,4608,4096,torch.float8_e4m3fnuz
512,9216,4096,torch.float8_e4m3fnuz
```

```bash
cat > /tmp/untuned_gaps.csv <<'EOF'
M,N,K,q_dtype_w
16,1280,8192,torch.float8_e4m3fnuz
16,8192,1024,torch.float8_e4m3fnuz
512,4608,4096,torch.float8_e4m3fnuz
512,9216,4096,torch.float8_e4m3fnuz
EOF
```

## Run the tuner

```bash
cd <aiter clone root>

AITER_CONFIG_GEMM_A8W8_BPRESHUFFLE=aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv \
python csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py \
    --untune_file /tmp/untuned_gaps.csv \
    --tune_file aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv \
    --libtype all \
  2>&1 | tee /tmp/tune_run.log
```

Notes:

- The env-var override and the `--tune_file` flag both point at the dsv3 CSV. Either alone works; both is belt-and-suspenders.
- `--libtype all` lets the tuner consider `ck`, `cktile`, and `asm` candidate kernels. The existing rows at these (N,K) use `libtype: ck`, so an `asm` win would be a notable result worth calling out in the PR; otherwise expect `ck`.
- Merge behavior is non-destructive: the tuner reads the existing 1534 rows, concatenates the 4 new ones, dedups by tuning keys keeping the lowest `us`. Existing rows are preserved.
- Expected wall time: roughly 5–15 minutes per (M,N,K) depending on candidate kernel count, so 30–60 min total.

## Post-tune verification

### 1. Confirm exactly 4 new rows landed for gfx942

```bash
TARGET=aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv
diff /tmp/target_csv_before.csv "$TARGET" | head -30

python3 - <<'PY'
import csv, sys
before = set((r['gfx'], r['M'], r['N'], r['K']) for r in csv.DictReader(open('/tmp/target_csv_before.csv')))
after  = list(csv.DictReader(open('aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv')))
new = [r for r in after if (r['gfx'], r['M'], r['N'], r['K']) not in before]
print(f'new rows: {len(new)}')
for r in new:
    print(f"  gfx={r['gfx']} M={r['M']} N={r['N']} K={r['K']} kernelId={r['kernelId']} us={r['us']} libtype={r['libtype']} kernelName={r['kernelName'][:60]}")
print()
print(f'total rows now: {len(after)}  (was {sum(1 for _ in csv.DictReader(open("/tmp/target_csv_before.csv")))})')
PY
```

Pass criteria:

- exactly 4 new rows
- all four have `gfx=gfx942`
- all four have `q_dtype_w=torch.float8_e4m3fnuz`
- all four have a non-negative `kernelId` and non-empty `kernelName`
- `us` values are positive and roughly consistent with neighbors at the same (N,K)
- no existing row was deleted (row count went from 1534 → 1538)

If any pass criterion fails, **do not submit the PR**. Re-run the tuner with `--verbose` if available, or open an issue here in the lab and pause.

### 2. Sanity-check `us` against neighbors

```bash
python3 - <<'PY'
import csv
from collections import defaultdict
rows = list(csv.DictReader(open('aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv')))
gfx942 = [r for r in rows if r['gfx'].strip()=='gfx942']
for N, K, M_new in [(1280,8192,16),(8192,1024,16),(4608,4096,512),(9216,4096,512)]:
    here = sorted([(int(r['M']), float(r['us'])) for r in gfx942 if int(r['N'])==N and int(r['K'])==K])
    print(f'N={N} K={K}:')
    for m, us in here:
        marker = '  ← NEW' if m == M_new else ''
        print(f'  M={m:6d}  us={us:.4f}{marker}')
    print()
PY
```

Expect the new M's `us` to fall between its neighbors' `us` values (or follow a smooth trend). Wildly out-of-line values suggest the tuner picked a degenerate kernel; investigate before submitting.

## Submitting the PR

### Diff scope

The diff should be a single file with exactly 4 inserted lines:

```bash
git diff --stat
# expect: 1 file changed, 4 insertions(+)
git add aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv
git commit -m "Add gfx942 tuned configs for DeepSeek-V3 A8W8 BPreShuffle decode/mid-prefill gaps"
git push origin dsv3-a8w8-bpreshuffle-coverage-gfx942
```

### PR title

```
Add gfx942 tuned configs for DeepSeek-V3 A8W8 BPreShuffle decode/mid-prefill gaps
```

### PR body template

```markdown
## What

Adds four tuned-config rows to `aiter/configs/model_configs/dsv3_a8w8_bpreshuffle_tuned_gemm.csv` for `gfx942` (MI300X), filling decode and mid-prefill gaps for DeepSeek-V3:

| M   | N    | K    |
|-----|------|------|
| 16  | 1280 | 8192 |
| 16  | 8192 | 1024 |
| 512 | 4608 | 4096 |
| 512 | 9216 | 4096 |

dtype: `torch.float8_e4m3fnuz`, libtype: as selected by tuner.

## Why

The file currently has 1403 gfx942 rows covering DeepSeek-V3 A8W8 BPreShuffle shapes. The four (M, N, K) combinations above are not present, despite both their adjacent M values being present at the same (N, K). M=16 is a common decode batch dimension; M=512 is a common mid-prefill dimension.

## How tuned

Ran `csrc/ck_gemm_a8w8_bpreshuffle/gemm_a8w8_bpreshuffle_tune.py --libtype all` on a single MI300X with the four shapes as `--untune_file` input and the dsv3 CSV as `--tune_file` output. The tuner's standard merge behavior (`aiter/utility/base_tuner.py:295-302`) preserves existing rows and adds the new ones. AITER revision: <fill in /tmp/aiter_head_sha.txt>.

## Scope

- CSV-only change.
- Four inserted lines, one file.
- Existing rows untouched.
- No production code changes.
- No new dependencies.

## Verification

- Diff is exactly 4 inserted lines, single file.
- All four rows have `gfx=gfx942`, `q_dtype_w=torch.float8_e4m3fnuz`.
- New `us` values fall in line with neighbors at the same (N, K).
- Tuner log available on request.

## Not claimed

- This PR does not claim a measurable end-to-end improvement on any benchmark; it closes a coverage gap so the tuned-config lookup hits a tuned row rather than falling through to whatever path applies for missing shapes.
- This PR does not modify dispatch/routing logic.
- This PR does not change kernel selection for any shape that already has a row.
```

## After merging (or rejection)

Either way, append a one-paragraph outcome note to `audits/AUDIT_20260430_aiter_autotune_pr_path_resolution.md` under a new `## Outcome` section: PR URL, merge or close decision, reviewer feedback if any, and what (if anything) needs to change about the playbook for the next autotune PR.

## What to do if anything doesn't match this playbook

- If `pip install -e .` fails: the droplet image may not have the right ROCm version. Note the error verbatim and stop — do not try to force-install.
- If the tuner errors with "Not exist untuned file": absolute vs relative path issue; use absolute paths for both `--untune_file` and `--tune_file`.
- If the tuner runs but writes to `/tmp/...csv` instead of the target: the merge step happens in `/tmp` and is then committed back; check `aiter/utility/base_tuner.py` for the post-merge copy-back. The dsv3 CSV is the final destination.
- If any existing row count drops (1534 → less than 1538): **do not submit**. Investigate. The tuner's `drop_duplicates` is keyed on tuning keys; an unexpected row loss means the dedup logic ate something.
- If `us` for a new row is wildly higher than its neighbors: re-run that single shape with `--libtype ck` to force a known-supported library; compare.

## Why this is a defensible first contribution

- Mechanical and verifiable: the diff is four CSV lines; the gap is provably real (audit memo); the tuning method is the existing aiter tuner with no modifications.
- Small enough to be reviewed in one sitting.
- No performance claim, no behavior change for existing shapes, no risk to other models.
- Establishes contributor footing without overclaiming.
