# Boundr vLLM Kernel Lab

This lab is a separate research workspace for public ROCm/vLLM launch-readiness analysis.

Scope:
- inspect public DeepSeek-family ROCm/vLLM optimization commits
- separate wrapper logic from backend dispatch from real kernel-path changes
- classify launch-lag causes into:
  - kernel coverage gaps
  - tuned-config gaps
  - dispatch-route gaps
- build benchmark and trace discipline for public kernel-performance research
- identify realistic contribution surfaces for future optimization work

Non-goals:
- no changes to any existing Boundr lab
- no imports from private proof lanes
- no contamination of accepted kernel-sidecar or CI/CD artifacts

Initial research targets:
- `944e138bcf39e9236bbfd49d98f00fb45e6cea54`
- `6841f5dc77e9200a2fa45a4bf935b23bd843bf30`
- `fb5635d3f90635ce9d1acbc975baab6e911a262b`
- `ec8ab9d254d3b2e6b919a55277da599a7b9ab146`

Primary question:
- for a new model launch on AMD ROCm/vLLM, which gap class is dominant:
  - kernel coverage
  - tuned-config coverage
  - route/dispatch correctness

Planned workflow:
1. pin and summarize candidate commits
2. inspect touched files and dependency paths
3. classify changes by launch-readiness gap class
4. design a benchmark and trace packet
5. build retroactive launch-lag case studies
6. identify optimization hypotheses worth real compute

See:
- [docs/BOUNDARY_AND_NON_INTERFERENCE.md](docs/BOUNDARY_AND_NON_INTERFERENCE.md)
- [docs/VLLM_ROCM_KERNEL_RESEARCH_PLAN_20260429.md](docs/VLLM_ROCM_KERNEL_RESEARCH_PLAN_20260429.md)
- [docs/COMMIT_TARGETS_AND_HYPOTHESES_20260429.md](docs/COMMIT_TARGETS_AND_HYPOTHESES_20260429.md)
- [docs/LAUNCH_READINESS_GAP_DETECTOR_V1_20260429.md](docs/LAUNCH_READINESS_GAP_DETECTOR_V1_20260429.md)
