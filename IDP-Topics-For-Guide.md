# IDP — Five Shortlisted Topics

Five project directions we've shortlisted, one page each. All are software-only, use public datasets,
and need at most one GPU.

---

## 1. Crypto-Agility Copilot — automated post-quantum migration

**What it is.** A tool that scans a codebase, finds every place it uses cryptography, works out
which of those places are actually dangerous, and generates the code changes to fix them.

**Why it matters.** Quantum computers will break RSA and elliptic-curve cryptography, with credible
estimates putting "Q-Day" between 2030 and 2033. The problem is already live, though: in a
*harvest-now-decrypt-later* attack, someone records your encrypted data today and decrypts it later.
Anything that must stay secret for a decade — health records, financial data, legal documents — is
already exposed. Industry estimates put roughly ₹2.3 trillion of Indian banking exposure in this
category.

India has already responded. The national quantum-safe task force has set a **2027–2029 migration
deadline for critical infrastructure**, and the **RBI has formed the Q-SAFE committee** (chaired from
IIT Madras) whose stated job includes building a *Cryptography Bill of Materials* — an inventory of
what cryptography an organisation uses. So the requirement is mandated and dated.

**What's missing.** Tools that build these inventories exist (CBOMkit, IBM Quantum Safe, Semgrep
rules), but the research literature calls them **"semantic-free"** — they list that RSA appears
somewhere, without tracking where it sits in the program's data flow. They also miss application-layer
crypto and data-at-rest configuration entirely.

So a CBOM today answers *"what cryptography do we use?"* It cannot answer the only question that
matters: **"what do we migrate first?"** A bank with 4,000 crypto call sites and a 2029 deadline needs
a priority order, and nothing produces one.

**What we'd build.**

- Static dataflow analysis that links each cryptographic call to *what data it protects*, *how long
  that data must stay secret*, and *where it travels*.
- A risk score per data path, giving a ranked migration order — long-retention, externally-transmitted
  data first; throwaway in-process crypto last.
- Automatic generation of hybrid post-quantum patches (X25519 + ML-KEM), with correctness checked by
  differential testing before the patch is proposed.
- Ships as a command-line tool and a CI integration that opens pull requests.

**Why it's a good project.** Pure software, no quantum hardware needed, no dataset to collect, and a
customer who is already looking for it. The prioritisation mechanism looks patentable, and the
evaluation (discovery recall, ranking quality, patch correctness) is a paper.

---

## 2. Hands-Free Indoor Navigation for Blind Users

**What it is.** An app that guides a blind person through an unfamiliar building using audio and
vibration — **with the phone in their pocket**.

**Why it matters.** India has roughly **4.95 million blind people** and around 34 million with visual
impairment. For them, independently finding a room in a hospital, government office or railway station
is close to impossible, because **GPS does not work indoors**.

**What's missing.** Research systems for indoor guidance already exist and work well — they track
movement using the phone's camera and motion sensors. But the researchers who built them state the
problem themselves: a blind person navigating a new space **already has one hand on a cane or a guide
dog**, so using the other for a phone isn't realistic. Holding a phone out also makes them a target,
and people with disabilities already face higher rates of crime.

That's the real gap. It isn't a localisation problem — it's a usability problem. Every accurate system
depends on a camera, and **the moment the phone goes in a pocket the camera is useless**.

**What we'd build.**

- **Magnetic fingerprinting.** Buildings are full of steel, which distorts the Earth's magnetic field
  in a way that is different in every corridor and stable over time. A magnetometer doesn't care that
  it's in a pocket. We match live readings against a pre-surveyed map of the building.
- **Step tracking that tolerates a pocket**, where the phone's orientation relative to the body is
  unknown and constantly shifting.
- **A particle filter constrained by the floor plan**, so the position estimate snaps to real corridors
  and can't drift through walls — walls become useful information rather than an obstacle.
- **Audio and haptic guidance** that doesn't occupy a hand or block ambient sound (blind travellers
  navigate by ambient sound, so masking it would be dangerous).
- Mapping a new building takes one sighted volunteer walking each corridor once.

**Why it's a good project.** Cheap, no special hardware, and the demo is unforgettable — blindfold
someone and they walk to a room with both hands free. Genuine social value, and the mechanism looks
patentable.

---

## 3. Uncertainty-Gated Reasoning — making AI models think only when needed

**What it is.** Reasoning models like o1-style systems spend thousands of tokens "thinking" before
answering — the same enormous effort on *"what is 2+2"* as on a hard problem. We want the model to
read its own internal state and decide, before it starts, whether the hard thinking is actually needed.

**Why it matters.** Long chains of thought are the reason these models are accurate, and also the
reason they're expensive and slow. Spending that budget uniformly, regardless of difficulty, is pure
waste. If you can spend it selectively, you get the same accuracy for much less compute — which is
what makes these models deployable.

The obvious approach — *just ask the model how confident it is* — is known not to work. Models are
systematically overconfident about their own answers.

**What we'd build.**

