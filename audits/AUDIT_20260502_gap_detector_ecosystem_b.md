# AUDIT 2026-05-02 — Launch-Readiness Gap Detector — Ecosystem-Seam Perspective (Auditor B)

## Charter

Test whether the detector's contribution is already covered by public AMD/vLLM process, or whether there is a real ecosystem-seam gap. Distinguish three explanations:

1. AMD or vLLM already does this under different names.
2. AMD considered it and the binding constraint is something else.
3. The org structure makes it nobody's job, so it really is an external opening.

Independent of Auditor A. Ecosystem-seam angle only.

---

## Verdict

**Genuinely-novel-and-undone score: 6.5 / 10.**

Not a 9 — public AMD/vLLM artifacts (DeepSeek-V3 perf plan #26768, ATOM RFC #229) already bin remaining gaps in language that maps cleanly onto kernel-coverage vs. tuned-config. So the **conceptual taxonomy is not novel.**

But not a 3 either — I did not find a public AMD or vLLM artifact that uses the three classes as a **disciplined classifier applied retroactively across launches**, no AITER labels or PR templates encode the taxonomy, and the dispatch-route class is less explicit in the public framing than kernel coverage or tuning. The detector's actual contribution is the **forced separation of the dispatch-route class from the tuning class**, plus retroactive scoring across launches as a discipline artifact.

---

## Evidence Per Explanation

### Explanation 1 — "The ecosystem already does this under another name."

**Partially supported.** Public AMD/vLLM artifacts show related categories, just not as a clean taxonomy:

- **DeepSeek-V3 ROCm Performance Uplift Plan** (vllm-project/vllm#26768) implicitly bins work into algorithmic, distributed, operator-coverage, and overhead gaps. Operator coverage and tuning recipes are listed adjacently but not as separate classes.
- **ATOM RFC #229** (CK-free AITER) explicitly states the remaining gap is "(1) no ASM GEMM for decode (M=1), (2) tuned GEMM CSV coverage only M≤256." This is **two of the three classes named cleanly**. Dispatch routing is conspicuously absent from this framing despite being a known issue elsewhere.
- **AITER tracking issue #14964** organizes work by AITER commit hash plus enhancement / bugfix sub-buckets — temporal, not gap-class.
- **AITER repo labels** are `enhancement`, `bug`, `triton`, `frameworks-devops`. No `kernel-coverage`, `tuning`, `dispatch` labels. No PR template enforces the distinction.
- **vLLM RFC #21805** (Unified Auto-Selection Mechanism for Attention Backends) and **issue #33163** (refactor 13 `VLLM_ROCM_USE_AITER` env vars into config) are direct evidence that dispatch routing is recognized as a distinct, painful surface — but the framing is "too many flags," not "dispatch is a gap class with its own detection signature."

So: public artifacts name kernel coverage and tuning more directly than dispatch routing. The dispatch-route class is the one that appears least consistently named in the public discourse, even though it is exactly the class that produced the lab's strongest commit (944e138 — W4A4 MoE silently emulating instead of using AITER on supported hardware).

### Explanation 2 — "Considered, but the binding constraint is something else."

**Supported as an inference from public artifacts.** Visible constraints in 2025–2026 include:

- **CI infrastructure.** Vllm AMD CI went from 37% passing in November 2025 to 93% in March 2026. Correctness CI was the gating constraint, not classification.
- **Hardware availability for tuning runs.** GEMM CSV coverage capped at M≤256 (per RFC #229) is a tuning-throughput problem, not a "we don't know which shapes to tune" problem.
- **Upstream PR-review velocity in vLLM.** vLLM is a third-party project; AMD work merges at vLLM's pace. A classifier doesn't change merge velocity.
- **SemiAnalysis-class reputation pressure.** AMD has been responding to public benchmark embarrassment (45% peak FLOPs sustained vs. NVIDIA's 93%) with broad-spectrum work, not surgical classification.

If a performance maintainer is triaging "DeepSeek-V3 is 2x slow on MI300X," public artifacts suggest engineer-hours and tuning-hardware-hours may be more binding than classification alone. The detector improves bucket identification; it does not relax those constraints.

**However**, the detector does have value precisely *because* hours are scarce — misclassifying a route bug as a tuning bug burns weeks. The 944e138 case shows this happening: a one-line schema fix (`("w_mxfp4",)` → `("w_mxfp4", "w_mxfp4_a_mxfp4")`) was the right answer, but the symptom looks identical to "MoE just needs more tuning."

### Explanation 3 — "Nobody's job because of org structure."

**Strongest of the three as a public-artifact inference.** This is the most credible visible reason the gap exists:

- **AMD perf team** owns AITER kernels and tuned-config CSVs. Their natural framing is "what do we ship in AITER next."
- **vLLM project** (third-party, mostly UC Berkeley + community + NVIDIA + AMD contributors) owns the dispatch logic in `rocm_aiter_fused_moe.py`, `quark_moe.py`, etc. Dispatch correctness lives in *their* tree, not AMD's.
- The **schema** (`_AITER_NATIVE_OCP_MX_SCHEMES`) that incorrectly excluded `w_mxfp4_a_mxfp4` is a vLLM file. AMD shipped the kernel correctly; vLLM's dispatch table didn't list it. Whose bug is that? Both. So neither team treats it as their primary defect surface.
- AITER's PR template categorizes "enhancement / bug / triton / frameworks-devops" — none of those slots invite a contributor to write "dispatch route in vLLM doesn't reach this kernel." That defect class lives across the seam.

The visible contrast is that TensorRT-LLM presents kernels and dispatcher through one integrated project surface, while AMD/vLLM launch work appears as parallel kernel-merge and vLLM-PR streams that have to converge. The cross-repo seam is the structural hypothesis.

---

## Most Likely Actual Explanation

**Combination of #2 and #3, weighted toward #3.**

Public artifacts already contain parts of the taxonomy (#1-partial). The visible binding constraints include hours, CI, and hardware access, not just naming (#2). But the *dispatch_route_gap class specifically* appears under-named **because it lives at the AMD-vLLM seam where neither public defect-tracking schema names it directly.** That is the visible opening.

The detector's value is therefore narrower than the V1 doc claims: it is most useful **as a seam instrument**, not as a full launch-readiness PM tool. Framed as the latter, maintainers may reasonably say the categories already exist. Framed as the former, it identifies a public cross-repo diagnostic gap.

---

## Public Framing Risk

**Real but manageable.** A retroactive-classification headline like "for 4 of 5 recent launches the dominant gap was dispatch-route, meaning the hardware was capable on day 0 but software shipped the wrong path" would be counterproductive if framed as indictment. The lab should frame the detector as a diagnostic instrument that helps maintainers ship faster, not as a scorecard of past misses. Show the 944e138 case as a success story of fast closure once detected.

---

## If Genuinely a Gap — Best Publication Shape

Ranked:

1. **PR-template / RFC proposal to vLLM upstream**, not AMD. Add a "ROCm gap class" required field to ROCm-tagged perf-bug issues with the three values. This survives the org-seam problem because it lives in vLLM's tree where dispatch defects actually get filed. Highest leverage, lowest political cost. **Recommended primary surface.**
2. **Research-style technical blog post** with retroactive classification of 3 launches (DeepSeek-V3, Kimi-K2, Qwen3-MoE) framed as instrument validation. Avoid scorecard framing. Cite 944e138 as the exemplar. Medium leverage, low risk.
3. **Maintainer discussion after more evidence.** Likely outcome without stronger artifacts: "we know, we're working on it." Do not lead with this.
4. **Academic paper.** Too slow; the seam will close (vLLM RFC #21805 already moves this direction) before publication.

The lab should also consider that the dispatch-route class may **be solved structurally** within 6–12 months if vLLM's unified backend auto-selection RFC lands. The window for the detector being maximally novel is now, not 2027.

---

## Evidence Index

- vllm-project/vllm#26768 — DeepSeek-V3 ROCm performance uplift plan (implicit gap categories)
- ROCm/ATOM#229 — CK-free RFC, names two of three gap classes
- vllm-project/vllm#14964 — AITER kernel integration tracker, organized chronologically not by gap class
- vllm-project/vllm#21805 — Unified Auto-Selection Mechanism for Attention Backends (dispatch as named pain)
- vllm-project/vllm#33163 — Refactor 13 AITER env vars (dispatch flag explosion)
- vllm-project/vllm#22245 — `device_gemm does not support this GEMM problem` for Qwen3-235B (kernel-coverage example)
- ROCm/aiter#915 — `fused_moe does not support this GEMM problem` (kernel-coverage example, Aug 2025, no AMD response visible)
- vllm-project/vllm#34641 — `VLLM_ROCM_USE_AITER_FP4BMM=True` crashes on MI300X (dispatch-route example)
- vllm-project/vllm#35925 — Qwen3.5-35B-A3B corrupted with AITER (correctness-via-dispatch)
- ROCm/aiter#2153 — MoE unit tests fail with AITER on (correctness-via-dispatch)
- Repo-local: COMMIT_AUDIT_944e138 — exemplar of dispatch_route_gap, one-line schema fix
- vLLM Blog 2026-02-27 "Beyond Porting" — describes ROCm attention backend as integrated work, frames it as dispatch+kernel together, supports seam reading
- SemiAnalysis MI300X analysis — establishes that AMD's binding constraint is broad-spectrum SW quality, not classification
