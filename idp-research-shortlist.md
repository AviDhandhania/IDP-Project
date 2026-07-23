# Innovative Design Project — Research Shortlist (2025–2026)

Two deep-research sweeps. Sweep 1 = cybersecurity. Sweep 2 = all software fields.
Generated 2026-07-23. Baselines are time-sensitive — **lock the baseline version at project start**.

Jump to: [Part A — Cybersecurity](#part-a--cybersecurity) · [Part B — All software fields](#part-b--all-software-fields)

---

# Part A — Cybersecurity

---

## 🥇 #1 — Context/intent-aware malicious-package detector (supply-chain)
- **Problem:** trojaned/typosquatted packages flood PyPI/npm; scanners miss subtle ones.
- **Open gap (novelty knob):** LLMs score 0.40–0.99 F1 on binary detection but collapse to **0.48 F1** on identifying the specific malicious indicator; npm ML detectors degrade **87% → 39%** (2021–2023) as attackers drop obfuscation for minimal-footprint code.
- **Reference system:** CHASE — multi-agent LLM pipeline, **98.4% recall @ 0.08% FPR** on PyPI.
- **Datasets:** CHASE 3,000 PyPI pkgs; Mind-the-Gap 4,070 PyPI (indicator-annotated); npm 6,420 malicious + 7,288 benign; github.com/lxyeternal/pypi_malregistry
- **Beat:** the 0.48 indicator-F1 ceiling, or the concept-drift collapse.
- **Papers:** arXiv 2601.06838 (CHASE), 2602.16304 (Mind the Gap), 2603.27549 (npm benchmark)

## 🥈 #2 — Training-free prompt-injection defense for LLM agents
- **Problem:** tool-using agents hijacked by malicious text in content they read. OWASP #1 LLM risk.
- **Open gap:** attacks still hit **84.3% ASR** (ASB); defenses have limited effectiveness.
- **Reference method:** MELON — re-run trajectory with user prompt masked; flag if tool calls unchanged. **0.24% ASR** on GPT-4o. Code public.
- **Benchmarks:** AgentDojo (97 tasks, 629 attack cases), Agent Security Bench (400+ tools), InjecAgent. Metrics: Benign Utility / Utility-under-Attack / ASR.
- **Beat:** raise utility-under-attack, or generalize to harder ASB/InjecAgent attack classes.
- **Caveat:** CaMeL (arXiv 2503.18813) gives a provably-effective design-level defense — don't claim "defenses don't exist."
- **Papers:** arXiv 2502.05174 (MELON), 2406.13352 (AgentDojo), ASB (ICLR 2025)

## 🥉 #3 — Statement-level LLM vulnerability detection
- **Problem:** function-level detection ~saturated; pinpointing the vulnerable statement barely works.
- **Baseline to beat:** best model (Claude-3.7-Sonnet) only **23.83% F1** statement-level on SecVulEval.
- **Dataset:** SecVulEval — 25,440 C/C++ functions, 5,867 CVEs (1999–2024), statement-level annotated, public.
- **Beat:** retrieval-augmented / static-analysis-augmented / multi-step reasoning that lifts ~24%.
- **Papers:** arXiv 2505.19828 (SecVulEval), 2506.23644 (QLPro: CodeQL+LLM)

## #4 — On-device small-LM misinformation pipeline (low-resource language) [non-cyber]
- **Problem:** AI misinformation tools underperform in non-English low-resource languages.
- **Template:** Phi-4 (on-device-capable) best for Bangla health-claim extraction.
- **Edge:** collect a natively-sourced (not translated) dataset for your target language + report F1 vs Phi-4.
- **Caveat:** two "first Urdu fake-news benchmark" claims were REFUTED — don't build on those.
- **Papers:** arXiv 2607.12336 (Bangla SLM), 2410.18390 & 2505.00008 (surveys)

---

## Secondary tier (leads to confirm, not fully verified)
- **PQC migration tooling** — CBOM tools are "semantic-free"; production-readiness gaps (hybrid-KEM 11%, tooling 22%). Regex-based CBOM generator is a feasible starter. arXiv 2602.05759, 2606.04739, 2603.01091
- **Deepfake detection** — audio benchmarks have zero 2024–25 TTS samples (open data gap). GenD: SOTA generalization tuning 0.03% of params. arXiv 2508.06248
- **C2PA provenance** — now in Pixel 10 / Sony hardware. "Origin Lens" = on-device image-provenance verify template. contentauthenticity.org 2026, arXiv 2602.02100
- **Privacy+fairness federated learning (RESFL)** — arXiv 2503.16251

**Empty in this sweep:** general phishing detection, privacy-preserving security (beyond RESFL) — skip unless you have a dataset.

---

## Recommendation
- Most defensible paper → **#1** (best datasets, clearest gap, splits into 3 workstreams: data/benchmark · model · evaluation & drift).
- Maximum frontier "wow" → **#2**.

Raw workflow output (temp, may be deleted): `%LocalAppData%\Temp\claude\...\tasks\wyuavum7x.output`

---

# Part B — All software fields

12 verified directions; 23 papers fetched, 24/25 claims confirmed 3-0. Each has a public dataset + baseline to beat.

## Tier 1 — best baseline-to-beat stories (dev tools)
### B1 — LLM unit-test generation (top pick, cleanest paper)
- Problem: LLM tests look plausible but don't cover code / catch bugs; old benchmarks contaminated.
- Beat: ULT benchmark, 3,909 contamination-free Python tasks — SOTA only **41% acc, 30% branch cov, 40% mutation**.
- Peer-reviewed (ACM TOSEM), public GitHub. Software-only. Paper: arXiv 2508.00408

### B2 — Runtime-verified code-review benchmark (genuine open gap)
- Problem: all code-review benchmarks score with BLEU / LLM-judge; NONE builds code + runs tests.
- Build: first benchmark/tool that verifies review comments via build+test execution (bootstrap from SWE-Bench harnesses).
- Papers: arXiv 2602.13377 (survey names this gap), 2603.11078, 2509.14856

### B3 — End-to-end coding agent
- Beat: ProjDevBench (20 projects, 8 categories) — agents hit only **27.4% acceptance** (80% exec + 20% review).
- Papers: arXiv 2602.01655 + public repo

## Tier 2 — on-device / edge ML
### B4 — SLM-specific quantization
- Gap: SLMQuant (first benchmark) shows big-LLM quant methods transfer poorly to small models.
- Beat: SmoothQuant/OmniQuant/SpinQuant on 6-dataset/3-arch suite. Paper: arXiv 2511.13023

### B5 — Load-aware edge-vs-cloud inference scheduler
- Beat: Random device-selection baseline under bursty load; energy 0.07–0.16 Wh edge vs 3.96 Wh cloud. Simulation = software-only. Paper: arXiv 2505.16508

### B6 — Fully-offline first-aid RAG on a phone (great demo)
- Pocket RAG (Android, quantized Llama/Gemma/Qwen): 94.5% acc, 3.7s, offline.
- ⚠️ SQuAD/HotpotQA claim REFUTED — define your own eval. Papers: arXiv 2602.13229, 2510.27107

### B7 — NPU-accelerated RAG (strongest numbers, NEEDS hardware)
- Snapdragon X Elite NPU: 4× latency, 4–12× energy vs CPU. ⚠️ Not pure software. Paper: arXiv 2606.11257

## Tier 3 — social-good NLP (low-resource = easy novelty)
### B8 — Low-resource-language tutoring
- AFRILANGTUTOR: 10 African languages, +1.8–15.5% over base; public data (194.7K dict, 78.9K QA).
- Your edge: repeat for your target language. Paper: arXiv 2604.20996

### B9 — Agricultural vision-language assistant
- Agri-3M-VL + AgriBench-VL-4K, pairwise win-rate metric. ⚠️ Confirm dataset links live. Paper: arXiv 2510.04002

### B10 — Automated accessibility code-fixing
- FixAlly: scanner findings → source fixes, 77% plausible / 69% accepted. ⚠️ iOS/SwiftUI only — port to Android/web. Paper: arXiv 2408.03827

### B11 — Program repair for DSLs / low-resource languages
- SLMFix: small model + RL, >95% validator pass, RL beats SFT even at 7B (Ansible/Bash/SQL/YAML). Paper: arXiv 2511.19422

### B12 — NLP-for-Social-Good (umbrella)
- Mental health, fact-checking, hate speech, crisis, climate. Low-resource languages = flagged gap. Paper: arXiv 2505.22327 + LoResLM/LowResNLP 2025

## Recommendation (Part B)
- Safest publishable → B1 (ULT) or B3 (ProjDevBench): "SOTA gets X%, we get X+N%", public harness, no hardware.
- Impressive + social-good showcase → B8 (your-language tutoring) or B6 (offline first-aid RAG).
- Systems paper → B4 (SLM quantization).

Raw output (temp): `...\tasks\wps917i7i.output`
