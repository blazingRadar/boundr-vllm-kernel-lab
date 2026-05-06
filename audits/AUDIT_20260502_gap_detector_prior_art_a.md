# AUDIT 2026-05-02 — Launch-Readiness Gap Detector, Prior-Art (Auditor A)

## Scope

Independent prior-art search for the lab's proposed three-class taxonomy
(`kernel_coverage_gap`, `tuned_config_gap`, `dispatch_route_gap`) for ROCm/vLLM
launch-readiness lag. Auditor A angle: published literature, vendor blogs,
OSS project docs, and adjacent diagnostic frameworks. No coordination with
Auditor B.

## VERDICT on novelty: 4 / 10

The three categories themselves are folk wisdom that is well-known across the
inference-engine community and visible in ad-hoc form across vLLM, SGLang,
TensorRT-LLM, and TVM/Glow lineage. What is genuinely uncommon — and where the
lab's framing has some originality — is (a) packaging them as a *named, mutually
exclusive classifier* with `dominant_gap_class` output, and (b) operationalising
the classifier as an *external diagnostic packet* a third party can produce
without internal vendor access. I did not find a published artifact that does
both. So: not novel as a decomposition; modestly novel as a productised
diagnostic.

## Evidence

### 1. Academic literature

- **Roofline model (Williams et al., Berkeley)** is the canonical structured
  decomposition of "model X is slow on accelerator Y" into compute-bound vs
  memory-bound. The lab's taxonomy is *orthogonal* to roofline (roofline is
  about analytical ceiling; the lab's taxonomy is about *which layer of the
  software stack is the cause*) — so roofline is not the same framework, but
  it is the obvious referent for "structured perf taxonomy" and reviewers
  will ask why the lab does not cite it.
- **"LLM Inference Unveiled: Survey and Roofline Model Insights" (arxiv
  2402.16363)** systematises optimisation-method evaluation against roofline.
  Still bottleneck-physics, not stack-layer. No three-class equivalent.
- **"The New LLM Bottleneck" (arxiv 2507.15465)** argues MLA + MoE shift
  bottlenecks to interconnect / expert-balance. Adjacent but not a taxonomy
  of *gap origin in the deployment stack*.
