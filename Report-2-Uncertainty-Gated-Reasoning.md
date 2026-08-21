# Review Report II

## Uncertainty-Gated Reasoning: Allocating Test-Time Compute from a Frozen Model's Internal State

**Innovative Design Project — Review 1 (Problem Identification and Proposed Methodology)**

**Team size:** 3 · **Duration:** one academic year · **Compute requirement:** one 24 GB GPU

---

## 1. Problem Identification

### 1.1 The technical problem

Large reasoning models (o1-style systems, DeepSeek-R1 and its distillations, Qwen3 in thinking mode)
achieve their accuracy by emitting a long chain of thought before answering. That chain is where the
accuracy comes from, and it is also the entire cost: thousands of generated tokens per query, with
latency and price scaling linearly in tokens emitted.

The allocation is uniform. A reasoning model spends comparable effort on *"what is 2 + 2"* and on a
competition-level olympiad problem, because nothing in the inference pipeline estimates how much
reasoning the current input requires. The obvious framing — "reasoning is expensive, so use less of it"
— is wrong, because reducing reasoning uniformly costs accuracy on exactly the inputs that need it. The
correct framing is **allocation**: spend the budget where it changes the answer.

### 1.2 More thinking is not merely wasteful — it is actively harmful

This is the finding that upgrades the problem from an efficiency concern to a correctness concern. Zhou
et al. [R4] measure answer *flips* as the token budget grows on a reasoning model. Beyond
approximately 7,000 tokens, negative flips (correct → incorrect) begin to exceed positive flips; the
flip ratio reaches **1.09 at 7K tokens (p = 0.014)** and **7.55 at 16K tokens**. Qualitative analysis
attributes **67.5%** of these to genuine overthinking — the model reaching a correct answer, explicitly
reconsidering, and rejecting it. They also show that difficulty modulates the optimum sharply:
easy problems (levels 1–2) peak at roughly **1.5K tokens** while hard problems (level 5) peak near
**8K**.

A uniform policy therefore cannot be optimal for any mixed workload. Set the budget for the hard tail
and you damage the easy majority; set it for the easy majority and you fail the tail. The survey
literature states the same conclusion in general form: current systems "apply fixed inference-time
compute regardless of task complexity, often overthinking simple problems while underthinking hard
ones" [R5].

### 1.3 Why the existing solutions are unsatisfying

Three families of solution exist, each with a structural defect.

**(a) Ask the model.** Prompt it to verbalise a confidence, then gate on that. This is known not to
work. Verbalised confidence is systematically inflated, and RLHF makes it worse — aligned models are
more overconfident than their pretrained counterparts. A COLM 2026 mechanistic study localises the
cause: a compact set of "Confidence Mover Circuits," primarily MLP blocks and attention heads in
middle-to-late layers, that write a confidence-inflation signal into the output [R6]. The signal we
want is present in the network; the verbalisation stage is where it is corrupted.

**(b) Retrain the model to decide.** AdaptThink [R7] and Thinkless [R8] teach a reasoning model to
choose its own mode via reinforcement learning, and the results are strong — AdaptThink reduces average
response length by **50.9% / 63.5% / 44.7%** on GSM8K / MATH-500 / AIME 2024 for
DeepSeek-R1-Distill-Qwen-1.5B *while improving* accuracy by 4.1 / 1.4 / 1.6 points, selecting
NoThinking for **86.9%** of GSM8K problems but only **40.4%** of AIME 2024. Thinkless reports 50–90%
reduction in long-chain usage. The defect is not the result but the mechanism: RL on the backbone must
be repeated for every model, alters the model's behaviour in the "think" branch as well as the gate,
and carries the standard risk that the run simply fails to converge. For a three-person undergraduate
team on one GPU, this is a project that can end with nothing.

**(c) Gate on cheap surface features.** The closest prior work, Zhai et al. [R2], solves a constrained
allocation problem via Lagrangian relaxation and then trains "a lightweight classifier to predict
oracle actions from cheap input features," reporting up to **12.8% relative accuracy improvement on
MATH under matched budget** and >91% imitation accuracy against the oracle. This is the right shape of
solution with an impoverished input: surface features of the prompt cannot see what the model itself
knows. Their framing confirms that a lightweight external gate is the deployable answer; it leaves the
question of what that gate should read.

### 1.4 Problem statement

*A reasoning model's own internal state, at the moment the prompt has been read and before any token is
generated, plausibly encodes whether extended reasoning will change the answer. No existing method
reads it for this purpose: verbalised-confidence gating reads a corrupted downstream signal, RL-based
gating modifies the model instead of reading it, and feature-based gating reads only the prompt's
surface. The problem is to extract a marginal-utility-of-compute signal from a **frozen** model's
activations and use it to allocate reasoning budget, and to evaluate that allocation under controls
strong enough to rule out the trivial explanations.*

---

## 2. Justification

**2.1 The signal is already known to exist — the enabling result is very recent.** Di Cicco [R1]
demonstrates that code correctness is **linearly decodable from hidden states at the final prompt
token, before any generation**, achieving held-out AUC **0.881 ± 0.008** across 50 outer splits on 444
LiveCodeBench tasks with Qwen3-4B. This is close to a proof of feasibility for our core mechanism:
pre-generation activations carry a robust, linearly accessible signal about the eventual outcome. CCPS
[R9] independently shows that perturbation-response features from final hidden states predict answer
correctness across Llama, Qwen and Mistral at 8B–32B on MMLU and MMLU-Pro. We are not gambling on
whether an internal signal exists; we are repointing an established signal at a different decision.

**2.2 The critical control has already been published, and almost nobody uses it.** The same paper
reports that a **prompt-length-only baseline reaches AUC 0.657**, and that after residualising for
prompt length its probe still holds **0.842** [R1]. This matters enormously: a large fraction of
adaptive-compute papers never test whether their "difficulty estimator" is a length detector wearing a
costume. Adopting length-residualised evaluation as a mandatory control is both a defence of our own
result and a criticism of the field we can substantiate.

