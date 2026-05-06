# Boundary And Non-Interference

This lab is intentionally isolated.

Hard rules:
- no code changes outside `/home/blazingradar/boundr-vllm-kernel-lab`
- no edits to:
  - `boundr-adversarial-gaming-lab`
  - `boundr-cicd-governance-lab`
  - `boundr-swebench-lab`
  - any other existing Boundr lab
- no shared mutable scripts across labs
- no copy-forward of accepted runner code into this lab without explicit user direction
- no claims that private Boundr kernel results transfer directly to ROCm/vLLM GPU kernels

Allowed inputs:
- public GitHub repos
- public commit diffs
- public docs
- local notes written inside this lab

Required discipline:
- keep public-kernel research artifacts local to this repo
- preserve clear separation between:
  - Linux authority/control-plane kernel work
  - GPU compute kernel work
- label hypotheses as hypotheses until benchmark or trace evidence exists

Success condition for this lab:
- a clean public research lane with its own artifacts, benchmark plan, and commit-level analysis
