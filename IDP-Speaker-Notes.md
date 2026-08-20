# Speaker Notes — Five Topics for the Guide

**Total: ~12 minutes** (2 min per topic + opening + ask). Bullets are cues, not a script — say them
in your own words. **Bold** lines are the ones to actually land.

---

## Opening (30 seconds)

- We surveyed a large number of directions and scored them on feasibility, publishability,
  patentability, impact and demo strength.
- Shortlisted five. All software-only, all public datasets, all need at most one GPU.
- **"For each one we can name the specific gap in the current work, and the number we'd be trying to beat."**
- Ask them to stop you at any point.

---

## 1. Crypto-Agility Copilot (2 min)

**Say:**
- Quantum computers break RSA and elliptic curve. Q-Day estimated 2030–2033.
- But the threat is already live — harvest now, decrypt later. Record encrypted data today, decrypt it
  in 2032. Anything that must stay secret for a decade is *already* exposed.
- India has acted: national task force set a **2027–2029 deadline for critical infrastructure**, and the
  **RBI's Q-SAFE committee** — chaired from IIT Madras — is specifically tasked with building a
  cryptographic inventory.
- Tools for that inventory exist. The literature calls them **"semantic-free"** — they tell you RSA
  appears somewhere, not where it sits in the data flow.
- **"So a bank gets a list of 4,000 places it uses cryptography, and a 2029 deadline. What nothing tells it is which ones to fix first."**
- We'd use dataflow analysis to link each crypto call to what data it protects, how long that data lives,
  and where it travels — then rank by risk. Long-lived data going over the internet first; throwaway
  in-memory crypto last.
- Plus auto-generated hybrid patches, correctness-checked by differential testing.

**If asked "isn't this just a linter?"**
→ A linter matches patterns. We're tracing data flow to work out *consequence*. The output isn't a list
of findings, it's a prioritised remediation plan — that's the part nobody has.

**If asked "what if quantum computing never arrives?"**
→ Doesn't matter. The migration is already mandated by RBI and the national roadmap. We're building for
a compliance deadline, not a prediction.

**If asked about novelty**
→ Dataflow analysis is old, PQC is standard. The claim is binding them: prioritising migration by
protected-data lifetime and exposure. We searched and found no prior claim on that.

---

## 2. Hands-Free Indoor Wayfinding (2 min)

**Say:**
- India has about **4.95 million blind people**, ~34 million visually impaired.
- GPS doesn't work indoors. So finding a room in a hospital or a government office independently is
  effectively impossible.
- Research systems for this exist and work — using the phone's camera and motion sensors.
- But the researchers who built them state the problem themselves: **a blind person already has one hand on a cane or a guide dog.** They don't have a spare hand. Holding a phone out also makes them a target, and people with disabilities already face higher crime rates.
- **"So this isn't a localisation problem. It's a usability problem. Every accurate system needs a camera, and the moment the phone goes in a pocket the camera is useless."**
- Our approach: buildings are full of steel, which distorts the Earth's magnetic field differently in
  every corridor, and stably over time. **A magnetometer doesn't need line of sight — it works in a pocket.**
- Combine that with step tracking, and constrain it with the floor plan using a particle filter — any
  estimate that walks through a wall gets discarded. Walls become information.
- Guidance by spatial audio and vibration. Not headphones — blind users navigate by ambient sound.

**If asked "is a magnetometer accurate enough?"**
→ Not on its own — one reading matches many locations. It works over a trajectory, fused with step
tracking and the floor plan. And the target isn't centimetres, it's "did they reach the room without a
wrong turn."

**If asked "who maps the buildings?"**
→ One sighted volunteer walks each corridor once. That's the whole survey.

**If asked about the user study**
→ Blindfolded participants first to refine the protocol, then blind participants through a local
organisation, with ethics approval — which we'd start applying for in month one.

---

## 3. Uncertainty-Gated Reasoning (2 min)

**Say:**
- Reasoning models generate thousands of tokens of "thinking" before answering. Same effort for
  "what's 2+2" as for a hard problem.
- That's where their accuracy comes from, so you can't just cut it — you have to spend it selectively.
- Obvious idea: ask the model how confident it is. Known not to work — models are systematically
  overconfident about themselves.
- **"Our idea: don't ask the model what it says. Read what it's actually doing internally."**
- Take an open reasoning model, **freeze it** — no retraining at all. Train a small probe on its internal
  activations to predict one thing: will thinking longer actually change the answer here?
- Use that as a gate. Easy questions get short answers, hard ones get the full chain.
- Target: **match full accuracy with 30–50% fewer tokens.** Result is an accuracy-versus-compute curve.
- Second finding: we expect the internal signal to be better calibrated than the model's stated
  confidence. That's publishable on its own.

**If asked "why is this low risk?"** — this is the strongest thing you can say about it
→ Because the model is frozen. No fine-tuning, no reinforcement learning, nothing that can fail to
converge. It's a small classifier on extracted features. Either the signal is there or it isn't, and we
know in weeks, not months.