**2.3 The target decision is different from the target of every calibration paper.** The calibration
literature predicts *whether the answer is correct*. We predict *whether spending more tokens will
change the answer*. These come apart in both directions: a problem the model will reliably get right
with short reasoning is low-value to think about (high correctness, zero marginal utility), and a problem
it will get wrong either way is equally low-value (low correctness, zero marginal utility). Compute
should go to the band in between. No surveyed work targets this quantity directly.

**2.4 The design cannot catastrophically fail.** The model is frozen. There is no fine-tuning, no
reinforcement learning, no reward model — nothing that can fail to converge after two months of GPU
time. The learned component is a linear or shallow classifier over extracted features. Either the
signal separates the classes or it does not, and we know which within weeks. Even the negative outcome
is publishable in combination with the calibration comparison, and even a modest token saving at equal
accuracy is a result.

**2.5 Cost and access are trivial.** All datasets are public (GSM8K, MATH-500, AIME, LiveCodeBench).
All models are open weights in the 1.5B–8B range. One 24 GB GPU suffices. There is no annotation
requirement, no human-subject component, no hardware, and no API spend for the core experiments.

**2.6 The area is active and the venue path is clear.** Two 2025–2026 surveys organise it [R5, R11],
an ICLR 2026 paper works the adjacent difficulty-adaptive problem [R10], and the efficient-reasoning
workshop circuit is well established. There is no risk of the topic being unrecognisable to reviewers.

---

## 3. Objectives

| # | Objective | Success criterion |
|---|-----------|-------------------|
| **O1** | Quantify the available headroom by constructing an oracle gate (per-item optimal budget from sampled outcomes) on each benchmark. | An explicit accuracy-versus-token Pareto frontier and the oracle's token saving at equal accuracy — the ceiling any method can reach. |
| **O2** | Train activation probes on a **frozen** reasoning model to predict the marginal utility of extended reasoning for a given input. | Held-out AUROC ≥ 0.80 **after length residualisation**, against the length-only baseline (≈0.657 reference from [R1]). |
| **O3** | Convert the probe into a deployable gate and measure the realised trade-off. | Match full-reasoning accuracy (within 1 point) at **30–50% fewer generated tokens**; full Pareto curve reported, not a single operating point. |
| **O4** | Compare the internal signal against verbalised confidence and against self-consistency as gating signals. | Lower ECE and higher AUROC than verbalised confidence; competitive with self-consistency@k at a fraction of its cost. Reference point: ECE₂ 0.089 reported by [R3]. |
| **O5** | Establish that the probe measures difficulty-relevant structure rather than surface artefacts. | Length-matched controls, token-count residualisation, cross-dataset transfer, and cross-model probe transfer, all reported including failures. |
| **O6** | Release probes, extraction harness, sampled-outcome labels and evaluation protocol. | Public artefact; per-item labels for ~4,000 items reusable by others. |

**Stretch objective (O7).** A risk-controlled gate: choose the probe threshold via conformal
calibration so that accuracy loss relative to always-think is bounded by a user-specified ε with high
probability. This converts a research curve into something with a deployment contract, and is the most
likely patent/product angle if we pursue one.

---

## 4. Scope

### 4.1 In scope

- **Models:** DeepSeek-R1-Distill-Qwen-1.5B and 7B, Qwen3-4B and 8B (thinking/non-thinking modes).
  Open weights only, versions pinned at project start.
- **Tasks:** mathematical reasoning (GSM8K, MATH-500), competition mathematics (AIME 2024/2025 as a
  hard out-of-distribution slice), and code reasoning (LiveCodeBench subset, chosen for direct
  comparability with [R1]).
- **Intervention point:** the reasoning budget decision — think vs. short-answer, and a graded budget
  variant. Made **pre-generation** at the final prompt token; a secondary mid-generation "continue or
  stop" variant is in scope as an ablation.
- **Learned component:** linear probes and shallow MLPs over residual-stream activations. Frozen
  backbone throughout.
- **Evaluation:** accuracy-versus-token Pareto curves, probe discrimination and calibration, and the
  full battery of controls in O5.

### 4.2 Explicitly out of scope

- **Any modification of the backbone.** No SFT, no RL, no LoRA on the reasoning model. This is the
  design decision that makes the project safe, and it is not negotiable mid-project.
- **Beating AdaptThink or Thinkless on raw token reduction.** They retrain the model; we do not. Their
  numbers are reported as *context*, and any comparison is explicitly labelled not like-for-like. Our
  claim is about the signal and the cost of obtaining it, not about topping a leaderboard.
- **Sparse-autoencoder interpretability of the probe.** Interesting, high-variance, and a separate
  project.
- **Proprietary/API models.** Activations are inaccessible, so they cannot be studied and their version
  drift breaks reproducibility.
- **Open-ended generation, multi-turn dialogue, agentic tool use.** Correctness must be automatically
  checkable for the label-generation stage to work.
- **Training a new reasoning model, or any claim about pretraining.**

### 4.3 Assumptions

Open-weight reasoning models remain downloadable at pinned versions; one 24 GB GPU is available for the
full year; benchmark contamination, while a general concern, does not differentially affect a
*within-item* comparison of short versus long reasoning (this is a genuine methodological advantage of
our label construction, since both branches see the same possibly-contaminated item).

---

## 5. Preliminary Literature Survey

### 5.1 Survey method

Search over arXiv, OpenReview, ACL Anthology and ICLR/COLM 2026 proceedings for January 2025 – August
2026, over the query families *{adaptive test-time compute, efficient reasoning, overthinking, reasoning
length control, hidden-state probing, LLM calibration, verbalised confidence}*, with citation chasing
from the two surveys. Fourteen works retained, thirteen from 2025–2026.

### 5.2 Summary of surveyed work

