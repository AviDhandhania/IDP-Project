# Review Report I

## Crypto-Agility Navigator: Dataflow-Aware Cryptographic Inventory and Prioritised Post-Quantum Migration

**Innovative Design Project — Review 1 (Problem Identification and Proposed Methodology)**

**Team size:** 3 · **Duration:** one academic year · **Track:** software-only, no specialised hardware

---

## 1. Problem Identification

### 1.1 The technical problem

Every deployed software system depends on cryptography it cannot enumerate. A mid-sized banking
application will invoke RSA, ECDSA, AES and SHA-family primitives from a mixture of first-party code,
third-party libraries, container base images, TLS terminators, database configuration and
infrastructure-as-code — with no single artefact recording where those invocations are or what they
protect.

Shor's algorithm renders RSA and elliptic-curve cryptography insecure against a cryptographically
relevant quantum computer (CRQC). NIST has standardised the replacements — ML-KEM (FIPS 203),
ML-DSA (FIPS 204) and SLH-DSA (FIPS 205) — so *what* to migrate to is settled. The unsolved problem is
industrial rather than cryptographic: **an organisation cannot migrate what it cannot locate, and cannot
sequence a multi-year migration without knowing which of its thousands of cryptographic call sites are
actually dangerous.**

This is sharpened by the *harvest-now-decrypt-later* (HNDL) threat model. An adversary records
ciphertext today and decrypts it once a CRQC exists. Mosca's inequality formalises the deadline: if
*x* is the number of years data must remain confidential, *y* the years required to complete migration,
and *z* the years until a CRQC exists, then **x + y > z** means the organisation is already too late.
For sectors with 25–50 year retention obligations — health records, life insurance, legal archives,
genomic data — that inequality is already violated [P8]. Critically, HNDL exposure is a property of
*the data*, not of the algorithm: two identical `RSA.encrypt()` calls, one wrapping a 30-year medical
record for offsite archival and one wrapping a 90-second session token, carry radically different risk.
No current tool distinguishes them.

### 1.2 The specific gap in the state of the art

Cryptographic discovery tooling has matured rapidly (CBOMkit, IBM Quantum Safe Explorer, SandboxAQ
AQtive Guard, and the recent academic scanner Crypsy [P1]), and the Cryptography Bill of Materials
(CBOM) has been standardised as a CycloneDX 1.6 extension [P6]. The output of all of these is
**semantically flat**: a list of the form *"RSA-2048 appears at `payments/crypto.py:214`"*.

Two measured consequences follow, both documented in the 2026 literature:

1. **Findings are not actionable.** Näther and Hirsch report that on real deployed services their
   assessment rules fire "on all matching invocations regardless of usage context," giving a
   real-world actionable-weakness precision of "roughly 0.3" [P1]. Two out of three flagged findings
   are noise — typically non-security hashing (cache keys, ETags, checksums) matched by the same rule
   as password hashing.

2. **Findings are not ordered.** Where risk scoring exists, it is *algorithm-intrinsic*. Shaw's
   quantum-aware scorer derives a 0–10 severity from key size, Shor-path qubit cost, Grover speedup
   factor and forward-security exposure [P2] — all properties of the primitive, none of the protected
   data. Every RSA-2048 call site in a codebase therefore receives an identical score, which is exactly
   the case in which prioritisation is needed and exactly the case in which this class of score
   provides no signal.

**Problem statement.** *Given a source repository, no existing technique binds each cryptographic
operation to the data it protects, that data's confidentiality lifetime, and its exposure surface, and
therefore no existing technique can produce a defensible migration order or suppress
context-irrelevant findings. Post-quantum migration tooling reports **what** cryptography exists; the
operational question is **what to migrate first**, and it is unanswered.*

### 1.3 Preliminaries and threat model

**Cryptographic assets.** Following the CycloneDX 1.6 CBOM object model [P6], a cryptographic asset is
one of: *material* (keys, certificates, secrets), *artefacts* (protocol or file-format configuration),
or *invocations* (calls into a cryptographic API). Our analysis operates over invocations and the data
flowing through them, and consumes material and artefacts as context.

**Standardised replacements.** NIST FIPS 203 (ML-KEM, key encapsulation), FIPS 204 (ML-DSA,
lattice signatures) and FIPS 205 (SLH-DSA, hash-based signatures) are final. Deployment practice is
*hybrid* — a classical and a post-quantum primitive combined so that security holds if either survives
(X25519 + ML-KEM for key establishment being the common construction). Hybrid deployment is what we
generate, and it is the conservative choice: a defect in the PQC implementation cannot make the system
worse than it was.

**Crypto-agility.** We adopt the operational definition: the property that a cryptographic primitive can
be replaced without redesigning the system that uses it. It is a property of *architecture*, not of
algorithm choice, which is why it is measurable from code and why CARS [P5] attempts to score it.

**Threat model.** The adversary is passive and patient. They cannot break RSA or ECC today. They can
(a) record ciphertext in transit or exfiltrate encrypted data at rest, (b) store it indefinitely at
negligible cost, and (c) decrypt it once a CRQC exists. They do not need to be detected, and detection
after the fact provides no remedy — this is the property that distinguishes HNDL from every other
vulnerability class, and the reason forward secrecy cannot help retroactively [P8].

Formally, **Mosca's inequality**: for a given data path, let *x* be the required confidentiality
lifetime, *y* the time to migrate that path, and *z* the time until a CRQC exists. The path is
*already breached* when

```
x + y > z
```

Every term except *z* is a property of the specific data path, and both *x* and *y* are in principle
recoverable from code and configuration. **This is the observation the project rests on:** the
literature treats *x* as an input supplied by a human analyst, and we treat it as something to infer.

### 1.4 A worked example

Two call sites in the same repository, matched by the same discovery rule and assigned the same
algorithm-severity score by every tool surveyed:

```python
# A — payments/archive.py
record = build_settlement_record(txn)              # source: database read
blob   = rsa_oaep_encrypt(record, archive_pubkey)  # RSA-2048
s3.put_object(Bucket="settlements-archive",        # sink: object store,
              Key=k, Body=blob)                    # lifecycle: retain 10 years

# B — web/session.py
tok    = make_csrf_token()                         # source: local RNG
sealed = rsa_oaep_encrypt(tok, session_pubkey)     # RSA-2048 — identical primitive
redis.setex(k, 900, sealed)                        # sink: cache, TTL 900 s
```

Site **A** protects a financial record with a ten-year retention obligation, written to an
externally-reachable object store. Under Mosca's inequality with *x* = 10 years, it is already breached.
Site **B** protects a value that is worthless in fifteen minutes; *x* ≈ 0, so migrating it delivers no
risk reduction whatsoever.

Both sites are `RSA_OAEP` with a 2048-bit key. An algorithm-intrinsic score [P2] must rank them
identically. A pattern-matching inventory [P1] reports them identically. Yet the correct migration order
is unambiguous, and every piece of evidence needed to derive it — `s3.put_object` with a ten-year
lifecycle rule versus `setex` with a 900-second TTL, a database-derived source versus a locally
generated token — is present in the repository and machine-readable.

