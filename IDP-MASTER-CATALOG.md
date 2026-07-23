# IDP Master Catalog — All Ideas, Explained, Ranked

Consolidates every project idea across all research threads: the cybersecurity sweep,
the broad-software sweep, the LLM-reasoning/interpretability family (UGR), and two
standalone ideas (satellite remote sensing, edge↔cloud routing).

Team size assumed: **3 people** (original brief). The UGR brief assumes 4 — noted where it matters.
Companion files: `idp-research-shortlist.md`, `idp-topics-explained.md`.
Generated 2026-07-23. **Lock baseline versions at project start** — cited numbers will be beaten within your year.

---

## How to read the ranking

Each idea is scored 1–5 on 8 criteria (higher = better *for a capstone*):

| Criterion | Meaning |
|---|---|
| **Feas** | Feasibility — can 3 undergrads build it in a year? |
| **Pub** | Publishability — clear public benchmark + a baseline number to beat |
| **Novel** | Novelty ceiling — how high the research contribution can go |
| **Impact** | Real-world / societal weight |
| **Demo** | How impressive the live demo is for examiners |
| **Cheap** | Low compute/hardware cost (5 = laptop; 1 = needs A100s / special hardware) |
| **Data** | Public dataset readiness (5 = download today; 1 = must collect it yourself) |
| **Risk⁻** | Low failure risk (5 = can't really fail; 1 = "the training might never converge") |

Tiers reflect **capstone fit** (weights feasibility, publishability, data, low-risk heavily;
novelty/impact/demo as tie-breakers), NOT raw ambition.

---

# Part 1 — Full idea catalog (grouped by domain)

## Domain I — Software Security

**I1. Malicious-package detector (PyPI/npm).** Detect trojaned/typosquatted packages.
Open gap: LLMs hit 0.48 F1 on identifying the *specific* malicious indicator (vs 0.99 on
binary detection); npm detectors drift 87%→39% as attackers drop obfuscation. Beat CHASE
(98.4% recall @ 0.08% FPR) on indicator-ID or drift-robustness. Data: CHASE 3k PyPI,
Mind-the-Gap 4,070, npm 6,420+7,288. Papers: 2601.06838, 2602.16304, 2603.27549.

**I2. Prompt-injection defense for LLM agents.** Stop agents obeying malicious text hidden
in content they read. Attacks still hit 84.3% (ASB). Reference: MELON (training-free,
0.24% ASR). Beat utility-under-attack or generalize to harder attack classes. Data:
AgentDojo, ASB, InjecAgent. Caveat: don't claim "no defense exists" (CaMeL is provable).
Papers: 2502.05174, 2406.13352.

**I3. Statement-level vulnerability detection.** Point to the exact vulnerable line with a
valid reason. Best model = only 23.83% F1 on SecVulEval — huge headroom. Augment LLM with
program analysis (CodeQL+LLM à la QLPro). Data: SecVulEval (25,440 C/C++ fns, 5,867 CVEs).
Papers: 2505.19828, 2506.23644.

**I4. PQC migration tooling.** Current Crypto-Bill-of-Materials tools are "semantic-free"
(don't track where crypto sits in control/data flow). Gaps: hybrid-KEM 11%, tooling 22%.
Regex CBOM generator = proven starter. Papers: 2602.05759, 2606.04739, 2603.01091.

**I5. Deepfake detection (audio focus).** Audio benchmarks (ASVspoof) contain ZERO 2024–25
TTS samples — open data gap. GenD gets SOTA generalization tuning 0.03% of params.
Paper: 2508.06248.

**I6. C2PA content provenance.** Now shipping in Pixel 10 / Sony hardware. Origin-Lens-style
on-device image-provenance verification. More engineering than research. Paper: 2602.02100.

**I7. Privacy+fairness federated learning (RESFL).** Adversarial privacy disentanglement +
fairness-aware aggregation. Paper: 2503.16251.

## Domain II — Developer Tools / Software Engineering

**II1. LLM unit-test generation (ULT).** LLM tests don't compile / miss branches / pass
trivially. Contamination-free benchmark; SOTA only 41% acc, 30% branch cov, 40% mutation.
Beat via coverage-guided iterative prompting. Data: ULT (3,909 Python fns, ACM TOSEM).
Paper: 2508.00408.

**II2. Runtime-verified code-review benchmark.** Every review benchmark scores by BLEU /
LLM-judge — NONE builds code + runs tests. Build the first outcome-verified one (apply
fix → build → test). The missing-benchmark story is the novelty. Papers: 2602.13377, 2603.11078.

**II3. End-to-end coding agent (ProjDevBench).** Build whole small projects from a spec.
Agents hit only 27.38% acceptance (0.8·exec + 0.2·review). Build a better scaffold. Crowded
space. Paper: 2602.01655.

**II4. Program repair for DSLs / low-resource languages (SLMFix).** Fix broken LLM-generated
config code (Ansible/Bash/SQL/YAML) with a small RL-tuned model. >95% validator pass; RL
beats SFT even at 7B. Niche but solid. Paper: 2511.19422.

## Domain III — On-device / Edge ML Systems

**III1. SLM-specific quantization (SLMQuant).** Big-LLM quantization transfers poorly to
small models. Design an SLM-specific method, beat SmoothQuant/OmniQuant/SpinQuant. One GPU.
Clean systems paper. Paper: 2511.13023.

**III2. Edge↔cloud inference router.** Run a small local model for easy queries, escalate
only hard ones to cloud (confidence-based offloading / speculative decoding). Contribution =
the routing algorithm + latency/cost/privacy trade-off curve, NOT model weights. Baseline =
Random routing. Fully simulation → software-only, near-zero data risk. Papers: 2505.16508,
2507.16731 (Collaborative Inference between Edge SLMs and Cloud LLMs).

**III3. Offline first-aid RAG on a phone.** Emergency guidance with no signal. Pocket RAG:
94.5% acc, 3.7s, offline. Stunning demo, huge impact. Caveat: its SQuAD/HotpotQA eval was
REFUTED — you must define your own eval + KB. Papers: 2602.13229, 2510.27107.

**III4. NPU-accelerated RAG.** RAG on a Snapdragon X Elite NPU: 4× latency, 4–12× energy vs
CPU. ⚠️ Needs that specific NPU hardware — not pure software. Paper: 2606.11257.

## Domain IV — LLM Reasoning & Interpretability (UGR family)

**IV1. Uncertainty-Gated Reasoning (UGR) ⭐.** A reasoning model reads its own internal
activations and spends long chain-of-thought ONLY when unsure — matching full-reasoning
accuracy at 30–50% fewer tokens. Core = a tiny probe on a FROZEN model (no retraining) →
gate compute by predicted correctness. Result is a hard number (accuracy-vs-tokens Pareto
curve). Second contribution: probe is better-calibrated than the model's verbalized
confidence (exploits self-verification "positivity bias"). Baselines: fixed short/long CoT,
self-consistency@k, verbalized-confidence gate. Data: GSM8K + MATH + a code set. Model:
1.5–8B open reasoning model. Compute: one 24GB GPU. **Almost can't fully fail** — partial
result (compute savings at equal accuracy) still publishes.

**IV2. Closing the "hypocrisy gap" (faithful CoT via SAEs).** Train a model so its stated
reasoning matches its internal computation, measured by Sparse-Autoencoder features. The
Feb-2026 paper only *measures* the gap; you'd be first to *reduce* it (via DPO on
faithful/unfaithful preference pairs). High ceiling (a real safety contribution), high
variance (SAEs finicky; reproducing the gap metric is a hard month-1). Needs one patient
interpretability lead. Uses pre-trained SAEs (Gemma-Scope/Qwen-Scope/Llama-Scope).

**IV3. Adaptive process verification (PRM that decides when to verify).** Instead of
verifying every reasoning step at full cost, learn a risk estimate that triggers the
expensive verifier only on high-risk steps. This is literally GenPRM's stated future work
("prune the reasoning dynamically"; "extend beyond math"). Shares the internal-risk core
with UGR — a natural pivot target. Medium feasibility (needs a working PRM setup).

**IV4. Dense credit assignment for small-model long-horizon RLVR.** Make a 1.5B model learn
long multi-step reasoning by injecting intermediate rewards, solving the sparse-reward wall
(small models almost never hit a fully-correct trajectory by chance → zero reward → no
learning). Fixes are brand-new (co-distillation, optimal-transport-to-teacher). Hottest
science, but RL is unstable/reward-hacking/compute-heavy. **A trap unless someone already
knows GRPO/RLHF.**

## Domain V — Applied ML for Social Good

**V1. Satellite remote sensing for environmental crime & disaster ⭐.** Detect illegal
deforestation, methane super-emitters, or flood extent from FREE Sentinel-1/2 imagery,
with a time-slider map UI auto-flagging detections. Clouds/shadows/noise wreck detection
and early-enough detection is unsolved — that's the research knob. Real CV work (segmentation),
not LLM fine-tuning. Data free: Sentinel Hub, Google Earth Engine, Sen1Floods11, deforestation
benchmarks. Extend AttMetNet methane (2512.02751) or SAR deforestation work. Visually stunning
+ obvious societal weight.

**V2. Low-resource-language tutoring.** AFRILANGTUTOR: +1.8–15.5% over base across 10 African
languages; releases 194.7K dict + 78.9K tutor-QA. Repeat for your language (e.g. an Indian
language); build a held-out test set. Paper: 2604.20996.

**V3. Agricultural vision-language assistant.** Photograph a diseased crop → diagnosis +
treatment. Agri-3M-VL + AgriBench-VL-4K (pairwise win-rate). ⚠️ Confirm dataset links live.
Paper: 2510.04002.

**V4. On-device misinformation, low-resource language.** Small model flags false health claims
offline. Phi-4 best for Bangla claim extraction. Your edge: a natively-sourced (not translated)
dataset. Papers: 2607.12336, 2410.18390.

**V5. Automated accessibility code-fixing.** FixAlly turns a11y-scanner findings into source
fixes: 77% plausible / 69% accepted (iOS/SwiftUI). Port to Android/web = your novelty.
Paper: 2408.03827.

---

# Part 2 — Ranking matrix (all criteria)

Scores 1–5, higher = better for a capstone. Risk⁻ = low-failure-risk.

| ID | Idea | Feas | Pub | Novel | Impact | Demo | Cheap | Data | Risk⁻ | Tier |
|----|------|:----:|:---:|:-----:|:------:|:----:|:-----:|:----:|:-----:|:----:|
| II1 | LLM unit-test generation (ULT) | 5 | 5 | 3 | 4 | 3 | 5 | 5 | 5 | **S** |
| IV1 | Uncertainty-Gated Reasoning ⭐ | 4 | 5 | 4 | 4 | 3 | 4 | 5 | 4 | **S** |
| I1 | Malicious-package detector | 4 | 5 | 3 | 5 | 3 | 4 | 5 | 4 | **S** |
| I3 | Statement-level vuln detection | 4 | 5 | 3 | 4 | 2 | 4 | 5 | 4 | **S** |
| V1 | Satellite remote sensing ⭐ | 4 | 4 | 4 | 5 | 5 | 3 | 5 | 3 | **A** |
| III2 | Edge↔cloud inference router | 4 | 4 | 4 | 4 | 3 | 5 | 5 | 4 | **A** |
| III1 | SLM-specific quantization | 4 | 4 | 4 | 4 | 2 | 3 | 4 | 4 | **A** |
| I2 | Prompt-injection defense | 4 | 4 | 4 | 5 | 3 | 4 | 5 | 3 | **A** |
| II2 | Runtime code-review benchmark | 3 | 5 | 5 | 4 | 3 | 4 | 3 | 3 | **A** |
| V2 | Low-resource-language tutoring | 4 | 4 | 3 | 5 | 4 | 3 | 4 | 3 | **A** |
| II3 | End-to-end coding agent | 4 | 4 | 3 | 3 | 4 | 4 | 5 | 4 | **A** |
| III3 | Offline first-aid RAG | 4 | 3 | 3 | 5 | 5 | 4 | 2 | 3 | **B** |
| V4 | On-device misinformation | 4 | 3 | 3 | 5 | 4 | 4 | 3 | 3 | **B** |
| IV3 | Adaptive process verification | 3 | 4 | 4 | 4 | 3 | 3 | 4 | 3 | **B** |
| II4 | DSL program repair (SLMFix) | 4 | 4 | 3 | 3 | 2 | 4 | 3 | 4 | **B** |
| V5 | Accessibility code-fixing | 4 | 3 | 3 | 4 | 3 | 4 | 3 | 4 | **B** |
| V3 | Agricultural VLM | 3 | 3 | 3 | 5 | 4 | 3 | 3 | 3 | **B** |
| I4 | PQC migration tooling | 3 | 3 | 4 | 4 | 2 | 5 | 3 | 3 | **B** |
| I5 | Deepfake detection | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | **B** |
| IV2 | Hypocrisy gap (SAE faithfulness) | 2 | 4 | 5 | 5 | 3 | 3 | 3 | 2 | **C** |
| III4 | NPU-accelerated RAG | 2 | 3 | 4 | 4 | 4 | 2 | 3 | 2 | **C** |
| IV4 | Dense-reward small-model RLVR | 2 | 4 | 5 | 4 | 3 | 2 | 4 | 1 | **C** |
| I6 | C2PA provenance | 3 | 2 | 3 | 4 | 4 | 4 | 2 | 3 | **C** |
| I7 | Privacy+fairness FL (RESFL) | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | **C** |

---

# Part 3 — Tiered verdict

**S tier — pick one of these for the safest publishable result:**
- **II1 (ULT test-gen)** — lowest-risk possible: fixed harness, mature Python tooling, laptop-runnable, "SOTA 41% → we get X%".
- **IV1 (UGR)** — best research idea that still can't really fail (probe on a frozen model); hard-number result; hot area.
- **I1 (malicious packages)** — most industry-relevant; richest datasets; splits cleanly 3 ways.
- **I3 (SecVulEval)** — absurdly low 24% baseline makes "beat it" realistic.

**A tier — strong, minor caveat each:**
- **V1 (satellite)** — best *impressive-and-solves-a-real-problem* fit; risk is CV robustness under clouds/noise (but partial results still publish).
- **III2 (edge router)**, **III1 (quantization)** — clean systems papers.
- **I2 (prompt injection)** — max frontier "wow", but a moving target.
- **II2 (runtime code-review benchmark)** — highest novelty (you build the missing benchmark); needs sandbox infra.
- **V2 (tutoring)**, **II3 (coding agent)**.

**B tier — good but data/eval/niche caveats.** **C tier — high ceiling but high risk or hardware-gated; only with the right specialist.**

---

# Part 4 — Other recommendations (not in the original lists)

1. **Fuse IV1 + IV3 into one project.** They share an "internal risk signal" core. Frame UGR
   as the general method and adaptive-PRM as the instantiation for step-level verification.
   One coherent paper, natural pivot room if early results push you one way — de-risks the year.

2. **V1 + III2 combo (field-deployable detection).** Run the satellite detector's inference
   pipeline with an edge-routing layer so it works offline in the field, escalating only
   ambiguous tiles to cloud. Adds a systems contribution on top of the CV one — but only if
   the core detector works first; don't start here.

3. **Benchmark-first strategy.** Two of your best ideas (II2, and the eval-undefined III3)
   are strongest as *"we built the missing benchmark."* Examiners love a released dataset +
   leaderboard; it's citable and hard to argue with. If unsure about a modeling result,
   ship a benchmark instead.

4. **Reconcile team size.** 3 vs 4 changes what's viable: the 4-person UGR split (rollouts /
   probe / gating / eval) compresses fine to 3 (merge probe+gating). Anything in C tier
   (SAE, RLVR) really wants a 4th specialist — don't attempt with 3 unless one of you
   already has that background.

5. **Always lock the baseline version at project start** and cite the exact arXiv version.
   These SOTA numbers *will* move during your year; "we beat [v1, cited]" must stay true.

6. **Prefer software-only + free-data ideas** to kill two capstone killers (hardware access,
   data collection): II1, IV1, I3, III2, V1 all qualify. Avoid III4 (needs an NPU) and
   V3/V4 (dataset not confirmed live / must self-collect) unless you've verified access.

---

# Part 5 — Final pick

Weigh it by what you optimize for:

- **"Highest chance of a real paper"** → **IV1 (UGR)** or **II1 (ULT test-gen)**. Both have a
  hard, reproducible number and a partial-result escape hatch.
- **"Extremely impressive + solves a legitimate world problem"** (your original words) →
  **V1 (satellite remote sensing)**. Stunning demo, undeniable societal weight, free data,
  real CV research — and still publishable.
- **Most industry-relevant / job-signal** → **I1 (malicious packages)** or **I2 (prompt injection)**.

If forced to name one that best satisfies *both* "impressive + real-world" and "publishable
+ feasible for 3": **V1 (satellite)** for the showcase, **IV1 (UGR)** for the safest science.
Start with whichever the team's strongest skill matches — CV/geospatial → V1; ML/LLMs → IV1.