- **Tensor-compiler literature (Ansor OSDI'20, Welder OSDI'23, Rammer
  OSDI'20, TVM, Glow, MLIR)** carries the implicit distinction between
  *operator coverage* (Glow's "lowering" is explicitly designed around
  missing-op coverage) and *schedule/tuning* (Ansor's auto-scheduler) and
  *dispatch* (Rammer's inter-op scheduling). All three of the lab's classes
  exist in this lineage individually; none is named the way the lab names
  them, and no single paper packages all three as a per-model classifier.
- **"The Hardware Lottery" (Hooker, CACM)** is the closest *conceptual*
  prior art for "ML gains are gated by software-stack maturity." It is a
  framing essay, not an operational taxonomy.

I found no MLSys / OSDI / ASPLOS paper that proposes the lab's exact 3-class
decomposition under any name.

### 2. Public engineering blogs

- **vLLM Blog 2026-02-27, "Beyond Porting: How vLLM Orchestrates
  High-Performance Inference on AMD ROCm"** — describes a 7-attention-backend
  *dispatcher* on ROCm with explicit fallback semantics and shape-keyed
  selection. This is the closest public artifact to the lab's
  `dispatch_route_gap` concept, but it is engineering description of a
  *solution*, not a *diagnostic taxonomy*.
- **vLLM Blog 2026-03-04, "vLLM Triton Attention Backend Deep Dive"** — same
  shape: dispatcher description, no gap-classification framing.
- **AMD ROCm blog "vLLM 0.9.x and ROCm" / "ROCm Becomes a First-Class
  Platform"** — performance posts, no taxonomy.
- **NVIDIA "Automating Inference Optimizations with TensorRT LLM
  AutoDeploy"** — describes day-0 onboarding effort but does not classify
  per-model lag into kernel vs config vs dispatch.

### 3. Open-source project docs and issue trackers

- **vLLM #30644 (FLASHMLA_SPARSE fallback)**, **#33163 (refactor AITER env
  vars to config)**, **#26768 (DeepSeek-V3 ROCm uplift plan)** — these
  issues *implicitly* span all three of the lab's gap classes, but vLLM's
  issue templates do not formalise the distinction.
- **SGLang #17398 (ROCm missing CLI / kernel build / backend dependency)** —
  again three different gap types in one ticket; no labels separating them.
- **ROCm/aiter issues** — labels visible publicly are `bug`, `enhancement`,
  `triton`, `frameworks-devops`. No `coverage_gap` / `tuning_gap` /
  `dispatch_gap` labels.
- **Optimum-AMD docs** — "validated on MI210/MI250/MI300, others not
  validated" is a *coverage matrix*, but at the GPU-arch axis, not the
  per-model gap axis.

### 4. NVIDIA-specific

NVIDIA's TensorRT-LLM "Day 0" rhetoric and AutoDeploy describe the *outcome*
(model is supported on launch day) and the *automation* (PyTorch graph →
optimised runtime), but I found no public NVIDIA-authored taxonomy that
classifies per-model launch gaps into a structured set of root-cause
categories. Their internal NIM onboarding is not publicly documented at that
level of granularity.

## Distinct gaps (where the lab's framing is genuinely original)

1. **Mutual-exclusivity output (`dominant_gap_class`).** Existing artifacts
   discuss kernel coverage, tuning, and dispatch as concerns; none I found
   forces a "pick one" classifier output per model release. That is the
   lab's actual product surface.
2. **External-diagnostic posture.** The lab proposes producing the
   classification *without* AMD-internal access, using public AITER kernel
   inventory + tuned-config CSVs + vLLM dispatch logic + traces when
   available. I found no public framework that takes this third-party-audit
   posture for ROCm or any other accelerator.
3. **Per-model-release granularity.** Roofline operates per-kernel/per-shape;
   tensor-compiler papers operate per-graph; vendor blogs operate per-stack-
   release. The lab's per-model-release axis (DeepSeek-V3, Kimi-K2,
   Qwen3-MoE) is uncommon in the published framing.

## Honest read

The lab is *partly* reinventing folk wisdom. Anyone who has shipped a model
on vLLM/SGLang/TRT-LLM has lived all three failure modes; calling them
`coverage` / `tuning` / `dispatch` is roughly the natural carving. The lab
overstates novelty when it claims this is "strictly better framing than
treating all lag as a tuning problem" — a strawman, since no serious
practitioner believes all lag is tuning, and the vLLM ROCm attention-backend
post explicitly treats dispatch as first-class.

That said, the *published-framework* gap is real. The community talks about
these three gap types informally in issues and blog posts but has not
produced (a) a named taxonomy, (b) a per-model classifier, or (c) a
third-party diagnostic packet. If the lab's V1 deliverable actually
classifies DeepSeek-V3 / Kimi-K2 / Qwen3-MoE retroactively with citations to
closing commits, that would be a meaningful artifact even though the
underlying categories are not new. The value would be in the *operationalisation*,
not the *concepts*.

Recommendation to the lab: drop the "strictly better framing" claim, cite
roofline and Glow/Ansor/Rammer explicitly as adjacent prior art, and
position the contribution as "the first publicly-reproducible per-model gap
classifier for ROCm/vLLM" rather than as a conceptual breakthrough. Under
that framing, novelty rises from ~4/10 (concepts) to ~7/10 (operational
artifact).

## Sources

- Williams, Waterman, Patterson, "Roofline: An Insightful Visual
  Performance Model" — https://people.eecs.berkeley.edu/~kubitron/cs252/handouts/papers/RooflineVyNoYellow.pdf
- "LLM Inference Unveiled: Survey and Roofline Model Insights" — https://arxiv.org/abs/2402.16363
- "The New LLM Bottleneck: A Systems Perspective on Latent Attention and
  Mixture-of-Experts" — https://arxiv.org/html/2507.15465v1
- Hooker, "The Hardware Lottery" — https://cacm.acm.org/research/the-hardware-lottery/
- Zheng et al., "Ansor: Generating High-Performance Tensor Programs"
  (OSDI'20) — https://www.usenix.org/system/files/osdi20-zheng.pdf
- Ma et al., "Rammer: Enabling Holistic Deep Learning Compiler
  Optimizations with rTasks" (OSDI'20) — https://www.usenix.org/system/files/osdi20-ma.pdf
- Shi et al., "Welder: Scheduling Deep Learning Memory Access via
  Tile-graph" (OSDI'23) — https://www.usenix.org/system/files/osdi23-shi.pdf
- vLLM Blog, "Beyond Porting: How vLLM Orchestrates High-Performance
  Inference on AMD ROCm" (2026-02-27) — https://blog.vllm.ai/2026/02/27/rocm-attention-backend.html
- vLLM Blog, "vLLM Triton Attention Backend Deep Dive" (2026-03-04) — https://blog.vllm.ai/2026/03/04/vllm-triton-backend-deep-dive.html
- vLLM ROCm performance optimization docs — https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference-optimization/vllm-optimization.html
- vLLM issue #26768 "DeepSeek-V3 Performance Uplift Plan on ROCm Backend" — https://github.com/vllm-project/vllm/issues/26768
- vLLM issue #30644 "FLASHMLA_SPARSE fallback to TILELANG" — https://github.com/vllm-project/vllm/issues/30644
- vLLM issue #33163 "Refactor VLLM_ROCM_USE_AITER env vars to config" — https://github.com/vllm-project/vllm/issues/33163
- SGLang issue #17398 "Comprehensive Issues with AMD ROCm Support" — https://github.com/sgl-project/sglang/issues/17398
- ROCm/aiter issues (label inventory) — https://github.com/ROCm/aiter/issues
- Hugging Face Optimum-AMD ROCm support docs — https://huggingface.co/docs/optimum/en/amd/amdgpu/overview
- NVIDIA Technical Blog, "Automating Inference Optimizations with NVIDIA
  TensorRT LLM AutoDeploy" — https://developer.nvidia.com/blog/automating-inference-optimizations-with-nvidia-tensorrt-llm-autodeploy/
- Pete Warden, "Why are ML Compilers so Hard?" — https://petewarden.com/2021/12/24/why-are-ml-compilers-so-hard/