- Take an existing open reasoning model and **freeze it** — no retraining at all.
- Train a small probe on its internal activations to predict: *will thinking longer actually change
  the answer here?*
- Use that prediction as a gate: easy questions get a short answer, hard ones get the full reasoning
  chain.
- Compare the probe's calibration against the model's own stated confidence — we expect the internal
  signal to be considerably more honest, which is an interesting result in its own right.

**Target result:** match full-reasoning accuracy using **30–50% fewer tokens**, shown as an
accuracy-versus-compute curve against fixed-policy baselines.

**Why it's a good project.** The frozen-model design is what makes it safe. There's no fine-tuning, no
reinforcement learning, nothing that can fail to converge — just a small classifier on extracted
features. Either the signal is there or it isn't, and we'll know within weeks instead of months.

Datasets are standard and public (GSM8K, MATH, plus a code set), models are in the 1.5B–8B range, and
**one 24 GB GPU is enough for the whole project**.

Even a partial result publishes: saving compute at equal accuracy is a real contribution, and the
calibration finding stands on its own regardless.

---

## 4. Explainable Malicious Package Detection

**What it is.** Attackers publish malicious packages to PyPI and npm — typosquatted or trojaned
versions of libraries people install every day. We want a detector that doesn't just flag a package,
but **points to the exact malicious lines and explains why**.

**Why it matters.** Almost all modern software is assembled from these packages, so one poisoned
package compromises every project that installs it. This is now one of the most consequential attack
surfaces in software.

**The two gaps, both with hard numbers.**

1. **Detectors can't explain themselves.** LLMs score between 0.40 and 0.99 F1 on the yes/no question
   *"is this malicious?"* — but collapse to **0.48 F1** when asked to identify *which specific line or
   call* is the malicious one. A security engineer can't act on a verdict with no evidence.
2. **They rot fast.** npm machine-learning detectors dropped from **87% to 39%** effectiveness between
   2021 and 2023, because attackers stopped using obfuscation and switched to minimal, innocuous-looking
   code. Detectors trained on last year's attacks fail on this year's.

The best published system, CHASE, reaches 98.4% recall at a 0.08% false-positive rate — so binary
detection is largely solved, and both gaps above are wide open.

**What we'd build** (one of these as the main target):

- **Explanation grounding.** Combine LLM reasoning with real program analysis — call graphs and taint
  tracking — so the model's explanation has to correspond to an actual data path in the code, not just
  something that sounds plausible. Goal: beat the 0.48 indicator-F1 ceiling.
- **Drift resistance.** Train on pre-2022 malware, test on post-2023 samples, and measure the
  degradation curve against that documented 87%→39% collapse. Behaviour-level features should age
  better than syntactic ones.

**Datasets — all public, nothing to collect.** CHASE's ~3,000 PyPI packages; Mind-the-Gap's 4,070
packages *annotated with the specific malicious indicator* (which is what makes the first target
measurable); an npm set of 6,420 malicious + 7,288 benign; and a time-stamped historical malware
registry for the drift study.

**Why it's a good project.** Clear numbers to beat, public data, splits cleanly into three independent
parts (data, detection, evaluation), and supply-chain security is heavily hired for.

---

## 5. A Distributed Database Built From Scratch

**What it is.** Write a real database engine ourselves — storage, transactions, SQL, and replication
across multiple machines. Essentially, build our own small Postgres.

**Being upfront:** unlike the other four, this isn't novel research. Databases and the Raft consensus
algorithm are well-understood. What it offers instead is depth and a superb demonstration — plus we've
identified a research angle that makes it academically substantial.

**What we'd build.**

- **Storage layer:** a B+-tree or LSM-tree on disk, a page cache, a write-ahead log, and crash
  recovery that actually recovers.
- **Transactions:** MVCC with snapshot isolation, so concurrent readers and writers don't block each
  other.
- **Query layer:** SQL parser, query planner that picks between execution strategies by cost, and the
  execution engine.
- **Distribution:** Raft — leader election, log replication, membership changes, snapshots — so the
  database survives losing a machine.

**The demo.** Three laptops form a cluster running a live transaction workload. Then we **pull the
power on the leader node mid-transaction**. A new leader is elected, the workload keeps running, no
committed data is lost. Plug the dead node back in and it catches up by itself.

**The research angle.** Distributed systems fail in ways normal testing never reaches — a network
partition plus a disk write reorder plus a leader election, all at the wrong moment. Industry solves
this with **deterministic simulation testing**: run the whole system on a fake clock, network and disk
so any failure is replayable from a single random seed.

We'd build that harness and then answer a real question: **which fault-injection strategies find which
kinds of bugs, and at what cost in test time?** Practitioners currently choose these strategies mostly
by intuition, so a measured comparison is a genuine contribution — and it turns "we implemented a
database" into "we built a way to prove a database is correct."

**Why it's a good project.** This is the core of systems computer science — on-disk data structures,
concurrency, crash recovery, consensus. Very low risk too, because every layer is useful on its own: a
single-machine database with working transactions and SQL is already a serious piece of work if the
distributed part runs late.