**That gap between "the information is in the code" and "no tool reads it" is the whole project.**

---

## 2. Justification

**2.1 The requirement is mandated and dated, not speculative.** India's national quantum-safe task
force has set a **2027–2029 migration deadline for critical information infrastructure**. The Reserve
Bank of India has constituted the **Q-SAFE committee** (chaired from IIT Madras) whose remit explicitly
includes construction of a cryptographic inventory and assessment of crypto-agility. SEBI's Cyber
Security and Cyber Resilience Framework names harvest-now-decrypt-later directly. Internationally, US
Executive Order 14412 (June 2026) directs CISA and NIST to publish minimum elements for a CBOM within
270 days. The project therefore targets a compliance artefact with a legal deadline, and its value does
not depend on any prediction about when quantum computers arrive.

**2.2 The gap between intent and execution is enormous.** A DigiCert survey (July 2026) found 87% of
organisations planning or piloting PQC but only **7%** having deployed quantum-safe cryptography across
most of their certificate estate. The bottleneck is not willingness; it is that no tool converts an
inventory into a plan.

**2.3 The gap is named by the literature itself as future work.** The primary academic scanner states
that context-insensitive rules "requir[e] manual triage to distinguish actionable from non-actionable
findings" [P1]. Zhang's ICSE'26 vision paper defines the missing agenda as exactly three pillars —
"PQC-aware detection, semantic refactoring, and hybrid verification" — and provides no implementation
[P4]. The CARS readiness framework scores an *organisation* on five dimensions but concedes that
"external predictive validation against migration outcomes remains future work" [P5]. We are therefore
building the component that three independent 2026 papers identify as absent.

**2.4 It is buildable by three students in one year.** Pure software; no dataset to collect; no GPU; no
quantum hardware. Mature reusable infrastructure exists (tree-sitter, Semgrep, CodeQL, liboqs,
CycloneDX 1.6). The evaluation targets are already-published numbers we can be measured against.

**2.5 There is a defensible intellectual property position.** Under the Indian Patent Office's CRI
Guidelines (2025), eligibility turns on demonstrable *technical effect* rather than novel hardware.
Ordering remediation by dataflow-derived data lifetime and exposure surface produces a measurable
technical effect (reduction in residual HNDL exposure per unit of engineering effort). Our prior-art
search found no claim on this combination.

---

## 3. Objectives

| # | Objective | Success criterion |
|---|-----------|-------------------|
| **O1** | Build a multi-language cryptographic discovery layer emitting CycloneDX 1.6 CBOM. | Discovery F1 ≥ 0.85 on our benchmark, versus Crypsy's reported overall 0.75 and CBOMkit's 0.66 on the Go subset [P1]. |
| **O2** | Implement inter-procedural dataflow binding: each crypto call site → the data it protects → that data's retention evidence → its exposure surface. | Successful binding for ≥ 70% of discovered call sites in Python and Java; retention evidence recovered automatically for ≥ 50%. |
| **O3** | Define and compute an **HNDL Exposure Score** per data path, operationalising Mosca's inequality at call-site granularity. | Ranking quality nDCG@20 ≥ 0.80 and Kendall-τ ≥ 0.6 against an expert-labelled priority order on held-out repositories. |
| **O4** | Suppress context-irrelevant findings using dataflow context. | Actionable-finding precision raised from the reported ≈ 0.30 [P1] to ≥ 0.70, at recall loss ≤ 5 points. |
| **O5** | Synthesise hybrid post-quantum patches (X25519 + ML-KEM) verified by differential testing before proposal. | ≥ 80% of proposed patches pass differential equivalence and the project's own test suite, on *real multi-file repositories* (where prior LLM migration work degrades from its 92.5% synthetic-single-fragment rate [P3]). |
| **O6** | Release the tool (CLI + CI action) and a public retention-annotated benchmark. | Public repository; CycloneDX 1.6 schema conformance; benchmark of ≥ 15 real repositories with expert priority labels. |

**Secondary objective (O7).** Publish the prioritisation-evaluation protocol itself. No existing paper
in this area reports a *ranking* metric; introducing nDCG/Kendall-τ against expert order as the
standard measure for migration tooling is a methodological contribution independent of our tool's
score.

---

## 4. Scope

### 4.1 In scope

