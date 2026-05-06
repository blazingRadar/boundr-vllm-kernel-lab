# AMD Investigation Pitch — Fused QK RMSNorm Fallback Threshold

Date: 2026-04-30
Status: **DRAFT — not yet sent**
Channel: TBD (likely GitHub issue on `ROCm/aiter` or direct DM to a recent AITER reviewer)

## Purpose

Send AMD a calibrated investigation question — not a PR, not an architectural proposal. Ask whether AMD wants us to characterize the fused QK RMSNorm fallback threshold on rented MI300X compute.

The pitch deliberately frames as: "would this be useful?" rather than "we propose to fix this." Different ask, different burden of evidence, much higher response probability.

## When to send

**Only after the lab has merged at least one concrete PR (PR 1 = route-gating tests).** The pitch lands meaningfully differently from a contributor whose name already appears in the merge queue versus from a stranger.

Order:
1. PR 1 (tests) merges
2. Wait one to two weeks (let the maintainer remember the merge)
3. Send this pitch
4. Continue PR 2 (deprecated API) and PR 3 (observability) in parallel regardless of pitch response

## The pitch text (~one page, four short paragraphs)

---

**Subject:** small investigation question — fused QK RMSNorm fallback threshold

Hi [AITER reviewer / team],

While reviewing the public AITER fused QK RMSNorm path for a small AMD-relevant contribution lab, we noticed the `_FUSED_QK_FALLBACK_M = 16384` constant in `aiter/ops/fused_qk_norm_rope_cache_quant.py`. The threshold currently gates fused vs fallback selection on `q.size(0)` alone.

Our hypothesis is that this scalar may stand in for a higher-dimensional break-even surface (head_dim, dtype, batch shape, ROCm version, launch cost). If true, the optimal cutoff could shift across real DeepSeek-V3 / Kimi-K2 production shapes. We don't have evidence either way yet, and we don't want to propose a behavior change without measurement.

We'd like to run a small (~1-hour) characterization experiment on rented MI300X capacity: sweep M around 16384 with N≥5 runs at fixed head_dim / dtype / hardware / route flags, capturing observed backend route, kernel launch count, peak memory, and tokens/sec. The outcome is a small data table (not a PR) — either it confirms 16384 is well-placed for production shapes, or it surfaces an actual decision surface. We'd share the data back regardless of whether the result is interesting.

Before we run it, two questions:
1. Would this characterization be useful to AMD, or is this work AMD has already done internally? If the latter, we'd love to hear the conclusion and stop spending compute on it.
2. Is there a specific shape distribution from production traffic that would make the experiment more valuable than a generic sweep?

No commitment expected — a one-line reply is enough, and we're shipping small PRs (route-gating tests, deprecated API replacement, route observability) on a separate track regardless of this question.

Thanks,
[name]

---

## What this pitch deliberately does NOT do

- Does not propose `route_surface_tensor`, `boundary_field`, or any architectural successor
- Does not claim the current threshold is wrong
- Does not ask AMD for hardware access
- Does not pitch multiple investigations at once
- Does not commit AMD to anything beyond reading the response email
- Does not commit the lab to follow-up beyond sharing the data

The architectural ideas (`boundary_field`, etc.) stay in the lab's research notes. They are post-empirical destinations, not the starting move.

## Why fused QK RMSNorm and not Quark OCP MX

The Quark route surface has more axes to characterize (capability + dtype pair + scheme + reuse + preprocess economics). The fused QK threshold has fewer axes and a single scalar to measure against. Smaller scope → cleaner experiment → more decisive yes/no on whether the lab's intuition is correct.

If this pitch lands well, the Quark version becomes the second pitch. If this one bounces or returns silence, sending the bigger Quark question is unlikely to land any better.

## Calibrated response distribution

| AMD response | Probability | Useful to lab? |
|---|---|---|
| "Yes, run it; here's a useful shape distribution" | ~25-35% | yes — strongest outcome |
| "We've characterized this internally; here's what we found" | ~25-35% | yes — saves $20 of compute, gives privileged signal |
| "Interesting but not priority" | ~20-30% | yes — cheap negative signal, redirect |
| Silence | ~10-20% | benign — try again after more merged PRs |

Three of four outcomes inform the lab's next move. Even silence is benign.

## What to do with each response

**"Run it; here's the production distribution"** → run E0 (git archaeology of the 16384 constant) + E1 (variance floor on N=20 identical runs) FIRST, then the M-sweep characterization at the AMD-suggested shapes on rented MI300X (~$10-20 total). Send results back whether interesting or boring. Don't pitch architecture; send data.

**"Already characterized internally"** → ask for the conclusion, thank them, redirect compute to other contribution work. The lab now has a privileged source on AMD's actual roadmap on this axis.

**"Interesting but not priority"** → don't push. Ship more PRs. Send a different (probably smaller) pitch in 6 months when context has changed.

**Silence** → benign. Don't read into it. Reviewers have queues. Ship more PRs and circle back later.

## What NOT to do regardless of response

- Don't follow up multiple times on silence
- Don't pitch the architectural successor objects (`boundary_field`, `route_surface_tensor`) until measurement justifies them
- Don't conflate "AMD said yes to investigating" with "the investigation found something worth a PR"
- Don't spend more than ~$30 of compute on this axis without a positive signal from AMD

## Required prerequisites before sending

- [ ] PR 1 (route-gating tests) has merged, OR is in active review with positive maintainer feedback
- [ ] Lab has a clear contributor GitHub identity that the AITER reviewer can match to the merge queue
- [ ] The right recipient is identified (look at recent AITER PR reviewers, not random GitHub handles)
- [ ] The lab has access to ~$20-30 of MI300X spot capacity ready to run if AMD says yes
- [ ] E0 git-archaeology has been done — so if AMD asks "what made you suspect 16384 isn't right", we have a real answer

## Notes for future pitches

If this one lands well, the second pitch (Quark route surface characterization) follows the same shape:
- single small experiment, time-boxed
- specific cost
- explicit "would this be useful"
- explicit no-commitment escape
- explicit "we're shipping PRs on a separate track regardless"

The two-track discipline (concrete PRs always shipping; investigation pitches as separate, smaller asks) is the architecture. Don't let the architectural enthusiasm leak into the pitch text.

## Hold these in research notes only — DO NOT pitch

- `route_surface_tensor` (Quark architectural successor)
- `boundary_field` (fused QK architectural successor)
- `utility_policy_with_hysteresis`
- "minimal mathematical IR unifying both"

These are post-empirical destinations the lab can describe in an interview narrative or a long-form research note. They are not pitch material. Keeping them out of the pitch is what makes the pitch land.
