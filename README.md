# Crypto-Agility Navigator

> **Dataflow-Aware Cryptographic Inventory and Prioritised Post-Quantum Migration**  
> *Innovative Design Project (IDP) · Academic Year 2026–2027 · Software-Only Track (Team of 3)*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standard: CycloneDX 1.6 CBOM](https://img.shields.io/badge/Standard-CycloneDX_1.6_CBOM-green.svg)](https://cyclonedx.org)
[![NIST Standards: FIPS 203/204/205](https://img.shields.io/badge/NIST-FIPS_203%20%7C%20204%20%7C%20205-blue.svg)](https://csrc.nist.gov)
[![Status: Review 1 Completed](https://img.shields.io/badge/Status-Review_1_Complete-brightgreen.svg)](#project-status--milestones)

---

## 📌 Executive Summary

Every enterprise software system depends on cryptography it cannot reliably enumerate or sequence for migration. With the finalisation of NIST post-quantum standards (FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA), **what** algorithms to migrate to is settled. The bottleneck is industrial and software-engineering: **an organisation cannot migrate what it cannot locate, and cannot sequence a multi-year migration without knowing which cryptographic call sites protect long-lived, exposed data.**

Under the **Harvest-Now-Decrypt-Later (HNDL)** threat model, passive adversaries capture ciphertext today to decrypt once a Cryptographically Relevant Quantum Computer (CRQC) emerges. By **Mosca's inequality** ($x + y > z$, where $x$ is data retention lifetime, $y$ is migration duration, and $z$ is time to CRQC), systems with long retention obligations (finance, healthcare, identity) are already in violation.

### The Critical Research Gap

Current state-of-the-art cryptographic discovery tools (Crypsy, CBOMkit, IBM Quantum Safe Explorer, SandboxAQ) output **semantically flat** inventories:
1. **Findings lack context and actionability:** Flagging every hash or cipher indiscriminately results in actionable precision around $\approx 0.30$ (over two-thirds are non-security uses like ETags, cache keys, or checksums).
2. **Findings are not ordered:** Risk scores in existing literature evaluate algorithm properties (e.g., key length, Shor-path qubit costs). Two identical `RSA.encrypt()` invocations—one wrapping a 30-year medical record stored in S3 and another wrapping an ephemeral 15-minute CSRF token—receive identical risk scores.

**Crypto-Agility Navigator** bridges this gap by binding static cryptographic invocations to the **data they protect**, inferring **data retention lifetimes** from code and declarative configuration (DDL/ORM models, cache TTLs, cloud lifecycle policies, IaC), calculating an **HNDL Exposure Score per data path**, and generating differentially verified hybrid post-quantum patches.

---

## 🏗️ System Architecture

```
                       Repository Source + Config (DDL / ORM / IaC / Cloud Policies)
                                                     │
                                                     ▼
     ┌────────────────────────────────────────────────────────────────────────────────────────┐
     │ 1. Multi-Language Cryptographic Discovery Layer                                        │
     │    • Tree-sitter AST parsing + extensible rule corpus (Semgrep / Crypistry)            │
     │    • Constant propagation & local type inference for runtime-computed arguments        │
     │    • Emits baseline CycloneDX 1.6 Cryptography Bill of Materials (CBOM)                │
     └───────────────────────────────────┬────────────────────────────────────────────────────┘
                                         │ Crypto Invocations & Assets
                                         ▼
     ┌────────────────────────────────────────────────────────────────────────────────────────┐
     │ 2. Semantic Binding & Retention Inference (Core Contribution - N1)                     │
     │    • Backward Taint Analysis: Plaintext / key parameters ➔ Data sources                │
     │    • Forward Taint Analysis: Ciphertext ➔ Sinks (network, database, object store)      │
     │    • Retention Evidence Extraction: ORM fields, Redis TTLs, S3 rules, DB migrations   │
     │    • Exposure Surface Classification: In-process < IPC < Local Host < Network / Cloud   │
     └───────────────────────────────────┬────────────────────────────────────────────────────┘
                                         │ Enriched Data Paths
                                         ▼
     ┌────────────────────────────────────────────────────────────────────────────────────────┐
     │ 3. Prioritisation & Finding Suppression Engine (N2, N3)                                │
     │    • HNDL Exposure Score: Exposure(p) = w_r·R(p) × w_e·E(p) × w_a·A(p) × w_k·K(p)      │
     │    • Context-Based Suppression: Suppresses non-security hashes & low-risk ephemera     │
     │    • Produces prioritized migration backlog ranked by risk reduction per unit effort   │
     └───────────────────────────────────┬────────────────────────────────────────────────────┘
                                         │ Prioritized Remediation Candidates
                                         ▼
     ┌────────────────────────────────────────────────────────────────────────────────────────┐
     │ 4. Hybrid Patch Synthesis & Differential Verification Gate (N4)                        │
     │    • Template-constrained liboqs hybrid constructions (e.g., X25519 + ML-KEM)          │
     │    • Three-part verification: Differential Equivalence, Property Tests, Interoperability│
     │    • Emits automated Pull Requests with enriched CycloneDX 1.6 CBOM annotations       │
     └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Objectives & Success Criteria

| Objective | Description | Target / Success Criterion |
|---|---|---|
| **O1: Multi-Language Discovery** | Extract crypto assets into standard CycloneDX 1.6 CBOM for Python and Java | Discovery $F_1 \ge 0.85$ (outperforming Crypsy 0.75 and CBOMkit 0.66) |
| **O2: Semantic Dataflow Binding** | Backward/forward taint tracing to source, sink, and retention configuration | $\ge 70\%$ call-site binding coverage; retention evidence inferred for $\ge 50\%$ |
| **O3: HNDL Exposure Scoring** | Operationalise Mosca's inequality at call-site granularity | Ranking quality $\text{nDCG@20} \ge 0.80$ and Kendall-$\tau \ge 0.6$ vs expert order |
| **O4: Noise Suppression** | Filter non-security cryptographic calls using dataflow provenance | Actionable precision increased from $\approx 0.30$ baseline to $\ge 0.70$ ($< 5$ pt recall loss) |
| **O5: Hybrid Patch Synthesis** | Generate hybrid PQC migrations (X25519 + ML-KEM) on real multi-file projects | $\ge 80\%$ pass differential testing, property tests, and downgrade-resilience gates |
| **O6: Benchmark Release** | Curate and release retention-annotated real-world benchmark with priority labels | $\ge 15$ repositories spanning finance, healthcare, identity, and messaging |
| **O7: Ranking Protocol** | Establish standardized ranking evaluation methodology for crypto migration | Methodological publication on evaluation protocols for PQC readiness tools |

---

## 🔬 Core Innovations & Novelty

- **N1: Retention-Aware Cryptographic Dataflow Binding:** First tool to bind cryptographic primitives to the confidentiality lifetime of the underlying data recovered from code and declarative infrastructure configs.
- **N2: Call-Site-Discriminating Risk Metric:** Moves past algorithm-intrinsic scores (where all RSA-2048 instances receive identical scores) to data-path-dependent HNDL scores, evaluated via ranking metrics ($\text{nDCG}$, Kendall-$\tau$, Spearman-$\rho$).
- **N3: Dataflow-Conditioned Finding Suppression:** Reclassifies non-security hashes (cache keys, checksums) without manual triage based on source/sink security relevance.
- **N4: Differentially Verified Hybrid Patch Synthesis:** Replaces unconstrained zero-shot LLM code generation with template-constrained PQC patches verified via differential equivalence, property tests, and hybrid downgrade checks.
- **N5: Public Retention-Annotated Benchmark:** First open dataset pairing real-world cryptographic call sites with retention ground-truth and expert-adjudicated migration priority orders.

---

## 📂 Repository Structure

```
.
├── .gitignore                               # Git ignore rules (Office locks, OS temp files)
├── LICENSE                                  # MIT License
├── README.md                                # Project overview and documentation (this file)
├── BACSE291_IDP_Common_Guidelines_2026-2027_Final.pdf # Course syllabus, review schedule & rubrics
├── Crypto-Agility_Navigator_Review1.pptx     # Review 1 Slide Deck (39 slides)
├── Crypto-Agility_Navigator_Review2.pptx     # Review 2 Slide Deck (36 slides)
├── Report-1-Crypto-Agility-Navigator.docx     # Review 1 Report (MS Word format, 25 pages)
├── Report-1-Crypto-Agility-Navigator.md       # Review 1 Report (Markdown source of truth)
├── Report-2-Crypto-Agility-Navigator.docx     # Review 2 Report (MS Word format, 469 paragraphs)
├── Report-2-Crypto-Agility-Navigator.md       # Review 2 Report (Markdown source of truth)
├── examples/                                # Worked benchmark test cases (S3 archive vs Redis TTL)
├── src/crypto_agility_navigator/              # Working ~20% Prototype (AST, Taint, Scorer, CBOM)
└── tests/                                   # Automated unit test suite (100% pass rate)
```

---

## 📅 Project Status & Milestones

- [x] **Review 1 — Problem Identification & Proposed Methodology (5 Marks — Completed)**
  - Problem identification, industrial & compliance urgency (RBI Q-SAFE, National CII 2027–2029, US EO 14412).
  - Comprehensive 16-paper literature survey with critical flaw analysis.
  - Architecture, mathematical scoring formulation, and 4-stage methodology defined.
  - Presentation slide deck: [`Crypto-Agility_Navigator_Review1.pptx`](Crypto-Agility_Navigator_Review1.pptx).
- [x] **Review 2 — Initial Design, Formulation & Prototype Implementation (~20% Completion / TRL 3 — 20 Marks)**
  - Comprehensive Review 2 Report ([`Report-2-Crypto-Agility-Navigator.md`](Report-2-Crypto-Agility-Navigator.md) & [`Report-2-Crypto-Agility-Navigator.docx`](Report-2-Crypto-Agility-Navigator.docx)) addressing all 7 evaluation parameters.
  - Complete 36-slide panel presentation: [`Crypto-Agility_Navigator_Review2.pptx`](Crypto-Agility_Navigator_Review2.pptx).
  - Working Stage 1–3 prototype (`src/crypto_agility_navigator/`) with AST discovery, dataflow taint tracking, retention inference, and HNDL scoring.
  - Standard-compliant CycloneDX 1.6 CBOM emission with custom dataflow properties.
  - Automated unit test suite (`tests/test_navigator.py`) passing with 100% success rate.
  - Empirical verification on worked example (`examples/sample_project`).
- [ ] **Review 3 — Progress Review (30% Completion — 10 Marks)**
- [ ] **Review 4 — Core Functionality and Integration (50% Completion — 15 Marks)**

---

## 📜 Regulatory Context & References

The project directly aligns with binding national and international transition deadlines:
- **India National Quantum-Safe Task Force:** Critical Information Infrastructure (CII) migration deadline (2027–2029).
- **Reserve Bank of India (RBI) Q-SAFE Committee:** Mandate for cryptographic inventories and crypto-agility assessments.
- **SEBI Cyber Security and Cyber Resilience Framework:** Explicit requirements addressing Harvest-Now-Decrypt-Later (HNDL) risk.
- **NIST Standards:** FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA).
- **OWASP CycloneDX 1.6:** Cryptography Bill of Materials (CBOM) specification.
- **US Executive Order 14412:** Direction on minimum elements for Cryptography Bills of Materials.

---

## 👥 Contributors

- **Avi Dhandhania** ([@AviDhandhania](https://github.com/AviDhandhania))
- *Innovative Design Project Team Members*

Licensed under the [MIT License](LICENSE).