- **Languages:** Python and Java as primary targets (chosen deliberately — Näther and Hirsch state
  that "ecosystems that hold much enterprise cryptography, such as Java, C/C++, and Python, are not yet
  demonstrated" [P1]); Go as a stretch target for direct comparison against published numbers.
- **Cryptography classes:** transport (TLS configuration), data-at-rest (envelope encryption, disk/DB
  encryption configuration), and application-layer cryptography (JWT signing, password hashing, token
  encryption, custom protocol code).
- **Analysis level:** source code plus adjacent declarative configuration — ORM models, database
  migrations, IaC (Terraform/Helm), object-store lifecycle policies, log-retention configuration. These
  are the machine-readable evidence of retention.
- **Outputs:** CycloneDX 1.6 CBOM enriched with dataflow and retention annotations; a ranked migration
  plan; auto-generated hybrid patches as pull requests.
- **Evaluation:** discovery accuracy, ranking quality, actionable precision, patch correctness.

### 4.2 Explicitly out of scope

- **Binary and firmware analysis.** A separate research line already addresses executables [P11]; we
  will not duplicate it.
- **HSM / PKCS#11 estate discovery and certificate-lifecycle management.** Vendor territory, and
  requires infrastructure we do not have.
- **Side-channel resistance and constant-time verification** of the PQC implementations we emit; we
  consume liboqs and inherit its properties.
- **Formal proof** of patch equivalence. We use differential testing, and will state that as a
  soundness limitation rather than claiming verification.
- **Any quantum hardware, QKD, or QRNG component.** The project's relationship to quantum computing is
  as a *threat model*, not a platform. This will be stated in the first paragraph of any publication.
- **Organisation-level maturity scoring.** CARS [P5] occupies that layer; we operate at call-site
  granularity.

### 4.3 Assumptions

Source access is available; repositories are analysable statically; retention policy is at least
partially expressed in machine-readable configuration; a domain expert (guide or industry contact) is
available for approximately 20 hours of priority labelling.

---

## 5. Preliminary Literature Survey

### 5.1 Survey method

We searched arXiv, IACR ePrint, ACM DL, IEEE Xplore and Springer for the period January 2025 – August
2026 using the query families *{crypto-agility, cryptographic inventory, CBOM, PQC migration, quantum-safe
static analysis, harvest-now-decrypt-later}*, followed by forward and backward citation chasing from the
two most recent scanner papers. Sixteen works were retained as directly load-bearing: eleven from
2025–2026, three from 2024 (a pre-standardisation binary toolchain and a systematic literature review),
and two classical baselines from 2017 and 2019 retained because every modern paper positions against
them.

### 5.2 Summary of surveyed work

| Ref | Work | Year / venue | Core contribution | Key reported numbers |
|-----|------|--------------|-------------------|----------------------|
| **P1** | Näther & Hirsch — *Hidden Ciphers and Where to Find Them* (Crypistry / Crypsy) | Aug 2026, arXiv 2608.04857 | Rule repository (214 rules) + static scanner + CBOM export; three discovery and two assessment categories | Benchmark F1 0.75 (P 0.87 / R 0.66); Go invocations F1 0.92; vs CBOMkit 0.66; 370 components over 57,610 files in < 6 min; **real-world actionable precision ≈ 0.3** |
| **P2** | Shaw — *Quantum-Safe Code Auditing* | Apr 2026, arXiv 2604.00560 | Regex detection of 15 vulnerable algorithm classes → LLM enrichment → VQE-based quantum-aware threat score (0–10) | P 71.98% / R 100% / F1 83.71% on a **stratified 602 of 5,775** findings (10.4% labelled) |
| **P3** | Pallarés de Bonrostro et al. — *Empirical Evaluation of LLMs for Migration of Code Fragments to PQC* | Jun 2026, arXiv 2606.07341 | 800 paired executable Python fragments across six crypto families; fine-tuning study | Fine-tuned GPT-4.1-mini: static similarity 0.9072, **functional correctness 92.5%**; GPT-4.1 zero-shot **15%** |
| **P4** | Zhang — *Toward Quantum-Safe Software Engineering* (AQuA vision) | ICSE'26 poster, arXiv 2602.05759 | Positions PQC migration as a distinct SE problem; three-pillar agenda: PQC-aware detection, semantic refactoring, hybrid verification | Two-page vision; no implementation or evaluation |
| **P5** | Costa — *Crypto-Agility Readiness Score (CARS)* | Jul 2026, IACR ePrint 2026/1467 | Five-dimension weighted readiness index (inventory completeness, algorithm compliance, architectural decoupling, toolchain readiness, governance); Delphi-derived weights | 43 OSS repositories in 5 categories; mean scores 24.9–47.5; weights from 12 senior engineers |
| **P6** | IBM Research — *The Anatomy of Cryptography Bills of Materials* | Eurocrypt 2026 | Object model for cryptographic assets, dependency relationships and evidence capture in CycloneDX | Standardisation reference — defines the schema we must emit |
| **P7** | *Towards Cryptography Bill of Materials Compliance* | 2026, Springer LNCS | Policy-driven engine classifying CBOM assets against customisable machine-readable rules | Prototype; policy layer above an existing CBOM |
| **P8** | *On the Practical Feasibility of Harvest-Now, Decrypt-Later Attacks* | 2026, arXiv 2603.01091 | Feasibility and economics of HNDL; prioritisation by sensitivity decay | Healthcare retention 25–50 yr → Mosca deadline already passed; forward secrecy cannot retroactively protect captured traffic |
| **P9** | *Post-Quantum Cryptography and Quantum-Safe Security: A Comprehensive Survey* | Oct 2025, rev. Jun 2026, arXiv 2510.10436 | Consolidated survey post-FIPS 203/204/205; crypto-agility and hybrid migration as organising themes | Survey; establishes standard-selection consensus |
| **P10** | *Securing Cryptography in the Age of Quantum Computing and AI* | Mar 2026, arXiv 2603.06969 | Threat landscape, implementation status and strategic response synthesis | Positioning / roadmap |
| **P11** | *A Toolchain for Assisting Migration of Software Executables Towards PQC* | 2024, arXiv 2409.07852 | Binary-level detection and migration assistance for compiled artefacts | Pre-standardisation; complementary analysis level |
| **P12** | *The Cost of Waiting: Decision-Theoretic Synthesis of Early vs Late PQC Migration Under Uncertainty* | 2026, Frontiers Quantum Sci. Tech. | Decision-theoretic treatment of migration timing under CRQC-date uncertainty | Provides the utility model our score can be justified against |
| **P13** | Rahaman et al. — *CryptoGuard* | CCS 2019 | Backward dataflow analysis detecting 22 classes of classical cryptographic API misuse in Java | The classical baseline; **proves inter-procedural crypto dataflow at scale is tractable** |
| **P14** | Näther et al. — *Migrating Software Systems towards Post-Quantum Cryptography: A Systematic Literature Review* | 2024, arXiv 2404.12854 | SLR extracting four migration phases, substeps and emerging role archetypes | Names three adopter obstacles: missing PQC experience and high realisation effort, security concerns about the new system, high complexity; finds terminology and steps "not defined precisely or consistently" and implementations "mostly experimental," yielding an "overall chaotic situation" |
| **P15** | *Harvest Now, Decrypt Later: Examining Post-Quantum Risk* | 2025, Federal Reserve FEDS working paper series | Economic and financial-stability framing of HNDL exposure | Establishes HNDL as a supervisory concern for the financial sector independent of any CRQC date estimate |
| **P16** | Krüger et al. — *CogniCrypt* | ASE 2017 | Developer-facing generation of correct cryptographic code plus misuse analysis | The "help the developer write it correctly" line of work; 2026 evidence reports general-purpose LLMs now exceeding CogniCrypt, CryptoGuard and Snyk Code on misuse precision and recall |

### 5.3 Critical analysis: what each work gets wrong, and our correction

This is the core of the review. For each work we state the flaw *in its own terms* — from stated
limitations, from methodology, or from what its evaluation omits — and the corresponding correction in
our design.

**P1 — Crypsy (the strongest and closest baseline).**
*Flaw 1 (context-blindness, admitted).* Assessment rules "fire on all matching invocations regardless
of usage context." The consequence is quantified by the authors themselves: real-world actionable
precision ≈ 0.3. A rule for weak password hashing cannot tell a password from a cache key because the
rule sees only the call, not the value flowing into it.
*Flaw 2 (no dataflow).* Confirmed absent. The tool is a pattern matcher with an excellent rule corpus;
there is no notion of what data a primitive protects.
*Flaw 3 (no prioritisation).* 370 components and 52 migration candidates are reported as a *set*, not
an order. The output does not answer the operator's actual question.
*Flaw 4 (recall asymmetry).* Precision 0.87 against recall 0.66 — a third of ground-truth assets are
missed, and the authors note that arguments "computed at runtime" cannot be resolved.
*Flaw 5 (coverage).* Java, C/C++ and Python "not yet demonstrated" — the ecosystems that matter.
**Our correction.** We treat Crypsy's rule corpus as the *input* to our contribution rather than a
competitor: reuse the discovery layer, add the semantic layer above it. Dataflow context directly
attacks Flaw 1 (a value that reaches `bcrypt` from an HTTP form field is a password; one that reaches
`sha256` from a file handle and terminates in a cache key is not), Flaw 2 by construction, and Flaw 3 by
producing a ranked plan. We address Flaw 4 partially with constant propagation and type inference to
resolve some runtime-computed algorithm identifiers, and will report honestly on the residual. Flaw 5 is
our scope choice (O1).

**P2 — Quantum-Safe Code Auditing (closest prior art on scoring).**
*Flaw 1 (the score cannot discriminate).* The VQE threat score is a function of algorithm properties
only — key size, Shor-path qubit cost, Grover factor, forward-security exposure. Every RSA-2048 site in
a repository receives the same score. A prioritisation signal that is constant across the set it is
meant to order carries no information about that set.
*Flaw 2 (quantum machinery is decorative).* A parameterised two-qubit circuit minimising a diagonal
Hamiltonian whose coefficients are published qubit-cost estimates is a weighted sum computed
expensively. The authors concede the outputs "are not forecasts of actual qubit requirements."
*Flaw 3 (evaluation ceiling).* Metrics come from a stratified 10.4% sample, with the authors
acknowledging that extrapolation "assumes the unlabelled 89.6% has similar label distribution — a
reasonable but unverified assumption." Recall of 100% on such a sample also indicates a detection task
made easy by construction.
*Flaw 4 (no baseline comparison).* Comparison against CryptoGuard, Bandit and SonarQube is listed as
*future work*, so the 71.98% precision figure is unanchored.
**Our correction.** Our score is a function of the *protected data path* — retention lifetime × exposure
surface × algorithm class × key reuse — so it varies across identical algorithms and orders them. We
justify it against a decision-theoretic utility model [P12] and Mosca's inequality [P8] rather than a
quantum circuit, and we state plainly that no quantum computation is involved. We evaluate on a fully
labelled benchmark, report ranking quality (which P2 never measures), and run the baseline comparisons
P2 defers.

**P3 — LLM migration of code fragments.**
*Flaw 1 (synthetic single-fragment setting).* 800 *paired* fragments constructed synthetically. The
authors state real-world validation "showed degraded performance" and that "complex multi-file
dependencies remain problematic." The 92.5% headline therefore describes the easiest possible instance
of the task.
*Flaw 2 (verification is round-trip testing, not equivalence).* Correctness was judged by functional
tests — encrypt/decrypt round-trips, signature verification, KEM encapsulation cycles. A round-trip
passes even if the patch silently weakens parameters, changes key derivation, or breaks interoperability
with an unmigrated peer.
*Flaw 3 (no discovery step).* The task assumes the fragment to migrate has already been identified and
isolated — precisely the step that is hard in a real repository.
*Flaw 4 (Python only, and closed models).* Reproducibility is bounded by proprietary API versions.
**Our correction.** Patch synthesis is the *last* stage of our pipeline, applied to sites our own
analysis located, in real multi-file repositories, and verified by **differential testing against the
unmigrated implementation** plus property-based tests plus an interoperability check with a
non-migrated peer under hybrid negotiation. We will report the honest degradation from 92.5% and treat
the gap between synthetic and real as a finding.

**P4 — AQuA vision paper.**
*Flaw:* it is a two-page agenda. It correctly names detection, semantic refactoring and hybrid
verification as the three missing pillars, and implements none of them; its critique of existing tools
(not designed for "PQC's probabilistic behavior, side-channel sensitivity, and complex performance
trade-offs") is asserted rather than measured.
**Our correction.** We implement and measure two of the three pillars (semantic refactoring, hybrid
verification) and cite this paper as independent third-party confirmation that the gap we target is the
recognised one. We do not adopt its side-channel claim, since we do not evaluate side channels.

**P5 — CARS.**
*Flaw 1 (wrong granularity).* Scores an organisation or repository on five dimensions. An engineer with
a sprint to plan cannot act on the number 31.4.
*Flaw 2 (subjective weights).* Weights derive from a 12-expert Delphi process — defensible but not
grounded in outcomes.
*Flaw 3 (unvalidated, admitted).* "External predictive validation against migration outcomes remains
future work." The index has never been shown to predict anything.
**Our correction.** We score *data paths*, not organisations, so each score names an actionable unit of
work. Validation is against an expert-elicited priority *ordering* on held-out repositories (a
measurable target) rather than against expert-assigned weights, which avoids validating the model on the
same opinions that built it.

**P6, P7 — CBOM standardisation and compliance policy.**
*Flaw:* both operate strictly above the inventory. P6 defines the schema and the evidence model; P7 adds
a policy engine classifying assets against machine-readable rules. Neither generates the semantic
content their layers would need — a policy engine reasoning over a semantically flat CBOM inherits its
blindness, and can express "RSA is non-compliant" but not "this RSA use is urgent."
**Our correction.** We treat P6 as an output contract (strict CycloneDX 1.6 conformance, so our
annotations ride in a standard artefact and any P7-style engine can consume them) and design our
retention/exposure annotations as an *extension* to it, which is also the cleanest route to adoption.

**P8, P12 — HNDL feasibility and migration-timing decision theory.**
*Flaw:* both reason at the level of the organisation or the data class. They establish that
prioritisation *should* be driven by sensitivity lifetime — P8 contrasts state secrets and genome
records against session cookies and ephemeral messaging — but provide no mechanism for determining
which class a given call site belongs to. The mapping from a line of code to a retention class is left
to a human.
**Our correction.** This is precisely the mechanism we build. Our contribution can be read as the
missing automation layer beneath P8's prioritisation argument, with the retention variable *x* in
Mosca's inequality recovered from code and configuration rather than assumed.

**P9, P10 — surveys.**
*Flaw:* by construction they describe rather than measure, and both organise around "crypto-agility"
without an operational definition that can be computed from an artefact.
**Our correction.** We supply one computable definition (the per-data-path exposure score) and evaluate
it. We use the surveys only to fix the standards baseline (ML-KEM/ML-DSA/SLH-DSA, hybrid deployment)
and avoid citing them as evidence of a gap.

**P11 — binary-level toolchain.**
*Flaw:* predates FIPS 203/204/205 finalisation, so its target algorithm set is stale, and binary
analysis loses the variable names, type information and configuration context that make retention
inference possible.
**Our correction.** Source-level scope, stated as a deliberate trade-off: we accept that we cannot see
into vendored binaries, and gain the semantic information needed for the contribution.

**P13 — CryptoGuard.**
*Flaw:* targets *incorrect* API usage (ECB mode, hardcoded keys, short keys) rather than
quantum-vulnerable-but-correct usage. It has no notion of quantum threat, no scoring, and is Java-only.
Notably, P3-adjacent 2026 work reports that general-purpose LLMs now exceed CryptoGuard and CogniCrypt
on precision and recall for misuse detection.
**Our correction.** We borrow its *technique* — backward inter-procedural dataflow from crypto call
sites — and repoint it at a different question. CryptoGuard asks "is this call wrong?"; we ask "what
does this call protect, and for how long?" Its existence is also our strongest feasibility argument:
scalable crypto-focused dataflow analysis was demonstrated in 2019, so the engineering risk in our core
mechanism is bounded.

**P14 — the systematic literature review, and a revealing authorship overlap.**
*Flaw 1 (the field has no shared vocabulary, by the review's own finding).* Terminology, migration steps
and roles are "not defined precisely or consistently across the literature," implementations are
"mostly experimental," and the situation is characterised as "chaotic." A review that concludes the
field lacks agreed definitions cannot itself supply a measurable target.
*Flaw 2 (phases without mechanisms).* Four migration phases and substeps are identified descriptively.
The review says *that* inventory and prioritisation are phases; it does not say how either is performed.
*Flaw 3 (pre-standardisation).* Published April 2024, before FIPS 203/204/205 finalisation, so its
treatment of algorithm selection is dated.
**The authorship point, which strengthens our case considerably.** The first author of this 2024 review
is also the first author of Crypsy [P1], the strongest 2026 scanner. The same group therefore (i)
surveyed the field and named its obstacles, then (ii) built a tool addressing discovery — and their own
2026 evaluation still reports actionable precision ≈ 0.3 with no dataflow and no prioritisation. The gap
we target has survived a dedicated review *and* a dedicated implementation by the people best placed to
close it. That is strong evidence the gap is real and non-trivial rather than merely unattempted.
**Our correction.** We supply exactly the missing mechanism for the prioritisation phase P14 names, and
we commit to one precise, computable definition (the per-data-path exposure score) rather than adding
another informal one to a field the review already calls chaotic.

**P15 — Federal Reserve HNDL analysis.**
*Flaw:* it operates at the level of the financial system, establishing HNDL as a supervisory and
financial-stability concern. It has no view of any individual system, and its unit of analysis is an
institution, so it cannot inform an engineering decision.
**Our correction.** We cite it strictly as institutional justification for §2.1 — evidence that a
central bank treats this exposure as material — and not as technical support. Our contribution is the
layer that converts an institution-level concern into a ranked engineering backlog.

**P16 — CogniCrypt.**
*Flaw 1 (wrong direction).* It helps a developer write *new* cryptographic code correctly. The
post-quantum problem is overwhelmingly about code that already exists, was written correctly by the
standards of its time, and is now obsolete for a reason unrelated to correctness.
*Flaw 2 (superseded on its own task).* 2026 evidence reports general-purpose LLMs exceeding CogniCrypt,
CryptoGuard and Snyk Code on misuse detection precision and recall, so the rule-based misuse-detection
approach is no longer the frontier even for its original purpose.
**Our correction.** We treat correct-but-obsolete usage as the target class — the case all misuse
tooling is designed to ignore — and we use an LLM only inside a template-constrained, differentially
verified patch step (§7.5), which takes the demonstrated LLM strength (code adaptation) without
inheriting its unreliability on cryptographic content.

### 5.4 Consolidated research gap

| Capability | P1 | P2 | P3 | P5 | P6/P7 | P8/P12 | P13 | **Ours** |
|---|---|---|---|---|---|---|---|---|
| Multi-language discovery | ✔ | ◐ | ✘ | ◐ | ✘ | ✘ | ◐ | ✔ |
| Standard CBOM output | ✔ | ✘ | ✘ | ✘ | ✔ | ✘ | ✘ | ✔ |
| Dataflow to protected data | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | ◐ | **✔** |
| Retention lifetime inference | ✘ | ✘ | ✘ | ✘ | ✘ | manual | ✘ | **✔** |
| Call-site-varying risk score | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | **✔** |
| Ranking evaluated as a metric | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ | **✔** |
| Context-based FP suppression | ✘ | ◐ | ✘ | ✘ | ◐ | ✘ | ✘ | **✔** |
| Verified migration patches | ✘ | ✘ | ◐ | ✘ | ✘ | ✘ | ✘ | **✔** |

*(✔ present · ◐ partial · ✘ absent)*

The empty rows are the project.

---

## 6. Novelty of the Proposed Work

**N1 — Retention-aware cryptographic dataflow binding.** We bind each cryptographic operation to a
triple: the data it protects (recovered by backward taint analysis from the primitive's plaintext
argument to its sources), that data's confidentiality lifetime (recovered by forward analysis to
persistence sinks and then from declarative retention evidence — ORM/DDL definitions, TTL constants,
object-store lifecycle rules, log-rotation policy, IaC), and its exposure surface (whether the resulting
ciphertext crosses a process, host or network boundary). No surveyed work performs this binding; P1 and
P2 confirm dataflow is absent from the current generation of tools, and P8's prioritisation argument
assumes a human supplies exactly this information.

**N2 — A risk score that varies across identical algorithms, and a metric that can evaluate it.** By
making the score a function of the data path rather than the primitive, two identical `RSA.encrypt()`
sites receive different ranks. Correspondingly we introduce *ranking quality against expert order*
(nDCG@k, Kendall-τ) as the evaluation metric. This is doubly novel: no surveyed work produces an
ordering, and none evaluates one — P2 reports detection F1 for a tool whose stated purpose is
prioritisation.

**N3 — Dataflow-conditioned finding suppression.** Turning the semantic layer inward, the same context
that ranks findings also filters them: a hash whose input never derives from a credential source and
whose output never reaches an authentication or storage sink is reclassified as non-security. This
targets the specific, quantified failure P1 reports (actionable precision ≈ 0.3) with a mechanism P1
lacks, and we report it as a precision/recall trade-off curve rather than a single number.

**N4 — Differentially verified hybrid patch synthesis in realistic settings.** Patches are proposed only
after passing differential equivalence against the original implementation, property-based tests, and a
hybrid-negotiation interoperability check against an unmigrated peer. This directly strengthens P3's
round-trip-only verification and moves the setting from synthetic isolated fragments to real multi-file
repositories, where P3 states its own method degrades.

**N5 — A public retention-annotated benchmark with expert priority labels.** The reason no prior work
reports ranking quality is that no dataset supports it. Producing one is a reusable contribution
independent of whether our score wins.

**Patentability note.** Under CRI Guidelines 2025 the claimable subject matter is the *mechanism*: a
method for ordering cryptographic remediation in which the ordering is derived from
statically-inferred protected-data lifetime and exposure surface. The technical effect is measurable —
reduction in residual HNDL exposure per unit of remediation effort, relative to algorithm-severity
ordering. Under Rule #2 of this project, the provisional application is filed **before** any
publication or preprint, since a pre-filing disclosure destroys novelty in India.

---

## 7. Proposed Methodology

### 7.1 Architecture

```
   repository + config
            │
   ┌────────▼─────────┐
   │ 1. Discovery     │  tree-sitter parse · Semgrep/Crypistry-style rules
   │                  │  → crypto asset candidates (CycloneDX 1.6)
   └────────┬─────────┘
   ┌────────▼─────────┐
   │ 2. Semantic bind │  backward taint: primitive ← plaintext ← source
   │    (core, N1)    │  forward taint: ciphertext → persistence / network sink
   │                  │  retention evidence extraction from DDL/ORM/IaC/TTL
   └────────┬─────────┘
   ┌────────▼─────────┐
   │ 3. Score & rank  │  HNDL Exposure Score per data path (N2)
   │    + suppress    │  context-based reclassification (N3)
   └────────┬─────────┘
   ┌────────▼─────────┐
   │ 4. Patch + verify│  liboqs hybrid X25519+ML-KEM · differential testing (N4)
   └────────┬─────────┘
            ▼
   enriched CBOM · ranked migration plan · verified pull requests
```

### 7.2 Stage 1 — Discovery

Per-language tree-sitter grammars produce ASTs; a rule corpus (extending open Semgrep and
Crypistry-style rules, with attribution) identifies cryptographic material, artefacts and invocations.
Constant propagation and local type inference resolve algorithm identifiers passed as variables —
directly targeting P1's stated inability to "resolve arguments computed at runtime." Output conforms to
the CycloneDX 1.6 CBOM object model [P6].

### 7.3 Stage 2 — Semantic binding *(the contribution)*

Built on an inter-procedural dataflow framework (CodeQL for Java, a custom pass plus type stubs for
Python; the technique follows CryptoGuard's backward-analysis design [P13]).

- **Backward pass.** From each primitive's plaintext/key parameter, trace to sources. Sources are
  classified: request parameter, form field, file read, database read, environment/secret store,
  computed digest, constant.
- **Forward pass.** From the primitive's output, trace to sinks: network write, filesystem write,
  database column, object store, log, in-memory cache, response body.
- **Retention evidence extraction.** For each persistence sink, resolve retention from the nearest
  machine-readable declaration: column type and adjacent `*_at`/`expires` fields, migration files,
  Redis/Memcached TTLs, S3/GCS lifecycle rules, Kubernetes/Terraform retention settings, log-rotation
  config, and named constants matching retention idioms. Unresolved sinks fall back to a conservative
  class prior derived from the sink type, and are flagged as inferred rather than observed — the
  provenance distinction matters for the ranking evaluation.
- **Exposure classification.** Ciphertext crossing a network boundary > crossing a host boundary >
  crossing a process boundary > remaining in-process.

**Realism control.** We expect substantial unresolved binding, particularly in dynamically typed
Python. Target coverage is 70% (O2), not 100%, and unresolved sites are reported in an explicit
"insufficient context" bucket rather than silently defaulted. A tool that admits what it cannot see is
usable; one that guesses silently is not.

### 7.4 Stage 3 — HNDL Exposure Score and ranking

For each data path *p*:

```
Exposure(p) = w_r · R(p) × w_e · E(p) × w_a · A(p) × w_k · K(p)
```

where *R* is normalised retention lifetime (from Stage 2, with observed evidence weighted above
inferred), *E* exposure surface, *A* algorithm quantum-vulnerability class (Shor-broken ≫
Grover-weakened; here we reuse the published qubit-cost reasoning that P2 encodes, without the quantum
circuit), and *K* a key-reuse/blast-radius factor (how many paths share the key material — recoverable
because Stage 2 already tracks key provenance).

The functional form is justified against Mosca's inequality [P8]: a path is *already breached* when
retention + expected migration time exceeds the CRQC horizon, and the score orders paths by how far
past that threshold they sit. Weights are calibrated on a training split of expert labels — deliberately
unlike CARS' Delphi elicitation [P5], because we want weights fitted to a target we can then measure
on held-out data. Sensitivity analysis over *w* is reported; if ranking quality is insensitive to the
weights, that is itself a useful finding.

Ties are broken by remediation cost estimate (number of call sites sharing the fix), yielding a plan
ordered by risk reduction per unit of effort rather than risk alone.

**Suppression (N3).** A finding is reclassified non-security when neither its sources nor its sinks are
security-relevant. Reported as a curve over the suppression threshold, so a security team can choose
its own operating point.

### 7.5 Stage 4 — Patch synthesis and differential verification

Templates per migration class (TLS configuration, KEM handshake, signature scheme, envelope encryption)
instantiated with liboqs hybrid constructions (X25519 + ML-KEM for key establishment; ML-DSA for
signatures with size implications reported). An LLM is used only for *localisation and adaptation* to
the surrounding code, with the template constraining the cryptographic content — the inverse of P3's
setup, in which the model chooses the cryptography.

Verification gate, all three required before a patch is proposed:
1. **Differential equivalence** — original and patched implementations exercised on the same inputs;
   observable behaviour (plaintext recovered, signature validity, error classes) must match.
2. **Property tests** — round-trip, tamper-detection, wrong-key rejection, parameter-downgrade
   detection. Explicitly including the checks a round-trip test alone cannot catch (P3, Flaw 2).
3. **Interoperability** — the patched peer must negotiate successfully with an unmigrated peer under
   hybrid mode, and must *fail closed* against a downgrade attempt.

### 7.6 Evaluation plan

| Research question | Metric | Baseline / target |
|---|---|---|
| Do we discover cryptographic assets as well as the state of the art? | Precision / recall / F1 on our labelled benchmark | Crypsy 0.75 overall, 0.92 Go [P1]; CBOMkit 0.66; target ≥ 0.85 |
| Does the semantic layer make findings actionable? | Actionable-finding precision | ≈ 0.30 reported [P1]; target ≥ 0.70 at ≤ 5 pt recall loss |
| Does the score order call sites correctly? | nDCG@10/@20, Kendall-τ, Spearman ρ vs expert order | Algorithm-severity ordering [P2]; random ordering; CVSS-style ordering. Target nDCG@20 ≥ 0.80 |
| Is retention inference reliable? | Coverage; accuracy against manual annotation | ≥ 70% coverage, ≥ 80% accuracy on covered sites |
| Are patches correct? | Differential + property + interop pass rate | P3's 92.5% synthetic single-fragment rate as reference upper bound; target ≥ 80% on real repositories |
| Does it scale? | Wall-clock on a 50k-file repository | Crypsy: 57,610 files in < 6 min [P1] |

**Benchmark construction.** 15–20 real open-source repositories (payments, healthcare, identity,
messaging domains, chosen for genuine retention diversity), each annotated for (a) ground-truth crypto
assets, (b) protected-data class and retention, (c) an expert priority ordering of the top 20 findings.
Two annotators plus adjudication; inter-annotator agreement reported (Krippendorff's α). This artefact
is O6 and answers the question no prior paper can.

### 7.7 Tooling and work split

Python + tree-sitter, Semgrep, CodeQL, liboqs / liboqs-python, CycloneDX 1.6 libraries, GitHub Actions.
No GPU, no quantum hardware, no paid API required for the core pipeline.

Three-way split: **(A)** discovery layer + rule corpus + CBOM conformance; **(B)** dataflow and
retention inference (the deepest component); **(C)** scoring, ranking evaluation, benchmark
construction and patch verification harness. Each part is independently reportable if another slips.

### 7.8 Indicative timeline

| Months | Milestone |
|---|---|
| 1–2 | Literature lock; benchmark repository selection; annotation protocol; discovery layer for Python |
| 3–4 | Java discovery; CycloneDX 1.6 conformance; **baseline replication** of Crypsy/CBOMkit numbers on our benchmark |
| 5–7 | Dataflow binding + retention inference; annotation of the benchmark (expert labelling) |
| 8 | Scoring, ranking evaluation, suppression curves — **primary result** |
| 9 | Patch synthesis + verification gate |
| 10 | **Provisional patent filing** (before any disclosure) |
| 11–12 | Ablations, scale tests, paper, artefact release, demonstration |

Month 8 is the gate: if ranking quality is achieved, the paper exists. Everything after is
strengthening.

### 7.9 Metric definitions

Stated precisely, because the ranking metrics are the ones no prior paper in this area reports and are
therefore the ones a reviewer will scrutinise.

**Discovery accuracy.** Standard precision, recall and F1 over ground-truth cryptographic assets, matched
by (file, line, algorithm) triple. Reported per language and per asset category, so our numbers are
directly comparable to the per-category breakdown in [P1].

**Actionable-finding precision.** Of findings the tool presents as requiring action, the fraction an
expert annotator agrees require action. This is the metric on which [P1] reports ≈ 0.3, and matching its
definition exactly is required for the comparison to be meaningful.

**Ranking quality.** With expert relevance grades *relᵢ* over the top-*k* findings,

```
DCG@k = Σᵢ₌₁..k  relᵢ / log₂(i + 1)          nDCG@k = DCG@k / IDCG@k
```

reported at k = 10 and k = 20. Complemented by Kendall's τ and Spearman's ρ against the full expert
ordering, since nDCG rewards getting the head of the list right while τ measures agreement throughout —
and an operator works down the list, so both matter.

**Retention inference.** Coverage (fraction of persistence sinks for which a retention value was
resolved) reported separately from accuracy (fraction of resolved values within one retention class of
the annotated truth). Separating them is deliberate: a tool that resolves 40% of sinks accurately is
more useful than one that resolves 90% badly, and a single blended number would hide the difference.

**Patch correctness.** Fraction of proposed patches passing all three verification gates (§7.5),
reported per migration class, with failures categorised by cause.

**Annotation reliability.** Krippendorff's α for the asset labels and for the priority orderings, so the
subjectivity of the ranking target is quantified rather than assumed away.

### 7.10 Risk register

| # | Risk | Trigger / early indicator | Response | Checkpoint |
|---|---|---|---|---|
| RR1 | Dataflow coverage too low to support scoring | < 40% of call sites bound on the first three repositories | Fall back to analyst-supplied retention per *data class*, propagated through the dataflow graph — automates the propagation, drops the inference. N1–N3 survive. | Month 5 |
| RR2 | Retention evidence absent from real repositories | Fewer than half of persistence sinks have any machine-readable retention signal | Extend evidence sources to code comments and commit messages via an LLM extractor, reported separately as *inferred* provenance | Month 5 |
| RR3 | Expert annotator unavailable | No confirmed labeller by month 4 | Two-team-member rubric-driven ordering plus guide adjudication; report α and state the weaker authority | Month 4 |
| RR4 | Baseline replication fails (cannot reproduce [P1]/CBOMkit numbers) | Month 4 replication off by > 10 points | Report on our benchmark only, with the discrepancy documented; do not claim comparability we cannot support | Month 4 |
| RR5 | Patch synthesis unreliable | < 50% passing the verification gate | Ship as a *diagnostic-only* tool; N1–N3 stand alone and the patch stage becomes future work | Month 9 |
| RR6 | Competing product release | Vendor announcement of dataflow prioritisation | File provisional immediately; pivot the paper's framing to the open, evaluated, benchmarked comparison — which a product release does not provide | Continuous |
| RR7 | Schema churn | CISA/NIST minimum-elements publication | Adapter layer already isolates emission; re-map fields only | Continuous |

### 7.11 Ethics and responsible disclosure

The tool analyses real open-source repositories and produces findings that, in the aggregate, describe
exploitable weakness in deployed software. Three commitments follow. **(a)** Genuine
present-day vulnerabilities discovered incidentally (CVE-linked dependencies, hardcoded keys) are
reported privately to maintainers before any publication, on a 90-day disclosure clock. **(b)** The
published benchmark reports assets and priority orderings at pinned commits, and does not include
credentials or exploit paths. **(c)** Quantum-vulnerable-but-currently-secure findings — the project's
actual subject — are not treated as vulnerabilities requiring embargo, and this distinction is stated
explicitly in the artefact so the benchmark is not misread as a list of live weaknesses.

---

## 8. SWOT Analysis

### Strengths

| # | Strength | Evidence |
|---|---|---|
| S1 | Demand is regulator-mandated with a fixed date, not speculative. | RBI Q-SAFE; national CII deadline 2027–2029; SEBI CSCRF; US EO 14412 |
| S2 | The gap is independently confirmed as future work by three separate 2026 papers. | [P1] admits manual triage; [P4] names the missing pillars; [P5] admits no predictive validation |
| S3 | Published numbers exist to be measured against — no need to invent a success criterion. | 0.75 F1, ≈0.3 actionable precision, 0.66 CBOMkit, 92.5% patch correctness |
| S4 | Zero hardware cost, zero data collection, no GPU, no vendor dependency. | Pure static analysis |
| S5 | Core technique is proven tractable at scale since 2019. | CryptoGuard [P13] |
| S6 | Clean three-way decomposition; every layer is independently publishable. | §7.7 |
| S7 | Genuine patent position with a measurable technical effect. | §6, CRI Guidelines 2025 |
| S8 | Demonstration is concrete and short: point the tool at a real repository, get a ranked plan and an opened pull request. | — |

### Weaknesses

| # | Weakness | Mitigation |
|---|---|---|
| W1 | Inter-procedural dataflow in dynamically typed Python is genuinely hard; P1 concedes even literal resolution fails for runtime-computed arguments. | Target 70% coverage, not 100%; explicit "insufficient context" bucket; Java (statically typed, CodeQL-supported) as the primary demonstration language. |
| W2 | Retention ground truth requires human annotation; no public dataset exists. | Annotation is scoped to top-20 findings per repository (~300–400 labels), two annotators, agreement reported. Building the benchmark is reframed as contribution O6. |
| W3 | Expert priority labels are subjective; the ranking target is partly opinion. | Report inter-annotator agreement; use *ordering* not absolute scores; hold out repositories; report sensitivity to weights. |
| W4 | The team has no prior static-analysis or compiler experience. | Build on CodeQL and Semgrep rather than a bespoke IR; month 3–4 baseline replication acts as an early competence check with a fallback (drop to intra-procedural + configuration-level binding, which still exceeds all baselines). |
| W5 | Differential testing is unsound — it can miss inequivalence. | Stated as a limitation, not hidden; property tests target the specific classes round-trip testing misses. |
| W6 | We cannot see into vendored binaries or closed dependencies. | Declared out of scope with the complementary line of work cited [P11]. |

### Opportunities

| # | Opportunity |
|---|---|
| O1 | CISA/NIST CBOM minimum elements (due under EO 14412) will define a schema target; conforming early positions the tool as reference-compatible. |
| O2 | A policy-engine layer already exists above the CBOM [P7] and a standardised object model below it [P6] — our semantic annotations slot into an established stack rather than competing with it. |
| O3 | The retention-annotated benchmark is likely to be reused, which is how a student artefact acquires citations. |
| O4 | Direct route to industry engagement: an Indian bank or CII operator under the 2027–2029 deadline is a willing pilot partner and a strong letter of support. |
| O5 | The ranking-evaluation protocol (O7) can be published as a short methodological paper even if the tool underperforms. |
| O6 | Natural extensions: archival re-timestamping, certificate-estate ranking, extension to Go/C++ — a follow-on programme rather than a dead end. |

### Threats

| # | Threat | Response |
|---|---|---|
| T1 | A vendor (IBM, SandboxAQ, Fortanix) ships dataflow-aware prioritisation during our project year. | File the provisional early (month 10 at the latest, earlier if a competing release appears); our defensible ground is the *evaluated, reproducible, open* version with a public benchmark — vendors publish neither. |
| T2 | The CBOM schema changes mid-project once CISA/NIST publish minimum elements. | Keep the semantic layer schema-independent; emit CycloneDX through a thin adapter. |
| T3 | Publishing before filing destroys Indian patent novelty. | Hard project rule: build → measure → provisional → publish. No preprint before filing. Raised with the guide as an institutional-process question. |
| T4 | Scope creep across languages consumes the year and leaves nothing measured. | Two languages, frozen at month 2. Go only if months 1–8 finish clean. |
| T5 | Retention evidence may be too sparse in real repositories for the score to work. | Explicit early check at month 5 on three repositories. If sparse, pivot to a hybrid mode where the analyst supplies retention *per data class* and the tool propagates it through the dataflow graph — which still automates the hard part and preserves N1–N3. |
| T6 | Expert annotator availability. | Fall back to a documented rubric-driven ordering by two team members plus the guide, with agreement reported; less authoritative, still measurable. |

**Strategic reading.** The project's centre of gravity is W1/T5 — whether enough semantic context is
statically recoverable from real code. Both have concrete month-5 checkpoints and a defined pivot that
preserves the novelty claims. Every other risk is schedule or scope, and is bounded by the layered
design.

---

## 9. Expected Outcomes and Deliverables

1. **Tool** — CLI plus CI action producing a CycloneDX 1.6 CBOM enriched with dataflow, retention and
   exposure annotations, and a ranked migration plan.
2. **Primary quantitative result** — ranking quality against expert order (nDCG@20, Kendall-τ) versus
   algorithm-severity ordering; the first such measurement in this literature.
3. **Secondary result** — actionable-finding precision improvement over the reported ≈0.30 baseline,
   as a precision/recall trade-off curve.
4. **Tertiary result** — verified hybrid patch correctness rate on real multi-file repositories, with
   honest comparison against the 92.5% synthetic-setting figure.
5. **Public benchmark** — 15–20 repositories annotated with crypto assets, protected-data classes,
   retention and expert priority ordering, with inter-annotator agreement.
6. **Provisional patent application** on retention-and-exposure-derived remediation ordering, filed
   before any disclosure.
7. **Paper** targeting a software-engineering or applied-security venue, positioned explicitly as
   implementing the semantic-refactoring pillar identified in [P4].
8. **Demonstration** — a real repository in, a ranked plan and an opened pull request out, in under
   ten minutes.

---

## 10. References

**[P1]** C. Näther and E. Hirsch. *Hidden Ciphers and Where to Find Them: Static Discovery and Assessment of Cryptographic Assets in Software.* arXiv:2608.04857, August 2026. <https://arxiv.org/abs/2608.04857>

**[P2]** A. Shaw. *Quantum-Safe Code Auditing: LLM-Assisted Static Analysis and Quantum-Aware Risk Scoring for Post-Quantum Cryptography Migration.* arXiv:2604.00560, April 2026. <https://arxiv.org/abs/2604.00560>

**[P3]** J. Pallarés de Bonrostro, A. I. González-Tabales and M. I. González Vasco. *Empirical Evaluation of Large Language Models for Migration of Code Fragments to Post-Quantum Cryptography.* arXiv:2606.07341, June 2026. <https://arxiv.org/abs/2606.07341>

**[P4]** L. Zhang. *Toward Quantum-Safe Software Engineering: A Vision for Post-Quantum Cryptography Migration.* Poster, ICSE 2026; arXiv:2602.05759. <https://arxiv.org/abs/2602.05759>

**[P5]** A. D. B. Costa. *Quantum-Safe Cryptography: A Migration Framework for Legacy Systems Toward NIST PQC Standards with the Crypto-Agility Readiness Score.* IACR ePrint 2026/1467, July 2026. <https://eprint.iacr.org/2026/1467>

**[P6]** IBM Research. *The Anatomy of Cryptography Bills of Materials: Standardization and Practice in CycloneDX.* Eurocrypt 2026. <https://research.ibm.com/publications/the-anatomy-of-cryptography-bills-of-materials-standardization-and-practice-in-cyclonedx>

**[P7]** *Towards Cryptography Bill of Materials Compliance.* Springer LNCS, 2026. <https://link.springer.com/chapter/10.1007/978-3-032-19567-8_10>

**[P8]** *On the Practical Feasibility of Harvest-Now, Decrypt-Later Attacks.* arXiv:2603.01091, 2026. <https://arxiv.org/abs/2603.01091>

**[P9]** *Post-Quantum Cryptography and Quantum-Safe Security: A Comprehensive Survey.* arXiv:2510.10436, October 2025, revised June 2026. <https://arxiv.org/abs/2510.10436>

**[P10]** *Securing Cryptography in the Age of Quantum Computing and AI: Threats, Implementations, and Strategic Response.* arXiv:2603.06969, March 2026. <https://arxiv.org/abs/2603.06969>

**[P11]** *A Toolchain for Assisting Migration of Software Executables Towards Post-Quantum Cryptography.* arXiv:2409.07852, 2024. <https://arxiv.org/abs/2409.07852>

**[P12]** *The Cost of Waiting: A Decision-Theoretic Synthesis of Early Versus Late Post-Quantum Migration Under Uncertainty.* Frontiers in Quantum Science and Technology, 2026. <https://www.frontiersin.org/journals/quantum-science-and-technology/articles/10.3389/frqst.2026.1918786/abstract>

**[P13]** S. Rahaman et al. *CryptoGuard: High Precision Detection of Cryptographic Vulnerabilities in Massive-Sized Java Projects.* ACM CCS 2019.

**[P14]** C. Näther et al. *Migrating Software Systems towards Post-Quantum Cryptography: A Systematic Literature Review.* arXiv:2404.12854, April 2024. <https://arxiv.org/abs/2404.12854>

**[P15]** *Harvest Now, Decrypt Later: Examining Post-Quantum Risk.* Finance and Economics Discussion Series, Board of Governors of the Federal Reserve System, 2025. <https://www.federalreserve.gov/econres/feds/files/2025093pap.pdf>

**[P16]** S. Krüger et al. *CogniCrypt: Supporting Developers in Using Cryptography.* IEEE/ACM ASE 2017.

**Standards and regulatory sources.** NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA);
OWASP CycloneDX 1.6 CBOM specification; RBI Q-SAFE committee terms of reference; SEBI Cyber Security and
Cyber Resilience Framework; US Executive Order 14412 (June 2026); Indian Patent Office CRI Guidelines
2025.