**If asked "what if the saving is small?"**
→ A smaller saving at equal accuracy is still a result, and the calibration comparison stands
independently. There's no outcome where we finish with nothing.

**If asked "couldn't the probe just be detecting long questions?"**
→ Real concern, and we test for it with length-matched controls.

**Resources:** one 24 GB GPU. GSM8K, MATH, plus a code set. All public.

---

## 4. Explainable Malicious Package Detection (2 min)

**Say:**
- Attackers publish poisoned packages to PyPI and npm — typosquatted names, code that runs at install
  time and steals credentials. One bad package compromises every project that installs it.
- Two gaps, both with hard numbers:
- **One:** LLMs get 0.40–0.99 F1 on "is this malicious?" — but drop to **0.48 F1** on identifying *which
  specific line* is the malicious one.
- **"A security engineer can't act on a verdict with no evidence. And right now the tools that give a verdict can't point at anything."**
- **Two:** npm detectors fell from **87% to 39%** between 2021 and 2023 — because attackers stopped
  obfuscating. The detectors had learned obfuscation as a proxy for malice.
- Best published system, CHASE, gets 98.4% recall at 0.08% false positives. So detection is largely
  solved; explanation and durability are not.
- Our approach for the first: build the call graph and taint-track from credential sources to network
  sinks, then **require the model's explanation to correspond to a real data path in the code.** It can
  still reason about what's suspicious; it can't invent the evidence.
- All datasets are public — including one with 4,070 packages annotated with the specific malicious
  indicator, which is what makes this measurable.

**If asked "why will yours be better?"**
→ Because we constrain the output. The current failure is that an LLM's explanation sounds right whether
or not it is. Program analysis makes plausible-but-wrong explanations rejectable.

**If asked about false positives**
→ That's why we report recall at fixed low false-positive rate, not raw accuracy. At 0.1% FPR across
500,000 packages you'd still generate 500 false alarms, so it's the only honest metric.

---

## 5. Distributed Database From Scratch (2 min)

**Be upfront — it lands better:**
- **"This one isn't novel research and we won't pretend it is. Databases and Raft are well understood."**
- What it offers is depth and a demonstration — plus we've found a research angle that makes it
  substantial.
- Scope: storage engine on disk, write-ahead log and crash recovery, MVCC transactions, SQL parser and
  a cost-based query planner, then Raft replication across machines.
- That's the core of systems computer science — on-disk structures, concurrency, recovery, consensus.

**The demo — describe it, it sells itself:**
- Three laptops, one cluster, live transaction workload.
- **"Then we pull the power on the leader node mid-transaction. A new leader gets elected, the workload keeps running, nothing committed is lost. Plug the dead machine back in and it catches up by itself."**

**The research angle:**
- Distributed bugs need exact interleavings — a network partition, plus a disk write reorder, plus an
  election, all at once. Normal testing never finds them and can't reproduce them.
- Industry solves this with deterministic simulation — run the system on a fake clock, network and disk
  so any failure replays from a single random seed. It's how FoundationDB and TigerBeetle are built.
- We'd build that harness, then measure **which fault-injection strategies find which classes of bugs, at
  what cost in test time.** People currently choose those strategies by intuition.
- **"That turns 'we implemented a database' into 'we built a way to prove a database is correct.'"**

**If asked "is it too big?"**
→ Every layer is useful alone. A single-machine database with working transactions and SQL is already a
serious artefact if the distributed part runs late. Nothing is all-or-nothing.

---

## Closing ask (30 seconds)

- **"We can start on any of these. What we'd like from you is which fits the department's direction and your own interests."**
- Our own order: Crypto-Agility first, Wayfinding second, UGR if you'd rather we optimise for a paper.
- One procedural question: for the first two we'd want to file a provisional patent, and **publishing
  before filing destroys novelty in India.** So we'd need to build → measure → file → then publish. Can
  you guide us on the institutional IP process?

---

## Quick reference — if you only remember five lines

| Topic | The line |
|---|---|
| Crypto-agility | "A bank gets 4,000 crypto call sites and a 2029 deadline. Nothing tells it which to fix first." |
| Wayfinding | "It's not a localisation problem, it's a usability problem — blind users have no spare hand." |
| UGR | "Don't ask the model what it says. Read what it's actually doing." |
| Malicious packages | "0.48 F1 on *which line is malicious*. A verdict with no evidence is unusable." |
| Database | "We pull the power on the leader mid-transaction and nothing is lost." |

## Numbers worth memorising

- Q-Day 2030–2033 · RBI Q-SAFE, IIT Madras · CII deadline 2027–2029 · ₹2.3 trillion HNDL exposure
- 4.95 million blind in India · ~34 million visually impaired
- Target 30–50% token reduction at equal accuracy · one 24 GB GPU
- 0.48 indicator-F1 · 87%→39% detector drift · CHASE 98.4% recall @ 0.08% FPR
- Datasets: 3,000 PyPI · 4,070 indicator-annotated · 6,420 malicious + 7,288 benign npm