| Ref | Work | Year / venue | Core contribution | Key reported numbers |
|-----|------|--------------|-------------------|----------------------|
| **R1** | Di Cicco — *Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation* | Jun–Jul 2026, arXiv 2606.14530 | Linear probes on final-prompt-token hidden states predict eventual code correctness pre-generation | AUC **0.881 ± 0.008** (50 outer splits); length-residualised **0.842 ± 0.010**; **prompt-length baseline 0.657 ± 0.014**; Qwen3-4B, 444 LiveCodeBench tasks |
| **R2** | Zhai, Li, Xiao, Li, Wang — *Adaptive Test-Time Compute Allocation for Reasoning LLMs via Constrained Policy Optimization* | Apr 2026, arXiv 2604.14853 | Lagrangian "solve-then-learn": binary-search oracle actions, then a light classifier over **cheap input features** | Up to **+12.8%** relative accuracy on MATH at matched budget; **>91%** imitation accuracy; DeepSeek-V3, GPT-4o-mini, Qwen2.5-7B |
| **R3** | Zollo, Wang, Zemel — *Unsupervised Confidence Calibration for Reasoning LLMs from a Single Generation* | Apr 2026, arXiv 2604.19444 | Self-consistency (k=100, offline, unlabelled) as weak supervision for a predictor over final-token embeddings; single generation at deployment | **ECE₂ 0.089** (Qwen avg.); >50% ECE reduction with as few as 5 samples; under shift ECE₂ 0.09–0.13 vs baselines 0.15–0.38; Qwen3 0.6B–14B, R1-Distill, Nemotron; GSM8K, PolyMath, SciQ, TriviaQA, WebQuestions |
| **R4** | Zhou et al. — *When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling* | Apr 2026, arXiv 2604.10739 | Measures answer flips as budget grows; establishes that extended reasoning destroys correct answers | Flip ratio **1.09 @ 7K tokens (p=0.014)**, **7.55 @ 16K**; **67.5%** genuine overthinking; easy peak ~1.5K vs hard ~8K tokens |
| **R5** | Alomrani et al. — *Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs* | Jul 2025, arXiv 2507.02076 | Two-tier taxonomy: L1-controllability (fixed budget) vs L2-adaptiveness (scale by difficulty/confidence) | Survey; names hybrid thinking models as the emerging trend |
| **R6** | *Wired for Overconfidence: A Mechanistic Perspective on Inflated Verbalized Confidence in LLMs* | COLM 2026, arXiv 2604.01457 | Circuit-level localisation of "Confidence Mover Circuits" — mid-to-late MLP blocks and attention heads writing the inflation signal | Intervening on these components substantially improves verbalised calibration; confirms RLHF exacerbates overconfidence |
| **R7** | Zhang et al. — *AdaptThink: Reasoning Models Can Learn When to Think* | EMNLP 2025 (main), arXiv 2505.13417 | RL algorithm teaching a reasoning model to select Thinking vs NoThinking | Length **−50.9 / −63.5 / −44.7%** on GSM8K / MATH-500 / AIME24 with accuracy **+4.1 / +1.4 / +1.6** (1.5B); NoThinking chosen for **86.9%** of GSM8K vs **40.4%** of AIME24 |
| **R8** | Fang et al. — *Thinkless: LLM Learns When to Think* | 2025, arXiv 2505.13379 | Control-token (`<think>`/`<short>`) mode selection trained by decoupled GRPO | **50–90%** reduction in long-chain usage on MATH-500 / GSM8K |
| **R9** | *CCPS: Calibrating LLM Confidence by Probing Perturbed Representation Stability* | 2025, arXiv 2505.21772 | Adversarial perturbation of final hidden states; features of the response used by a light classifier to predict correctness | Llama / Qwen / Mistral, 8B–32B; MMLU, MMLU-Pro; outperforms prior confidence methods |
| **R10** | *DiffAdapt: Difficulty-Adaptive Reasoning* | ICLR 2026 | Adapts reasoning effort using an **entropy** signal as the difficulty proxy | Token reduction at maintained accuracy |
| **R11** | *Don't Overthink It: A Survey of Efficient R1-style Large Reasoning Models* | Aug 2025, arXiv 2508.02120 | Taxonomy of efficiency techniques for R1-style models | Survey |
| **R12** | *Stop When Reasoning Converges: Semantic-Preserving Early Exit for Reasoning Models* | 2026, arXiv 2605.17672 | Mid-generation early exit when the reasoning trace semantically converges | Complementary intervention point (during, not before, generation) |
| **R13** | *Calibrating LLM Judges: Linear Probes for Fast and Reliable Uncertainty Estimation* | 2025, arXiv 2512.22245 | Linear probes for uncertainty in the LLM-as-judge setting | Establishes the linear-probe recipe in an adjacent task |
| **R14** | *ADaPT: Token-Level Decoupling for Efficient Large Reasoning Models* | 2026, arXiv 2606.19919 | Token-level compute decoupling within the reasoning trace | Finer-grained, orthogonal intervention |

### 5.3 Critical analysis: where each work falls short, and how we correct it

**R1 — pre-generation decodability (our enabling result, and a narrow one).**
*Flaw 1 (single model, single domain).* One model (Qwen3-4B), one benchmark (444 LiveCodeBench tasks).
Generality is asserted, not shown.
*Flaw 2 (predicts the wrong thing for our purpose).* The target is *correctness*, not the *marginal
value of additional reasoning*. A gate built on correctness prediction will happily spend a long chain
of thought on an item the model will get wrong regardless — pure waste — and will withhold reasoning
from an item it can get right only *with* reasoning.
*Flaw 3 (no downstream use).* The paper stops at AUC. It never closes the loop to an allocation policy,
so it demonstrates a signal without demonstrating that the signal is worth anything.
*Flaw 4 (an unexplained negative left open).* Self-repair geometry could not be analysed "due to
insufficient successful repair instances," and non-linear probes did not beat linear ones — reported
without resolution.
**Our correction.** We adopt R1's methodology wholesale (final-prompt-token probing, nested outer
splits, leakage-free protocol, length residualisation) because it is the most rigorous evaluation
protocol in this literature, and change the *label*: from "will the answer be correct" to "will extra
reasoning change the answer." We test three models across four datasets, and we close the loop to a
gate with a measured Pareto curve — which is precisely what R1 omits.

