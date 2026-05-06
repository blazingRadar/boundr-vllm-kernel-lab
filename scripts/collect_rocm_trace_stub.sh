#!/usr/bin/env bash
set -euo pipefail

# Stub only.
# This script is intentionally conservative and does not assume a working ROCm box.
# It records the command, flags, and expected trace outputs for later real runs.

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <run-id> <command...>" >&2
  exit 2
fi

RUN_ID="$1"
shift

OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/traces/${RUN_ID}"
mkdir -p "${OUT_DIR}"

{
  echo "run_id=${RUN_ID}"
  echo "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "command=$*"
  echo "VLLM_ROCM_USE_AITER=${VLLM_ROCM_USE_AITER:-}"
  echo "VLLM_ROCM_USE_AITER_LINEAR=${VLLM_ROCM_USE_AITER_LINEAR:-}"
  echo "VLLM_ROCM_USE_AITER_MOE=${VLLM_ROCM_USE_AITER_MOE:-}"
  echo "VLLM_ROCM_USE_AITER_MLA=${VLLM_ROCM_USE_AITER_MLA:-}"
  echo "VLLM_ROCM_USE_AITER_TRITON_GEMM=${VLLM_ROCM_USE_AITER_TRITON_GEMM:-}"
  echo "VLLM_ROCM_USE_AITER_FP4_ASM_GEMM=${VLLM_ROCM_USE_AITER_FP4_ASM_GEMM:-}"
} > "${OUT_DIR}/run_context.env"

cat > "${OUT_DIR}/README.txt" <<'EOF'
Expected real execution on ROCm host:
1. replace this stub with a real rocprof/rocprofiler wrapper
2. capture stdout/stderr
3. capture profiler output
4. record hottest kernels and fallback signatures
EOF

printf '%s\n' "$*" > "${OUT_DIR}/planned_command.txt"
echo "stub_written=${OUT_DIR}"