**R2 — constrained-policy allocation (closest prior art, and the one to beat).**
*Flaw 1 (blind features).* The classifier reads "cheap input features" of the prompt. The model's own
representation of the problem — which encodes what it knows, what it has seen, and where it is
uncertain — is unused. Two prompts with identical surface statistics can be trivial and impossible for
a given model, and surface features cannot separate them.
*Flaw 2 (model-specific oracle, generic features).* The oracle actions are derived from a specific
model's behaviour, but the features are model-agnostic, so the classifier must learn a
model-specific function through a model-blind input. This is a structural information bottleneck.
*Flaw 3 (no length control reported).* With prompt-surface features and no length residualisation, we
cannot tell how much of the 91% imitation accuracy is length detection — and R1 shows length alone gets
0.657 AUC on a related task.
*Flaw 4 (partly closed models).* DeepSeek-V3 and GPT-4o-mini are API models; reproducibility depends on
unversioned endpoints.
**Our correction.** We keep R2's oracle construction (it is the right way to define the target) and
replace the input: internal activations instead of surface features, which is exactly the missing
information. We add the length-residualised evaluation R2 lacks and report the delta between a
surface-feature gate and an activation gate as a direct, controlled comparison — making R2 our
principal baseline rather than a competitor we ignore.

**R3 — unsupervised calibration from a single generation.**
*Flaw 1 (post-hoc by construction).* The predictor reads embeddings of the *completed* generation. It
can tell you afterwards how much to trust an answer; it cannot decide beforehand how much to spend.
For allocation, this is the wrong side of the decision.
*Flaw 2 (expensive offline stage, admitted).* k = 100 samples per item on unlabelled calibration data,
and the authors concede the method "relies on offline sampling, which may be resource-intensive and
need to be repeated over time."
*Flaw 3 (inherits self-consistency's failure mode, admitted).* Where agreement correlates weakly with
correctness, the weak supervision is wrong — and agreement is weakest exactly on hard items, which are
the items that matter for allocation.
*Flaw 4 (scope, admitted).* Restricted to "relatively well-defined settings with automatic evaluation."
**Our correction.** We move the probe to the pre-generation position, which is the only position from
which a budget decision can be made. We adopt their self-consistency-as-weak-supervision trick for
label generation where gold answers are unavailable — with the important difference that our label is a
*difference* between two sampled branches (long vs short), so consistent-but-wrong behaviour still
yields a correct "extra thinking won't help" label. Their ECE₂ of 0.089 becomes our calibration
reference point, and their method becomes a baseline in O4.

**R4 — overthinking measurement (our motivation, and it stops at diagnosis).**
*Flaw 1 (no intervention).* The paper establishes the pathology beautifully and proposes no controller.
Its own conclusion — that the optimum is difficulty-dependent, ~1.5K vs ~8K tokens — is an argument for
exactly the gate it does not build.
*Flaw 2 (difficulty is taken from dataset labels).* The analysis uses annotated difficulty levels. A
deployed system does not have them; predicting difficulty is the actual problem.
*Flaw 3 (causal mechanism unresolved, admitted).* The authors state that "definitive causal mechanisms
underlying overthinking requires further investigation through controlled interventions."
*Flaw 4 (domain and model scope, admitted).* Mathematical and scientific reasoning only; open-weight
models only.
**Our correction.** We build the controller R4 argues for, and replace annotated difficulty with a
predicted internal signal — which is the only version that deploys. We additionally adopt their *flip
rate* as a secondary evaluation metric: a good gate should reduce the negative-flip rate, not merely
save tokens, and no adaptive-compute paper we surveyed reports this. That is a cheap, defensible extra
contribution.

**R7, R8 — AdaptThink and Thinkless (the strongest results, obtained the expensive way).**
*Flaw 1 (the backbone is modified).* RL on the reasoning model means the resulting artefact is a
different model. The gate cannot be transplanted, audited separately, or removed; and the "think"
branch is no longer the original model's behaviour, so the comparison against the base model conflates
gating with fine-tuning gains. Some of AdaptThink's *accuracy improvement* is plausibly RL benefit
rather than allocation benefit — the paper does not decompose it.
*Flaw 2 (cost and repeatability).* Every new model requires a new RL run. For an organisation with a
model zoo, or a student team with one GPU, this does not scale.
*Flaw 3 (binary mode).* Think or not-think. R4's evidence is that the optimum is graded (1.5K vs 8K),
not binary.
*Flaw 4 (no internal-signal analysis).* Whether the learned policy exploits a signal that was already
present in the frozen model is never asked — which is precisely our research question.
**Our correction.** A detachable probe over a frozen model: portable across models, auditable in
isolation, removable, and leaving the base model's think-branch behaviour untouched, so any measured
saving is attributable to allocation alone. We support graded budgets, not a binary switch. And we
answer the question R7/R8 leave open — how much of their gain was available without touching the
weights. If our frozen probe recovers a large share of AdaptThink's reduction, that is a genuinely
interesting scientific finding about where the information lives; if it recovers little, that is an
equally interesting negative result about what RL adds. Both outcomes are reportable.

**R6 — mechanistic account of verbalised overconfidence.**
*Flaw:* diagnostic and interventional at the calibration level; it never connects the finding to
resource allocation, and its intervention edits the model's components (a modification we rule out).
**Our correction.** We use R6 as the *explanation* for our O4 result rather than as a method. If our
internal probe beats verbalised confidence as a gating signal, R6 supplies the mechanism — the signal
is corrupted between the mid-to-late layers and the emitted token — which converts an empirical
observation into an explained one. This is how our calibration finding becomes a contribution rather
than a table.

**R9, R13 — probing for correctness and for judge uncertainty.**
*Flaw:* both read the response or perturb the final state after the answer exists; both target
correctness rather than marginal utility; and R9's perturbation stage adds inference cost, which is
self-defeating for a mechanism whose purpose is to save inference cost.
**Our correction.** Pre-generation, single forward pass, no perturbation — the gate's overhead must be
negligible relative to the tokens it saves, and we report that overhead in milliseconds as a
first-class metric. Cost-of-gate is absent from most of this literature.

**R10 — DiffAdapt (entropy as the difficulty signal).**
*Flaw:* entropy is a one-dimensional, output-distribution summary. It conflates several distinct states
— genuine ambiguity, multiple valid phrasings, and knowledge gaps — and is only weakly connected to
whether *reasoning* helps. It is also computed at the output layer, discarding the richer intermediate
representation.
**Our correction.** Entropy becomes one of our baselines (a cheap, sensible one) and one of our probe's
input features, so we can report how much the full activation vector adds over the entropy scalar. That
decomposition is a clean, publishable ablation.

**R12, R14 — mid-generation early exit and token-level decoupling.**
*Flaw:* both act *during* generation, so cost is already being incurred before the decision, and neither
can decline to think in the first place.
**Our correction.** Complementary rather than competing, and we say so: our pre-generation gate composes
with R12-style early exit. If time permits, the combined policy (allocate before, exit early within) is
an additional experiment with a plausible multiplicative effect.

**R5, R11 — surveys.**
*Flaw:* both taxonomise; neither measures. R5's L2-adaptiveness category is defined as scaling by
"input difficulty or model confidence" — conflating two things our work deliberately separates, since
model confidence is measurable internally and input difficulty is not intrinsic to the input at all but
relative to the model.
**Our correction.** We adopt R5's L1/L2 vocabulary for positioning and then split its L2 category into
*externally estimated difficulty* and *internally read state*, which is the distinction our experiment
isolates.

### 5.4 Consolidated research gap

| Capability | R1 | R2 | R3 | R4 | R7/R8 | R9 | R10 | **Ours** |
|---|---|---|---|---|---|---|---|---|
| Reads internal activations | ✔ | ✘ | ◐ | ✘ | ✘ | ✔ | ✘ | ✔ |
| Decision made **pre**-generation | ✔ | ✔ | ✘ | ✘ | ✔ | ✘ | ◐ | ✔ |
| Backbone left frozen | ✔ | ✔ | ✔ | ✔ | ✘ | ✔ | ✘ | ✔ |
| Target = marginal utility of compute | ✘ | ✔ | ✘ | ✘ | ◐ | ✘ | ◐ | **✔** |
| Closes loop to an allocation policy | ✘ | ✔ | ✘ | ✘ | ✔ | ✘ | ✔ | ✔ |
| Length-residualised controls | ✔ | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | ✔ |
| Reports gate compute overhead | ✘ | ◐ | ✘ | — | ✘ | ✘ | ✘ | **✔** |
| Reports negative-flip-rate change | ✘ | ✘ | ✘ | ✔ | ✘ | ✘ | ✘ | **✔** |
| Graded (not binary) budget | — | ✔ | — | — | ✘ | — | ◐ | ✔ |

*(✔ present · ◐ partial · ✘ absent · — not applicable)*

**The single sentence.** No existing work reads a frozen model's pre-generation internal state to
predict the *marginal utility of additional reasoning* and uses it to allocate budget under
length-controlled evaluation. Every ingredient exists separately; the combination does not.

---

## 6. Novelty of the Proposed Work

**N1 — A new prediction target: marginal utility of compute.** We predict Δ = p(correct | long CoT) −
p(correct | short CoT) per item, rather than p(correct). This is the quantity an allocator actually
needs, and it is not monotone in correctness — both the easy and the hopeless deserve zero budget. The
calibration literature [R1, R3, R9] predicts correctness; the allocation literature [R2, R10] predicts
difficulty or entropy. Neither predicts the difference.

**N2 — Pre-generation activation-based gating on a frozen model.** R1 establishes pre-generation
decodability but builds no policy; R2 builds the policy but from surface features; R7/R8 build a policy
by retraining the model. The combination — read the frozen model's own state, decide before the first
token, change nothing in the weights — is unoccupied, and it is the version that is portable, auditable
and removable.

**N3 — A controlled attribution of gating gains to allocation rather than fine-tuning.** Because the
backbone is untouched, any token saving at equal accuracy is attributable to allocation alone. This lets
us answer a question the RL papers cannot: *how much of the adaptive-thinking benefit was already
latent in the frozen model?* Both possible answers are scientifically interesting, which is why this
framing is also the project's insurance policy.

**N4 — Length-residualised evaluation as a required protocol, applied as a critique.** We adopt R1's
control and extend it into a small audit: re-evaluate the published-style gating signals (entropy,
verbalised confidence, prompt-surface features) under length residualisation and report how much of
each survives. Given that length alone reaches AUC 0.657 in the comparable setting [R1], we expect this
to be a substantive and slightly uncomfortable contribution to the field.

**N5 — Two evaluation dimensions this literature omits: gate overhead and flip-rate reduction.** A
gating method's cost must be netted against its saving (most papers do not report it), and R4's
negative-flip pathology gives a correctness-side metric that token counts miss. Reporting both makes
our evaluation strictly stronger than the papers we compare against.

**N6 — Public per-item marginal-utility labels.** Producing the sampled long/short outcome distributions
for ~4,000 items across three models is expensive and reusable; it is the dataset that makes N1
studyable by anyone else.

**Note on IP.** Unlike Report I, this project is optimised for **publication, not patent**. The
plausible claimable element is O7 (the risk-controlled gate with a bounded-accuracy-loss guarantee),
and if we pursue it the provisional must precede any preprint. Our recommendation to the guide is to
treat this project as the paper-track option and Report I as the patent-track option.

---

## 7. Proposed Methodology

### 7.1 Pipeline

```
 Stage 1  LABEL GENERATION (expensive, offline, one-time per model)
          for each item: sample n long-CoT and n short/no-think responses
          → p_long, p_short → Δ = p_long − p_short  → label
                    │
 Stage 2  FEATURE EXTRACTION (frozen model, single forward pass)
          residual-stream activations at final prompt token, all layers
          (+ output entropy, + prompt length — as features AND as controls)
                    │
 Stage 3  PROBE TRAINING
          logistic regression / shallow MLP · nested CV, 50 outer splits
          length-residualised variant trained and reported alongside
                    │
 Stage 4  GATE POLICY
          threshold sweep → accuracy-vs-token Pareto · graded budget variant
          conformal threshold for bounded accuracy loss (O7)
                    │
 Stage 5  EVALUATION vs 7 baselines · controls · ablations · overhead
```

### 7.2 Stage 1 — Label generation (the real compute cost, and it is bounded)

For each item, sample n = 8 responses under long chain-of-thought and n = 8 under short/no-think mode,
score each against gold, and estimate Δ. Items are then assigned to three classes:
**needs-reasoning** (Δ above threshold), **reasoning-neutral** (|Δ| small, high accuracy — the savings
opportunity), and **hopeless** (both branches near zero — also no budget, and separating this class from
"neutral" is a distinction correctness-probes cannot make).

Where gold answers are unavailable we substitute self-consistency agreement as weak supervision,
following [R3] — with the advantage noted in §5.3 that our label is a *difference* of two branches, so a
consistently-wrong model still yields a valid "extra thinking won't help" label.

**Cost estimate (this is the binding constraint, so it is stated explicitly).** ≈4,000 items × 16
samples × ≈1.5K mean tokens ≈ 10⁸ generated tokens per model. On a 24 GB GPU with a 1.5B model under
vLLM this is on the order of days, not weeks; the 7–8B models are batched overnight over the mid-project
period. Mitigation if it overruns: reduce to n = 4 with wider Δ thresholds (R3 reports >50% ECE
reduction with as few as 5 samples, which suggests small n is workable), and cut the item count on the
easiest dataset first. This stage is scheduled early precisely so that overrun is visible in month 3
rather than month 9.

### 7.3 Stage 2 — Feature extraction

Single forward pass over the prompt on the frozen model; capture residual-stream activations at the
final prompt token from every layer. A layer sweep identifies the most informative depth (R6's finding
that confidence signals concentrate in middle-to-late layers gives a strong prior). Auxiliary features:
output-distribution entropy (the R10 signal, included so we can measure what activations add over it)
and prompt token count (included as a feature in one arm and as a residualisation control in another).

The secondary mid-generation variant extracts activations at fixed token checkpoints during a reasoning
trace, giving a "continue or stop" gate for the composition experiment with R12-style early exit.

### 7.4 Stage 3 — Probe training

L2-regularised logistic regression as the primary model, with a shallow MLP as a capacity check. R1
reports that non-linear probes did not beat linear ones on the related task, so we expect linear to
suffice and will report the comparison either way.

Protocol, taken directly from R1 because it is the most defensible in this literature: nested
cross-validation with 50 outer splits, strict leakage prevention (no item appears in both the label-
generation calibration and the probe test fold), and every headline number reported twice — raw and
length-residualised.

### 7.5 Stage 4 — Gate policy

Sweep the probe threshold to trace the full accuracy-versus-token frontier; report the curve, not a
cherry-picked point. Two variants:

- **Binary gate** — think or short-answer, for comparability with R7/R8.
- **Graded gate** — probe output mapped to one of k budget levels (e.g. 512 / 2K / 8K tokens), motivated
  directly by R4's finding that the optimum is ~1.5K for easy and ~8K for hard items.

**Risk-controlled variant (O7).** Split-conformal calibration on held-out data selects the threshold
guaranteeing accuracy loss ≤ ε with probability 1 − δ relative to always-think. This is what makes the
result deployable rather than merely interesting.

### 7.6 Stage 5 — Baselines, controls, ablations

**Baselines.**
1. Always-think (accuracy ceiling, token ceiling).
2. Never-think / short-answer only (token floor).
3. Fixed truncated budgets at several levels (the L1-controllability family, [R5]).
4. Verbalised-confidence gate (the naive approach; expected to lose, with R6 explaining why).
5. Self-consistency@k gate (strong but expensive; also the R3 comparison point).
6. Output-entropy gate (the R10 signal).
7. **Prompt-surface-feature gate** — a reimplementation of R2's input class, which is the controlled
   comparison that isolates our contribution.
8. Prompt-length-only gate (the trivial baseline; R1's 0.657 reference).
9. Oracle gate (O1 — the ceiling).
10. AdaptThink / Thinkless published numbers as external context, **explicitly labelled not
    like-for-like** since they retrain the backbone.

**Controls.** Length residualisation on every metric; length-matched evaluation subsets; permutation
test on probe labels; verification that the probe is not separating datasets rather than items when
pooled.

**Ablations.** Layer depth; probe capacity; n in label generation; activations-only vs
activations+entropy vs entropy-only; cross-dataset transfer (train on MATH, test on GSM8K and
LiveCodeBench); **cross-model transfer** (does a probe trained on 1.5B transfer to 7B — a strong result
if yes, an informative limitation if no); binary vs graded gate.

**Metrics.** Accuracy at matched token budget; token reduction at matched accuracy; area under the
accuracy-cost curve; probe AUROC/AUPRC (raw and residualised); ECE and Brier for calibration; **negative
flip rate** (from R4); **gate wall-clock overhead in ms and as a fraction of tokens saved**.

### 7.7 Tooling and work split

PyTorch, HuggingFace Transformers, vLLM for the sampling stage, TransformerLens or plain forward hooks
for activation capture, scikit-learn for probes. One 24 GB GPU. All public data.

Three-way split: **(A)** sampling infrastructure and label generation (the compute-heavy,
schedule-critical part); **(B)** activation extraction, probe training, controls; **(C)** gate policy,
baselines, calibration comparison, evaluation harness. Interfaces are two files — a per-item label
table and a per-item activation tensor store — so the three streams decouple after month 3.

### 7.8 Indicative timeline

| Months | Milestone |
|---|---|
| 1 | Environment, model/version pinning, reproduce a published reasoning-benchmark number end to end |
| 2 | Sampling harness; pilot label generation on 300 GSM8K items; **first go/no-go: does Δ have usable variance?** |
| 3–4 | Full label generation for the 1.5B model; activation extraction; first probes; **second go/no-go: residualised AUROC > 0.7?** |
| 5 | Gate policy, first Pareto curve — **primary result exists here** |
| 6–7 | Scale to 7–8B models; cross-dataset and cross-model transfer |
| 8 | Baseline suite complete, including the R2-style surface-feature comparison |
| 9 | Calibration study (O4) and the length-residualisation audit (N4) |
| 10 | Conformal risk-controlled gate (O7); flip-rate analysis |
| 11–12 | Ablations, write-up, artefact release, demonstration |

The two explicit go/no-go gates in months 2 and 4 are the point of the design: the project's central
hypothesis is tested cheaply and early, and a negative answer at month 4 still leaves eight months to
convert the work into the calibration-and-audit paper (O4 + N4), which does not depend on the gate
working.

---

## 8. SWOT Analysis

### Strengths

| # | Strength | Evidence |
|---|---|---|
| S1 | **The project cannot fail catastrophically.** Frozen backbone, no RL, no fine-tuning; the learned component is a linear classifier. | §2.4 |
| S2 | The core signal is already demonstrated to exist by an independent 2026 paper. | AUC 0.881 pre-generation [R1]; CCPS across 4 model families [R9] |
| S3 | Motivation is quantified rather than asserted, with a striking headline number. | Flip ratio 7.55 at 16K tokens; 67.5% genuine overthinking [R4] |
| S4 | Cheap and self-contained: one 24 GB GPU, public data, no annotation, no API spend, no hardware. | §2.5 |
| S5 | Multiple independent publishable results, not one all-or-nothing claim. | Gate result (O3), calibration comparison (O4), length-residualisation audit (N4), labels dataset (N6) |
| S6 | The evaluation protocol we adopt is the strongest in the literature, and adopting it pre-empts the obvious reviewer objection. | R1's 50-split residualised protocol |
| S7 | Clean three-way work split with narrow interfaces; streams decouple after month 3. | §7.7 |
| S8 | Two explicit early go/no-go gates, at months 2 and 4. | §7.8 |

### Weaknesses

| # | Weakness | Mitigation |
|---|---|---|
| W1 | **Stage-1 sampling is the real cost** — ~10⁸ generated tokens per model on one GPU. | Scheduled first; n reducible from 8 to 4 (R3 works with 5 samples); item count reducible; vLLM batching; 1.5B model carries the primary result and larger models are a scaling ablation, not a prerequisite. |
| W2 | Not state of the art on token reduction — AdaptThink's 63.5% will likely exceed our frozen-probe result. | Never claim the leaderboard. The claim is "how much is available without touching the weights," which is a different and unanswered question. Frame R7/R8 as context, explicitly not like-for-like. |
| W3 | Label noise: Δ estimated from 8 samples is a noisy estimate of a probability difference. | Three-class formulation with a dead band instead of a hard threshold; report probe performance as a function of n; permutation test to bound chance performance. |
| W4 | Probes may not transfer across models or datasets, weakening the generality story. | Transfer is an *ablation with a reportable negative*, not a load-bearing claim. A model-specific probe is still useful — you train it once per model, cheaply, which is the whole point versus RL. |
| W5 | The effect could be small on stronger models that already overthink less. | Test on 1.5B (where R7 reports the largest headroom) first; R4's flip data suggests overthinking persists at scale. If the effect shrinks with scale, that is a reportable scaling finding. |
| W6 | Benchmark contamination is endemic in GSM8K/MATH. | Our label is a *within-item* difference between two branches of the same model on the same item, so contamination affects both branches and largely cancels. AIME 2025 included as a fresher slice. State this explicitly rather than ignoring it. |
| W7 | No patent story worth the name. | Accepted by design; this is the paper-track project, and O7 is the only IP-plausible component. |

### Opportunities

| # | Opportunity |
|---|---|
| O1 | Adaptive test-time compute is a high-traffic area with clearly identified venues (ICLR/COLM/EMNLP efficiency tracks, EfficientML-style workshops) and two 2025–2026 surveys establishing it as a recognised field. |
| O2 | The length-residualisation audit (N4) could become a widely cited methodological correction — a small paper with disproportionate influence, and cheap to produce once the harness exists. |
| O3 | The per-item marginal-utility label set (N6) is the kind of artefact other groups adopt, which is how a student paper accumulates citations. |
| O4 | Natural composition with mid-generation early exit [R12] and token-level decoupling [R14] — a follow-up paper on the combined policy with a plausible multiplicative saving. |
| O5 | Direct industrial relevance: inference cost is the dominant line item for anyone serving reasoning models, and a detachable gate is deployable in a way a retrained backbone is not. |
| O6 | The frozen-probe-versus-RL comparison (N3) speaks to an interpretability question — where the information about difficulty lives — giving the work an audience beyond efficiency. |

### Threats

| # | Threat | Response |
|---|---|---|
| T1 | **A well-resourced lab publishes this during our project year.** The area moves in months. | Our defensible ground is not the idea but the *controlled* execution: length-residualised, frozen-backbone, oracle-bounded, with the R2-style surface-feature comparison. Large-lab papers routinely omit exactly these controls. Also: submit the calibration/audit component early rather than holding everything for one big paper. |
| T2 | The internal signal turns out to be weak for the marginal-utility target even though it is strong for correctness. | This is the month-4 go/no-go. Pivot is pre-defined: revert to the correctness target (known to work, AUC 0.881) and reframe the contribution as O4 + N4 — the calibration comparison and the length-residualisation audit — which do not require the gate to succeed. |
| T3 | Pinned model versions become unavailable or benchmarks are revised. | Pin and locally archive weights, tokenizer and benchmark snapshots in month 1. Record exact commits. |
| T4 | Reviewers dismiss it as "an obvious combination of a probe and a threshold." | Pre-empt with the controls (N4, N5), the oracle ceiling (O1), and the explicit attribution argument (N3). The obviousness objection dies on the observation that nobody has reported the length-residualised number. |
| T5 | Sampling overruns and consumes the year. | Month-2 pilot on 300 items gives a hard extrapolation before committing. Fallbacks in W1 are pre-specified rather than improvised. |
| T6 | Gate overhead eats the saving on short prompts. | Measured and reported as a first-class metric (N5); the gate is one forward pass over a prompt already being processed, so the overhead is structurally small, but we will show it rather than assert it. |

**Strategic reading.** The dominant risk is T2 — whether marginal utility is as decodable as
correctness. That is precisely why the label-generation and probing stages are front-loaded, why there
are two go/no-go gates in the first four months, and why the pivot target (O4 + N4) is a paper that
stands entirely on published, already-verified signal. The project is designed so that the *uncertain*
part is tested first and the *certain* part is the fallback — which is the same principle the research
itself is about.

---

## 9. Expected Outcomes and Deliverables

1. **Primary result** — accuracy-versus-token Pareto curves for activation-gated reasoning against nine
   baselines and an oracle ceiling; target 30–50% token reduction at parity accuracy.
2. **Probe results** — AUROC/AUPRC for marginal-utility prediction, raw and length-residualised, across
   three models and four datasets, with layer and capacity ablations.
3. **Calibration finding** — internal probe versus verbalised confidence versus self-consistency, with
   R6's circuit-level account supplying the mechanism for the verbalised-confidence failure.
4. **Methodological contribution** — the length-residualisation audit of existing gating signals, and
   the introduction of gate overhead and negative-flip-rate as required reporting.
5. **Attribution finding** — how much of the RL-based adaptive-thinking gain is recoverable from a
   frozen model.
6. **Artefacts** — per-item marginal-utility labels (~4,000 items × 3 models), trained probes, extraction
   and evaluation harness, all public.
7. **Stretch** — conformal risk-controlled gate with a bounded-accuracy-loss guarantee.
8. **Demonstration** — side-by-side inference on a mixed workload: same accuracy, visibly fewer tokens,
   with the gate's decision shown per query.

---

## 10. References

**[R1]** C. Di Cicco. *Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation.* arXiv:2606.14530, June 2026 (rev. July 2026). <https://arxiv.org/abs/2606.14530>

**[R2]** Z. Zhai, B. Li, B. Xiao, M. Li and X. Wang. *Adaptive Test-Time Compute Allocation for Reasoning LLMs via Constrained Policy Optimization.* arXiv:2604.14853, April 2026. <https://arxiv.org/abs/2604.14853>

**[R3]** T. Zollo, J. Wang and R. Zemel. *Unsupervised Confidence Calibration for Reasoning LLMs from a Single Generation.* arXiv:2604.19444, April 2026. <https://arxiv.org/abs/2604.19444>

**[R4]** S. Zhou, R. Ling, J. Chen, X. Wang, T. Fan and H. Wang. *When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling.* arXiv:2604.10739, April 2026. <https://arxiv.org/abs/2604.10739>

**[R5]** M. A. Alomrani et al. *Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs.* arXiv:2507.02076, July 2025. <https://arxiv.org/abs/2507.02076>

**[R6]** *Wired for Overconfidence: A Mechanistic Perspective on Inflated Verbalized Confidence in LLMs.* COLM 2026; arXiv:2604.01457. <https://arxiv.org/abs/2604.01457>

**[R7]** J. Zhang et al. *AdaptThink: Reasoning Models Can Learn When to Think.* EMNLP 2025 (Main); arXiv:2505.13417. <https://arxiv.org/abs/2505.13417>

**[R8]** G. Fang et al. *Thinkless: LLM Learns When to Think.* arXiv:2505.13379, 2025. <https://arxiv.org/abs/2505.13379>

**[R9]** *CCPS: Calibrating LLM Confidence by Probing Perturbed Representation Stability.* arXiv:2505.21772, 2025. <https://arxiv.org/abs/2505.21772>

**[R10]** *DiffAdapt: Difficulty-Adaptive Reasoning for Large Reasoning Models.* ICLR 2026. <https://proceedings.iclr.cc/paper_files/paper/2026/file/353d4deedc4aac78b24924c485cdb4a3-Paper-Conference.pdf>

**[R11]** *Don't Overthink It: A Survey of Efficient R1-style Large Reasoning Models.* arXiv:2508.02120, August 2025. <https://arxiv.org/abs/2508.02120>

**[R12]** *Stop When Reasoning Converges: Semantic-Preserving Early Exit for Reasoning Models.* arXiv:2605.17672, 2026. <https://arxiv.org/abs/2605.17672>

**[R13]** *Calibrating LLM Judges: Linear Probes for Fast and Reliable Uncertainty Estimation.* arXiv:2512.22245, 2025. <https://arxiv.org/abs/2512.22245>

**[R14]** *ADaPT: Token-Level Decoupling for Efficient Large Reasoning Models.* arXiv:2606.19919, 2026. <https://arxiv.org/abs/2606.19919>

**Benchmarks and models.** GSM8K; MATH / MATH-500; AIME 2024 and 2025; LiveCodeBench;
DeepSeek-R1-Distill-Qwen-1.5B/7B; Qwen3-4B/8B. All versions to be pinned and archived at project start
(project Rule #1).
