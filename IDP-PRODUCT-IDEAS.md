# IDP Product & Patent Ideas — Classical + Quantum

Companion to `IDP-MASTER-CATALOG.md`. **Nothing there is replaced.** That file optimises for
*"will this produce a publishable paper?"*. This file optimises for a different pair of goals:

1. **Patentable** — a specific, non-obvious *technical mechanism* you can claim.
2. **Actually used** — a thing a real person opens and is measurably better off for.

Constraints applied to every idea below: buildable by **you + Claude Code** in a year, software-first,
**college GPU available** (so training is fine), minimal-hardware options flagged explicitly.
Generated 2026-08-17.

---

## Before anything: the patent rules that decide what's worth filing

India's **CRI Guidelines 2025** (IPO, 29 Jul 2025) are the gate. Section 3(k) still bars "computer
programme per se", but the 2025 guidelines settle two things in your favour:

- **Technical effect is the test.** A concrete, reproducible improvement to a technical system —
  less compute, less memory, lower latency, better signal fidelity, stronger security, measurably
  higher accuracy on a technical task.
- **No novel hardware required.** Technical effect achieved by software on general-purpose hardware
  is now sufficient. This is the change that makes a student software project filable.

What still gets refused: a better *informational output*, an automated business method, a prettier
presentation of data. **"We built an app that shows users X" is not patentable. "We built a method
that resolves ambiguity in X by coupling signal A into decoder B, cutting error N%→M%" is.**

> ⚠️ **Publish-vs-patent trap — read this before you arXiv anything.** In India (and the EPO/most of
> the world) a public disclosure before filing destroys novelty. Section 31 grace is narrow and
> unreliable. **File a provisional first (~₹1,600 for individuals/startups, buys 12 months), then
> publish.** Your capstone is trying to be both a paper *and* a patent — the ordering is: provisional →
> paper → complete spec. Get this wrong and you lose the patent, not the paper.

Every idea below states its **claim** — the one sentence a patent attorney would build around.

---

# Part A — Classical ideas (no quantum)

## P1 — Prescription Safety Net (offline, handwriting → drug-safety check)

**Who uses it:** anyone handed a handwritten prescription in India — plus the pharmacist reading it.
Adverse drug events hit 5–10% of hospitalised patients, a big slice from illegible handwriting,
wrong dose, and missed interactions. Elderly patients on 5+ drugs from 3 specialists are the sharp end.

**What exists:** OCR "prescription reader" apps (MediSathi etc.) and drug-interaction APIs
(Drugs.com, Medscape). They are two separate boxes: OCR guesses the text, then a checker looks up
whatever the OCR guessed. **The failure is at the seam** — OCR guesses wrong, the checker confidently
checks the wrong drug.

**The claim (the patentable bit):** *don't decode then check — decode* ***using*** *the check.*
Keep the OCR's top-k candidate lattice instead of one string, and re-score candidates jointly against
a pharmacological plausibility model (does this drug + this dose + this frequency + this patient's
existing meds and indication actually co-occur?). "Amlodipine 5mg OD" beats "Amiodarone 5mg OD" not
because the pixels say so but because 5mg OD is not an amiodarone dose. Then a calibrated
abstain-gate: below confidence τ, refuse to answer and say *which token* is unreadable.
That reverse coupling — semantics into the decoder, plus a refusal threshold — is a technical effect
(measurable accuracy lift on a technical task), and I found no product doing it.

**Build:** on-device TrOCR/Donut-class model fine-tuned on Rx handwriting + an interaction graph from
open drug data + a small dose-plausibility model. Speaks the result in the local language.
Runs offline (privacy — this is health data under DPDP).

**Risk:** you'll need to build a handwritten-Rx dataset; that's the real cost. Start by asking one
local clinic. Regulatory: ship as *decision support to the pharmacist/patient*, never as a diagnosis.

---

## P2 — Scam Interception at the Moment of Payment ⭐

**Who uses it:** every UPI user with a parent. AI voice-cloning needs 3–30s of audio, and
INTERPOL's Mar-2026 assessment puts impersonation fraud among the leading drivers of >$400B in global
losses. CERT-In flagged it as India's fastest-growing fraud vector.

**What exists:** Google rolled out fake-call detection in Phone by Google (Jun 2026) — but it works by
a **device-to-device encrypted handshake**, so it only helps when *both* sides use Phone by Google, on
a normal cellular call. The scam that actually lands in India arrives on **WhatsApp**, from a fresh
account with a stolen profile photo. No handshake exists to check. Caller-ID apps flag unknown numbers;
these calls aren't from unknown numbers, they're from "your son".

**The claim:** fuse three on-device signals that are currently never combined, and intervene at the
**transaction moment**, not the call moment —
(a) *conversation structure*: the coercion script (manufactured urgency → isolation → secrecy → payment)
is far more invariant across scams than any acoustic artefact;
(b) *synthesis artefacts* in the audio;
(c) *concurrent app state*: a payment app being foregrounded, or a UPI intent being constructed, while
(a) and (b) are elevated.
When the joint score crosses threshold, don't just show a banner — **impose friction on the payment
intent**: a cooldown timer, a callback-the-saved-number prompt, or a shared-secret challenge that a
cloner can't answer. Cross-signal fusion + transaction-time intervention is the mechanism. Strong,
narrow, defensible claim.

**Build:** Android accessibility/notification listener + on-device ASR (Whisper-small / IndicASR
distilled) + small classifier for coercion-script detection + anti-spoof audio front-end.
Everything on-device (you cannot ship people's phone calls to a server, legally or ethically).

**Why it's the best of the classical batch:** highest patent strength × highest daily-user value ×
a demo that visibly stops a live scam in front of examiners. Hardest part is Android plumbing, and
that is exactly what Claude Code is good at.

---

## P3 — Two-Way Indian Sign Language

**Who uses it:** ~7 million deaf Indians. ISLRTC counts about **300 certified ISL interpreters**
for all of them. That ratio is the entire pitch.

**What exists:** plenty of isolated-sign recognition (YOLO/Swin models hitting 95–98% on *single
signs*), CISLR (~4,700 words) and iSign benchmarks. **Continuous, gloss-free sentence translation is
still open**, and nothing usable runs on a phone in a shop or a clinic.

**The claim:** per-signer few-shot adaptation. ISL varies by region, hand size, skin tone, and speed;
a general model degrades on the individual. Claim a lightweight adapter enrolled from ~30 seconds of a
user signing a fixed calibration set, updating only a low-rank adapter on a frozen backbone, with the
adaptation running **on-device** — technical effect: accuracy lift at fixed compute/memory budget.

**Build:** MediaPipe pose/hand landmarks → temporal transformer → gloss-free seq2seq. Reverse
direction (speech → sign avatar) via a 3D avatar driven by pose sequences.

**Honest risk:** highest-impact idea here, **and** the highest failure risk — continuous ISL data is
thin and you may end up shipping phrase-level rather than free translation. Only take this if the
team genuinely cares about it; a half-working version still helps people and still publishes.

---

## P4 — Runtime Accessibility Repair ⭐ (best patent-per-unit-effort)

**Who uses it:** blind and low-vision Android users, every day. This is the complaint the 2026
assistive-tech reviews keep repeating — *"the ceiling rose dramatically and the floor barely moved"*.
Screen readers are excellent; the apps they read are broken. An unlabelled button is announced as
"Button" and the user is stuck.

**What exists:** FixAlly (arXiv 2408.03827) fixes accessibility issues **in source code**, iOS/SwiftUI —
which requires being the developer of the app. Nobody fixes the app you didn't write, on the device,
while you use it.

**The claim:** an on-device agent that reads the live accessibility tree + screen graph, synthesises
the missing semantic labels from surrounding visual and structural context (icon glyph, sibling text,
navigation position), and **injects them back into the accessibility tree before the screen reader
speaks it** — with a cache keyed by (app, version, view-signature) so the expensive inference runs once
per screen, not once per glance, and a user-correction loop that pins a corrected label permanently.
The version-keyed cache + correction loop is what turns "call an LLM on a screenshot" (obvious, slow,
unpatentable) into a claimable system with a real technical effect: latency and compute per screen
reduced to ~zero after first visit.

**Build:** Android AccessibilityService + a small on-device VLM (or quantised Gemma-3n class) +
SQLite label cache. Pure software, no dataset collection — you generate your own eval by scanning the
top-200 Play Store apps for unlabelled nodes.

**Why I rank it top-3:** low failure risk, clean claim, a user base that will tell you loudly whether
it works, and an evaluation ("% of unlabelled interactive elements correctly named, latency after
cache warm") that is a paper table on its own.

---

## P5 — Appliance-Level Electricity Bill Breakdown (minimal hardware)

**Who uses it:** anyone whose bill jumped and doesn't know why. Output is literally
"your geyser cost ₹840 last month; shifting it 2 hours saves ₹210."

**What exists:** NILM (non-intrusive load monitoring) is a mature research field; deep-learning
disaggregation works well **when you have labelled data for that home**. The 2026 reviews name the
blockers: behavioural similarity between appliances, and scalability/deployment — i.e. *nobody has
labels for your house*.

**The claim:** solve the deployment gap, not the accuracy gap. Claim an active-learning loop that
picks the *maximally informative moment* to ask the resident one question ("did you just switch
something on?"), converting a stranger's home into a labelled home in a handful of taps — plus
transfer from a pretrained signature bank so the cold-start is warm. Technical effect: target
disaggregation accuracy reached with an order of magnitude fewer labels.

**Hardware:** either **zero** (parse the utility's 15/30-min interval data where available) or
**~₹1,500** (ESP32 + split-core CT clamp on the main line — no electrician, no rewiring). Public
datasets to bootstrap: UK-DALE, REDD, SmartNIALMeter.

---

## P6 — DPDP Consent & Erasure Toolkit

**Who uses it:** every Indian business processing personal data. DPDP Rules were finalised Nov 2025;
the **Consent Manager framework goes live 13 Nov 2026** and full compliance is due **mid-May 2027**.
An EY survey found >81% of organisations hadn't even drafted a DPDP-aligned policy and >83% hadn't
started implementation. That is a market with a deadline attached.

**The claim:** most of this is compliance paperwork (not patentable). The one technical core worth
claiming: **verifiable consent receipts with automatic erasure propagation** — a cryptographic receipt
that lets a user prove what they consented to and when, and lets a fiduciary prove erasure actually
propagated through downstream processors and backups, without either side trusting the other's logs.
Merkle-anchored receipts + a propagation-proof protocol.

**Reality check:** registering as an actual Consent Manager needs serious net worth — you're building
the **tooling/SDK**, not the licensed entity. Lower demo value, high real-world usefulness, and the
easiest of these to turn into revenue.

---

## P7 — Camera-Free, Wearable-Free Fall & Distress Detection (minimal hardware)

**Who uses it:** elderly people living alone — a huge and growing Indian demographic — and their
children in another city. Wearables fail for the honest reason the literature keeps stating: elderly
users won't wear them and forget to charge them. Cameras are rejected on privacy (nobody wants one in
a bathroom, which is where falls happen).

**What exists:** WiFi CSI fall detection is well-proven in the lab (93–99% accuracy across 2–10m,
works through walls, SenseFi + open-source frameworks available). **It does not survive moving to a new
home** — models are environment-specific, which is why this is research and not a product.

**The claim:** environment-invariant sensing. Self-supervised embedding trained to be invariant to room
geometry via domain-adversarial training, plus **unsupervised on-site adaptation** during the first days
of normal living (no scripted calibration, no asking a 78-year-old to fall over on purpose). Technical
effect: accuracy retained on unseen environments with zero labelled calibration.

**Hardware:** 2× ESP32 (~₹800 total) as CSI transmitter/receiver, or a router with CSI extraction.
Minimal, cheap, and the demo — detecting a fall through a wall with no camera — is unforgettable.

---

## P8 — Deepfake Detection for Ordinary Video Calls

**Who uses it:** anyone taking a video call from a "relative" or a "CFO". Live face-swap now responds
to motion and prompts, so **passive liveness checks built for photo/replay attacks simply don't catch
it**, and Zoom/Teams/Meet ship no reliable built-in detection in 2026.

**The gap worth exploiting:** a 2026 analysis of the research literature found **precisely zero** papers
targeting real-time/live-stream conditions as their primary threat model, while 71% studied offline
public-figure video. The field is optimising the wrong problem. That is your opening — and it makes
both a paper and a patent.

**The claim:** active **rendering-stress challenge-response** — inject prompts a real-time face-swap
pipeline is structurally bad at (rapid profile turn with self-occlusion, hand crossing the face,
sudden specular change from screen brightness flash), and score the *reconstruction failure* rather
than static artefacts, fused with passive cues, in-band on a normal WebRTC call. Claim the
challenge-selection policy (pick the challenge that maximises expected discriminability given current
bandwidth/lighting) — that's the non-obvious part, and it directly addresses the false-positive
constraint that blocks legitimate users.

---

## P9 — Crowdsourced Road Hazard Map (phone in your pocket)

**Who uses it:** every two-wheeler rider; municipal road departments as the downstream consumer.
**Claim:** hazard classification from IMU alone (no camera, no dashcam), with vehicle-and-mounting-
invariance learned rather than calibrated, GPS-drift-robust localisation by multi-pass fusion across
riders, and **privacy-preserving aggregation** so no individual's route is reconstructable from
contributions. Software-only, phone stays in the pocket.
**Caveat:** the most crowded idea in Part A (several apps and papers exist) — patent hinges entirely on
the invariance + private-aggregation combination. Lowest patent confidence here; included because the
usefulness is undeniable.

---

# Part A2 — Classical ideas, batch 2 (selected for the demo)

**What makes a demo land**, and what every idea below is filtered against:

1. **The examiner participates.** They hold the phone, they walk the corridor, they pick which strip is fake.
2. **It runs with the WiFi off.** Campus networks fail on demo day. Every idea here works offline.
3. **The result is a verdict, not a dashboard.** "Fake" / "adulterated" / "turn left in 4 steps" beats a chart.
4. **Failure is visible and honest.** A system that says "I can't read this" earns more trust than one that
   guesses. Build the abstain path — it's also where the patent claims live.
5. **60 seconds, no setup.** If it needs a calibration ritual, it isn't a demo, it's a rehearsal.

---

## P10 — Counterfeit Medicine Verification Without a QR Code ⭐ (best demo in this document)

**The demo:** two visually identical strips of the same medicine on the table. Examiner picks either one,
scans it, phone says **GENUINE** or **COUNTERFEIT** in about a second. No internet. Nothing else needed.

**The problem:** India has a well-documented spurious-drug problem, with police busting fake life-saving
drug rackets and spurious stock crossing state lines. The government's answer is **mandatory QR codes** —
amended Drugs Rules, nine data elements, effective **1 July 2027** for most categories and 2028 for
antimicrobials.

**Why the QR mandate leaves a gap you can fill:** a QR code is *copyable*. A counterfeiter photographs a
genuine pack's QR and prints it on 10,000 fakes, and every scan returns a valid record. This isn't
hypothetical — **fake holograms have already been found on spurious antimalarials in India**. And the
documented risk isn't at the factory (those drugs are trustworthy); it's at the **transfer points between
wholesalers, distributors and sub-distributors** where product is swapped. A code that authenticates the
*data* cannot authenticate the *object*.

**The claim:** authenticate the physical object using its own randomness. Every printed carton carries an
**inherent physical unclonable function** — the microscopic randomness of ink droplet spread on paper
fibre, which the printer itself cannot reproduce twice. Register a compact hash of that microstructure at
manufacture; verify it later from an ordinary phone camera. The patentable core is **not** "use a PUF" —
that's known (inkjet-printed PUFs, paper-texture authentication, 2026 work exists). It's making it work
**on a phone, in the field, over a supply chain's lifetime**: pose- and illumination-invariant feature
extraction from an uncontrolled handheld capture, plus a **degradation-tolerant matcher** that still
authenticates a carton after months of scuffing, humidity and handling — with a calibrated abstain when
the surface is too damaged. Field robustness is the unsolved part and the technical effect is measurable
(false-accept/false-reject vs wear).

**Build:** phone macro capture + classical texture features (or a small CNN) + a registration DB. Print
your own test cartons on a normal inkjet to build the dataset — you can generate hundreds in an afternoon,
so **no data-collection blocker**. Works offline once the batch's registry is cached.

**Why I rank it first:** unforgettable demo, a real crime it prevents, a regulatory tailwind that *creates*
the customer without solving the problem, and a claim that's narrow enough to survive examination.

---

## P11 — Stampede Early Warning From Cameras That Already Exist

**Timeliness:** a stampede-like incident at an Indian temple killed at least seven people on **17 August
2026** — the day this section was written. Vaishno Devi, Nalanda, Andhra Pradesh: this recurs.

**The demo:** feed real crowd footage; the overlay shows density and flow, and the system announces
**"gate 3 reaches critical in ~90 seconds"** *before* anything visibly goes wrong. Predicting the incident
before it happens is a far better demo than detecting it after.

**What exists:** YOLOv8m + CNN-LSTM crowd-monitoring frameworks, density analytics, drone-based monitoring
recommendations. Nearly all of it **detects the current state**. Reviews of Indian mass-gathering safety
name the gap plainly: limited deployment of real-time analytics leaves authorities **unable to respond to
emerging dangers** — the problem is lead time, not measurement.

**The claim:** forecast the **time-to-critical-density** per zone, not the current density. Known physics
gives you the target — risk rises sharply above ~5 persons/m², and Crowd Risk Index work combines speed,
flow, density and behaviour. Claim a model that estimates *when* each zone crosses threshold from inflow/
outflow dynamics at connected gates, and — the genuinely non-obvious part — **recommends the minimal
intervention** (which gate to hold, for how long) by simulating the counterfactual, so the alert is
actionable by a constable with a whistle rather than being one more alarm. Technical effect: warning lead
time at fixed false-alarm rate.

**Build:** existing CCTV/public footage + crowd-counting backbone + a flow model. Runs on your GPU.
**Ethics guardrail to state up front:** count people, never identify them — no face recognition, no
tracking of individuals. Say this in the paper and the demo; it will be asked.

---

## P12 — Milk & Cooking-Oil Adulteration Test (₹5 of hardware)

**The demo:** examiner brings any milk. Drop it on a paper strip, wait, photograph. Phone reports
**"starch detected, ~0.4%"**. Then do it with a sample you spiked. Watching a phone catch food fraud in
front of you is visceral in a way no dashboard is.

**The problem:** FSSAI reports persistent adulteration in milk supply chains, especially in rural and
semi-urban distribution.

**What exists:** a solid research base — paper-based microfluidic sensors with 10 µL samples read by phone
after 5 minutes, colorimetric assays for starch/H₂O₂/NaClO with smartphone image analysis, detection limits
around 0.2% and recoveries of 91–105%. This is **lab-validated science that never became a usable product**,
which is exactly the kind of gap a capstone can close.

**Why it isn't already solved:** colorimetry from a phone is a nightmare outside a lab — every phone's
camera pipeline applies its own white balance and tone curve, kitchen lighting is yellow, and the strip
ages. Published work sidesteps this with controlled setups.

**The claim:** self-referencing colorimetry. Print **known reference patches beside the reaction zone** on
the same strip, and solve for the illuminant and camera response from those patches before reading the
sample — making the measurement invariant to phone model and lighting without any calibration step by the
user — plus a reaction-kinetics model so the reading is timing-tolerant instead of demanding an exact
5-minute wait. Technical effect: quantification accuracy across uncontrolled devices/lighting. That
invariance is the product, and it's claimable.

**Hardware:** printed paper strips (cents each) + reagents from a college chemistry lab. **Get a chemistry
faculty member as co-supervisor** — it makes the reagent work trivial and strengthens the filing.

---

## P13 — Hinglish Doctor–Patient Consultation Scribe

**The demo:** two people role-play a consultation in natural mixed Hindi-English — *"do din se fever hai,
and there's body ache"* — and a structured clinical note assembles live on screen with speakers correctly
separated.

**The problem, quantified:** **over 250 million people in India code-switch**, and ASR models suffer a
**30–50% relative WER increase** on code-switched speech versus monolingual. Every AI-scribe product sold
in India is built on monolingual assumptions.

**What exists:** the DISPLACE-M challenge (2026) produced a Qwen3-based system with end-to-end neural
diarization hitting **18.59% tcpWER**, first of 25 entrants. HiACC provides a code-switched Hinglish corpus.
So there's a **public baseline number to beat** — which makes this one of the few ideas here that is
*also* a clean paper in the master-catalog sense.

**The claim:** the named hard part is **rapid turn-taking and heavily overlapped speech** in real consults.
Claim joint diarization-and-recognition where **role priors** (doctors ask, patients describe symptoms;
drug names and dosages come from one side) feed back into speaker assignment — resolving overlap by
*who is likely saying this kind of thing*, not by acoustics alone. Then constrain decoding to a medical
lexicon so drug names survive code-switching. Technical effect: tcpWER and speaker-attribution accuracy.

**Build:** DISPLACE-M + HiACC + Whisper/Qwen-ASR fine-tuning on your GPU. On-device is the goal (health
data + DPDP), which pairs with **Q10**.

---

## P14 — Hands-Free Indoor Wayfinding for Blind Users

**The demo:** blindfold an examiner. They walk from the entrance to a specific room, guided only by audio
and haptics, phone in pocket. Nothing else in this document produces that moment.

**The gap, stated by the researchers themselves:** existing apps use phone IMU/VIO for GPS-denied indoor
guidance, but **"a blind person navigating a new space often has at least one hand in use for a guide dog
or a cane, so using the other for a phone is less than ideal"** — and holding a phone out **raises the
risk of crime**, which people with disabilities already face disproportionately. The usability constraint,
not the localisation math, is the unsolved problem.

**The claim:** localisation that works **with the phone in a pocket**. Pocket placement destroys the
camera-based VIO everything else relies on, so claim fusion of pedestrian dead-reckoning with **building
magnetic-field anomaly fingerprints** (steel structure makes every corridor magnetically distinctive) and
map-constrained particle filtering that snaps the estimate to walkable geometry — with guidance delivered
as spatialised audio and haptic patterns that don't occupy a hand or an ear. Technical effect: positioning
error with no camera and no hand.

**Bonus:** the map problem solves itself — a sighted volunteer walking the building once generates the
fingerprint map. **Pairs directly with P4** (runtime accessibility repair): same users, same team,
one story about independence indoors. This is the strongest two-idea combination in the repo.

---

## P15 — Speech Restoration for Atypical Speakers

**The demo:** a recording of severely dysarthric speech plays — the room can't understand it. The system
outputs the same sentence, intelligibly, after a five-minute enrollment. People are visibly moved by this
one; it's the demo with the highest emotional weight here.

**Who uses it:** people with cerebral palsy, ALS, Parkinson's, post-stroke dysarthria — for whom ordering
food or being understood by a call-centre IVR is a daily wall.

**Where the field is:** commercial ASR works for *mild* dysarthria and **performs poorly for moderate or
severe**, and speaker-dependent training is **"tiring and time-consuming"** for exactly the people least
able to spare the effort. CLARIS (CHI 2026) converts atypical speech to fluent speech with cross-language
personalization; few-shot personalization (MetaICL) and federated personalization are 2026-active.

**The two openings:** (a) TORGO, the field's workhorse corpus, has **8 speakers of one English variety** —
Indian-language dysarthric speech is essentially unserved; (b) enrollment burden is the adoption blocker,
and it is a *technical* problem: which utterances you ask for determines how much you learn per minute of
a tiring task.

**The claim:** **active enrollment** — choose the next phrase to elicit by maximising expected information
gain over the speaker's articulation-error model, reaching target intelligibility in a fraction of the
enrollment time, with adaptation confined to a small on-device adapter. Technical effect: intelligibility
per second of enrollment effort. That framing is honest, measurable and unclaimed.

**Ethics:** co-design with actual users from day one, or don't do it. The literature on assistive-tech
*abandonment* is the reason so many of these projects die.

---

## P16 — Forward Collision Warning for Two-Wheelers, From a Phone

**The demo:** rider's-eye footage plays; the app calls out **"brake"** a second and a half before the
near-miss the examiner hasn't spotted yet.

**The stakes:** two-wheelers are **over 70% of India's registered vehicles** and a higher share of the
**480,583 accidents recorded in 2023** — riders are the largest group of those killed.

**What exists, and why it's the wrong thing:** nearly everything is **post-crash** — accelerometer crash
detection, SOS alerts, smart helmets, QR emergency tags. Those help after you're on the road. Pre-crash
warning is left to V2V infrastructure that India doesn't have.

**The claim:** monocular forward-collision warning tuned for the two-wheeler case, which is genuinely
different from car ADAS and not just a port of it: motorcycles **lane-split and lean**, so the camera roll
angle changes constantly and the threat is frequently *lateral encroachment* rather than a lead vehicle
slowing. Claim roll-compensated time-to-collision estimation from a pocket/handlebar phone with a
**lean-aware threat model**, plus warning-timing that adapts to the rider's own observed reaction latency.
Technical effect: warning lead time at fixed false-alarm rate, which is the metric that decides whether a
rider keeps the app installed or uninstalls it in a week.

**Caveat, stated plainly:** ADAS is a crowded patent field. Your defensible ground is the lean/roll
compensation and the two-wheeler threat geometry, not collision warning in general. Check prior art
carefully before drafting.

---

## P17 — Anemia Screening From a Photo (good demo, crowded field — read before choosing)

**The demo:** photograph the inner eyelid, get a hemoglobin estimate. Fast, visual, medically meaningful —
and anemia is genuinely one of India's largest public-health burdens.

**Why I'm ranking it lower than its impact suggests:** this field is *full*. Nature Communications (2018)
reported fingernail-photo hemoglobin at ±2.4 g/dL and 97% sensitivity; NiADA has run clinical studies with
**2,476 participants**; AnemiaVision (2026) reports 94–97% accuracy on conjunctiva+fingernail. Beating a
number is possible; getting a patent through is much harder here.

**If you take it, the only claim I'd file:** cross-device and cross-skin-tone calibration invariance —
the failure mode that keeps these apps in papers instead of clinics — using in-frame reference (a printed
card or the sclera as a white reference) rather than learned priors that quietly encode skin tone.
Technical effect: error consistency across devices and Fitzpatrick types. **Also the ethically correct
framing**, since uneven performance across skin tones is the documented harm in this literature.

---

**Considered and skipped:** hyperlocal air-quality sensor calibration (real gap — one calibration model
doesn't hold over time — but the demo is a chart, and demo quality was the filter here).

---

# Part B — Quantum-track ideas

**Read this first, because it saves you a year.** In 2026 quantum machine learning has **no proven
real-world advantage**; classical methods are faster and more reliable for essentially every ML task
people care about, and the honest forecasts say not in 2026 and probably not 2027. Quantum kernel
benchmarks across 64 datasets and 20,000+ models come back "mixed at best", with exponential
concentration a fundamental scaling concern.

So there are exactly **three honest ways** to do a quantum project that is *useful to people*:

1. **Quantum as the threat** — build the classical software people need *because* quantum is coming
   (PQC migration). 100% real, funded, deadlined. ← **strongest**
2. **Quantum-inspired** — take the math (tensor networks) and run it on your GPU, beating classical
   heuristics today, with no QPU involved. Honest and effective, as long as you say so.
3. **Hybrid with a fallback gate** — use a QPU only where it might help and prove, per instance, when
   it doesn't. Patent the *decision*, not the speedup.

Anything that requires quantum advantage to be true in order to work is a trap.

---

## Q1 — Crypto-Agility Copilot: dataflow-aware CBOM + auto-migration ⭐ (best quantum-track pick)

**Who uses it:** every bank, every CII operator, eventually every engineering team. India's national
task force set a **2027–2029 quantum-safe migration timeline for critical infrastructure**; the RBI
stood up the **Q-SAFE committee** (chaired from IIT Madras) whose stated task includes building a
**Cryptography Bill of Materials (CBOM)** and assessing crypto-agility; SEBI's CSCRF names
harvest-now-decrypt-later directly. Estimates put ₹2.3 trillion of Indian banking exposure to HNDL.

**What exists and where it breaks:** CBOMkit (Linux Foundation PQCA), IBM Quantum Safe, SandboxAQ,
Semgrep rules. The stated 2026 gaps: discovery **covers network protocols well but misses
application-layer crypto, data-at-rest configuration, and embedded firmware**; CycloneDX 1.6 support is
uneven; and — the important one from the research literature — **current CBOM tools are "semantic-free":
they list that RSA appears somewhere, not where that key sits in the program's control and data flow.**

**The claim:** make the CBOM semantic. Static dataflow analysis that binds each cryptographic primitive
to (i) the data it protects, (ii) that data's retention lifetime, and (iii) its exposure surface —
producing a per-data-path **HNDL exposure score** (long-retention + externally-transmitted + classical-KEM
= migrate first), and then generating a **verified hybrid-migration patch** (X25519+ML-KEM) whose
equivalence to the original is checked by differential testing. Prioritised, dataflow-derived migration
ordering is a concrete technical effect and, as far as I can find, unclaimed.

**Build:** pure software. Tree-sitter/Semgrep + a dataflow pass per language, CycloneDX 1.6 output,
liboqs for the hybrid primitives, auto-PR generation. No quantum hardware, no GPU needed. Ships as a
CLI + GitHub Action that a real team can adopt on day one.

**Why this is my top quantum pick:** it is the only idea in Part B where the customer is already
looking for the product, the deadline is set by a regulator, and nothing depends on quantum hardware
ever working.

---

## Q2 — Quantum-Inspired Tensor-Network Scheduler (runs on your college GPU)

**Who uses it:** your own college's exam/timetable office, a hospital's OT scheduler, an ambulance
dispatcher, an EV charging hub. Real, boring, valuable.

**The honest framing:** tensor-network methods are quantum *mathematics* on classical hardware — MPS/DMRG
machinery applied to constrained combinatorial optimisation (knapsack, shortest path, scheduling have
all been done this way). Reported GPU-optimised quantum-inspired solvers reach up to ~80× over
traditional solvers on suitable problems. **No QPU. Say so in the first line of the paper.**

**The claim:** feasibility-preserving contraction — encode hard constraints as projectors applied during
MPS contraction so that infeasible assignments are never represented, rather than penalised after the
fact (the standard QUBO-penalty approach, which wastes the whole search on invalid states). Technical
effect: time-to-feasible-solution and memory at fixed bond dimension.

**Build:** PyTorch/quimb/ITensor, one GPU. Benchmark against OR-Tools CP-SAT — and **be prepared for
CP-SAT to win on some instances**; that's a finding, not a failure, and it feeds Q3.

---

## Q3 — Per-Instance Solver Router (quantum / quantum-inspired / classical)

**The insight:** everyone in 2026 runs hybrid pipelines — annealers for a warm start, gate-based for
refinement, classical for the rest — and **nobody knows in advance which one to use for a given
instance.** Choosing is currently folklore.

**The claim:** a learned dispatcher that predicts, from cheap structural features of a problem instance
(constraint-graph treewidth, density, degeneracy, symmetry), which backend will return the best solution
within a given time/cost budget, and routes accordingly — with a guaranteed classical fallback so the
system is never worse than the baseline. Technical effect: better solution quality per unit compute/cost.
This is the **same core idea as III2 (edge↔cloud router) in the master catalog**, moved to solvers —
which means the two ideas share machinery and a team member.

**Why it's a good bet:** it is honest about quantum (it will empirically show when the QPU loses, and
that's a publishable result), it's patentable (the routing policy is the invention), and it degrades
gracefully — if quantum never helps, you've built a useful classical portfolio solver, which is a real
and well-regarded research area on its own.

**Build:** Qiskit/PennyLane + free IBM Quantum access + D-Wave free tier + OR-Tools + your GPU.

---

## Q4 — Personal Quantum-Safe Vault (upgrade what you already stored)

**Who uses it:** ordinary people with a decade of photos, documents and chat exports in cloud storage —
exactly the long-retention data HNDL targets. Signal (PQXDH) and iMessage (PQ3) already solved
*messages in transit*; **your 2016 Google Drive backup is still classically encrypted and someone may
already have a copy.**

**The claim:** a re-encryption proxy that upgrades data **at rest** to hybrid PQC without a full
download-decrypt-reupload cycle, maintaining a verifiable **key-rotation lineage** so you can prove
which objects were upgraded when, and recover across rotations. Technical effect: bandwidth/compute cost
of migration, plus recoverability guarantees.

**Build:** liboqs + a storage-provider adapter. Easiest build in Part B, lowest failure risk, moderate
patent strength (prior art around hybrid KEM is dense — the *at-rest lineage* part is where novelty
lives).

---

## Q5 — Learned Error Mitigation / Noise-Aware Layout

ML-driven quantum error mitigation and layout selection is genuinely active (ML-QEM up to 100 qubits,
Q-Cluster, 2026 fidelity-prediction frameworks) and buildable: simulators + free IBM hardware time +
your GPU. **But:** IBM and others are filing hard in exactly this space, so prior-art risk is the worst
of any idea in this document, and the users are quantum researchers, not people. Listed for
completeness — take it only if someone on the team wants a quantum-native career.

## Q6 — Quantum Kernels Where n Is Genuinely Tiny

Rare-disease tabular data, small clinical cohorts — the only regime where quantum kernels aren't
obviously dominated. Claim would be data-dependent feature-map selection to avoid exponential
concentration. **Low confidence:** the 2026 benchmark literature is unkind, and "we tried and it didn't
beat an SVM" is a fine paper but not a product. Do not build your capstone on it.

---

## Quantum ideas to skip (they sound great and aren't)

- **QRNG-as-a-service / quantum entropy for apps.** Free QRNG APIs already exist (qrandom.io,
  TrueEntropy, Quantum Blockchains) and a $35 open-source QRNG shipped in 2026. More importantly,
  entropy is not a real problem — `/dev/urandom` is fine. No user need, no defensible claim.
- **QKD/quantum-network simulators for education.** Fun, well-covered, zero patent, zero users.
- **"Quantum blockchain".** Marketing.
- **VQE drug discovery.** Needs hardware you don't have and advantage that doesn't exist yet.

---

# Part B2 — More quantum ideas (batch 2)

Same three honest lanes as above. Batch 1 covered the migration *scanner* (Q1) and the solver side
(Q2/Q3). This batch goes after the parts of the quantum transition that are **already breaking things
today** — handshake size, boot memory, archival validity, on-chain exposure — plus one quantum-inspired
idea that makes every other project in this repo work better.

## Q7 — Network-Adaptive PQC Authentication (fix the handshake that PQC just broke) ⭐

**The problem is live right now, not in 2030.** ML-DSA-44 signatures are ~2,420 bytes against ECDSA-P256's
64 — up to **34× larger**. A depth-2 chain with two CT SCTs reaches **~17,500 bytes on the wire, a 32×
increase over Ed25519**. Post-quantum handshakes push HTTPS past 10 KB, which **breaks roughly 5% of
connections on real networks**, and adds an extra round trip. And you can't compress your way out:
PQC keys and signatures are **high-entropy data that resists compression**, unlike the repetitive ASN.1
that classical cert compression exploited.

**Who this hurts most:** users on congested, lossy, high-RTT mobile networks — i.e. most of India.
Every extra round trip is a visible stall on a UPI payment or a page load. This is a quantum-caused
problem whose victims are ordinary people on bad networks.

**What's being done:** Let's Encrypt is targeting **Merkle Tree Certificates** in staging late 2026 and
production 2027. MTC shrinks the common case — but it's a one-size decision, not a per-connection one.

**The claim:** make authentication-path selection **adaptive per connection**. The server picks among
{Merkle-tree cert, full PQC chain, cached-cert-ID suppression, intermediate omission} using a predictor
over observed path characteristics (RTT, loss, congestion-window evolution, prior session state) to
minimise expected time-to-first-byte rather than bytes-on-wire — because on a lossy link the two are
*not* the same objective. Claim the selection policy and the client-side hint that feeds it.
Technical effect: TTFB and handshake-success-rate on constrained links. Clean, measurable, unclaimed.

**Build:** pure software. rustls / quic-go / OQS-OpenSSL + `tc netem` for reproducible loss/latency
emulation. Your evaluation table is TTFB and connection-failure-rate vs loss%, which is a paper figure
and a patent exhibit at the same time. **No GPU, no QPU, no dataset to collect** — the fastest idea in
this document to first result.

**Application worth naming in the spec:** the same mechanism under a payments latency budget (UPI must
complete in seconds, sometimes on 2G) — RBI's quantum-safe push and this constraint collide directly.

---

## Q8 — Quantum-Safe Secure Boot for 20-Year Devices (minimal hardware)

**Who uses it:** every smart meter, EV charger, medical device, water pump controller and industrial PLC
being installed *this year* and expected to run until the 2040s — i.e. straight through Q-Day. Consumer
gadgets can wait; **these cannot**, and the literature says exactly that: industrial controllers adopt
PQC earlier because of long lifetimes.

**The named gaps:** PQC signature verification in a bootloader "may consume significantly more memory,
while injecting more delay when initiating execution of the operating system", per stage, on devices
with strict limits on code size, RAM, energy and update bandwidth. Hash-based signatures (LMS/XMSS) are
the conservative choice for boot — and they are **stateful**, which is the real deployment killer:
reuse a one-time key after a power failure mid-update and you've destroyed your security.

**The claim (two parts, either is filable):**
1. **Staged verification with a rollback-safe commit** — verify only the boot-critical stage with a small
   hash-based signature before handing over control, verify the remainder concurrently during early boot,
   and gate the commit so a failed background verification triggers a safe rollback rather than a brick.
   Technical effect: boot latency and peak RAM at equal security.
2. **Power-fail-atomic key-state management for stateful hash signatures** — a durable state protocol that
   makes one-time-key advancement crash-consistent on flash with no battery-backed store.

**Prior art warning:** there is a granted US patent on PQC secure boot (US 12,531,724) — read it before
you draft. Your novelty must live in the staging/rollback or the state-atomicity, not in "use PQC in
secure boot", which is now claimed.

**Hardware:** ESP32-S3 or STM32 dev board, ~₹500–900. Everything else is firmware you write.

---

## Q9 — Archival Signature Renewal at Scale (the 2035 problem, solvable in 2026) ⭐

**The problem in one sentence:** a degree certificate, land record, court filing or medical consent signed
today with RSA/ECDSA becomes **unverifiable-in-principle** the day those algorithms fall — and legal
documents are routinely expected to hold up for **decades**. ETSI's answer (PAdES-B-LT / **B-LTA**) is
periodic **re-timestamping with stronger algorithms** before the old ones weaken. Everyone agrees on the
mechanism; almost nobody has an implementation that scales.

**Who uses it:** universities (every degree ever issued), land registries, hospitals, courts, and at
national scale DigiLocker-class systems. This is a real customer with a real budget and a legal
obligation, not a hypothetical user.

**The naive approach fails on cost:** re-timestamping N documents = N timestamp-authority calls, forever,
compounding every algorithm generation.

**The claim:** amortised renewal. Aggregate a renewal epoch's documents into a Merkle tree, obtain **one**
PQC timestamp over the root, and issue each document a compact inclusion proof plus a **verifiable
chain-of-renewal** linking every epoch back to original signing — so verification cost stays constant and
timestamp cost becomes O(1) per epoch instead of O(N). Add a scheduler that decides *when* each class of
document must be renewed from an algorithm-obsolescence risk model (retention period × current
cryptanalytic margin), so you renew the 30-year land records early and the 2-year receipts never.
Technical effect: cost and scalability of maintaining long-term verifiability. Strong, concrete, and I
could not find it claimed.

**Build:** pure software — a renewal service + verifier library, ETSI PAdES/ASiC profiles, liboqs for the
PQC timestamps. Demo: sign 100k documents, break the "old" algorithm on purpose, show every document
still verifies through the renewal chain. That demo lands.

---

## Q10 — Entanglement-Guided Model Compression (quantum-inspired, runs on your GPU)

**Why this one matters strategically:** it makes *every other idea in this repo* work better. P1, P2, P4
all need a capable model running on-device. Compression is the enabling layer.

**State of play:** Multiverse's CompactifAI claims quantum-inspired tensor-network compression up to
**95% with 2–3% precision loss, 4–12× faster inference**, and tensor-train work on ChatGLM3-6B / LLaMA2-7B
reports ~1.6–1.9× with matching latency gains. **But** a 2026 paper — *Rethinking the Role of Tensor
Decompositions in Post-Training LLM Compression* — is pointedly skeptical, and that skepticism is your
opening: the honest open question is **where** decomposition helps, not whether it exists.

**The claim:** stop allocating ranks uniformly. Use an **entanglement-entropy proxy computed per layer**
(the quantum-information quantity that tensor networks were built around) to decide each layer's bond
dimension — layers whose weight matrices carry low "entanglement" across a given bipartition tolerate
aggressive truncation; high-entanglement layers don't. Then co-optimise with quantisation, since the two
interact. Technical effect: perplexity/accuracy at a fixed memory budget. This is the rare case where the
quantum framing is doing real work rather than decoration.

**Build:** PyTorch + tensorly/quimb, one college GPU, open models. Honest labelling: **no QPU, quantum
*mathematics* on classical hardware** — say it in the abstract's first line.

**Prior-art caution:** Multiverse is a funded company filing in this space. Your claim must be the
*entropy-guided rank allocation*, not tensor compression generally.

---

## Q11 — Verified Natural-Language → Optimization Model

**Who uses it:** the hospital administrator, timetable clerk or logistics coordinator who has a real
scheduling problem and cannot write a QUBO or a CP model. This is the actual adoption bottleneck for
every optimization tool, quantum or classical — the formulation step, not the solve.

**Prior art exists — read it first:** **LLM-QUBO** (arXiv 2509.00099, AAAI Symposium) already does
end-to-end natural-language → QUBO with hybrid Benders decomposition, and NL4OPT preceded it.

**The gap they leave:** correctness. An LLM that silently produces a *plausible but wrong* constraint set
gives you a confident optimal solution to the wrong problem — and the user, by construction, cannot
check it.

**The claim:** counterexample-guided formulation repair. Generate a candidate model, then **verify it
differentially** against an executable oracle (brute force on small instances, or a reference CP-SAT
model generated independently); when they disagree, feed the disagreeing instance back as a
counterexample and repair; iterate to agreement or to an explicit "cannot verify" refusal. Claim the
verification-and-repair loop plus the small-instance generator that makes it tractable. Technical effect:
formulation correctness rate, and a hard guarantee where there was none.

**Build:** pure software. LLM + OR-Tools + a QUBO backend. Pairs naturally with **Q2/Q3** — this becomes
their front door, so a team could take Q3 + Q11 as one coherent project.

---

## Q12 — On-Chain Quantum Exposure Analyzer & Migration Planner

**The numbers are startling and current:** as of **1 March 2026, over 34% of all bitcoin have revealed a
public key on-chain**; ~**6.9M BTC** (including Satoshi-era holdings) sit exposed; Fortune puts **>$2
trillion** in digital assets at risk. **BIP-360 and BIP-361** (Apr 2026) propose phased migration that
would ultimately **freeze coins in wallets that fail to migrate**. Estimates place Q-Day as early as 2030.

**Who uses it:** anyone holding crypto, and every exchange/custodian who must migrate customers.
Unlike most quantum ideas, the user can act *today* and the benefit is immediate.

**The claim:** exposure-aware migration planning. Classify each UTXO into quantum-exposure classes
(pubkey revealed vs hash-protected vs reused address), then compute a **migration schedule that optimises
fee cost against exposure-time**, since consolidating everything at once is expensive and moving nothing
is unsafe — plus detection of the reuse patterns that silently re-expose an already-migrated wallet.
Technical effect: quantified risk reduction per unit fee.

**Build:** pure software, public chain data, no permissions needed. **Caveat:** crypto is a volatile domain
and some examiners react badly to it — pitch it as *asset-custody risk analysis*, not as a crypto project.

---

## Q13 — Quantum-Inspired Anomaly Detection (only if you want it, and it's crowded now)

MERA/tensor-network autoencoders for unsupervised anomaly detection landed in **April 2026**
(arXiv 2604.06541), benchmarked against dense autoencoders, and hybrid quantum-classical autoencoders for
network intrusion detection exist too. The inductive-bias story is real, but you'd be arriving second into
a field that is currently publishing fast. Take it only as a **fallback** if another idea stalls.

## Q14 — Magnetic-Anomaly Navigation Software (hardware-gated — read the caveat)

**Tempting because the software gap is precisely stated:** MagNav is passive and unjammable, but is
"limited by magnetometer stability and **platform magnetic interference, which can be 1,000 times greater
than the target magnetic anomaly magnitudes**" — a source-separation problem, which is a software problem.
SandboxAQ ships AQNav commercially; SBQuantum flew a diamond magnetometer in 2026.

**Why I'm not recommending it:** the quantum part needs an actual quantum magnetometer you don't have.

**The version you *can* build, honestly labelled:** indoor GPS-denied positioning using the **phone's own
magnetometer** + IMU, exploiting building magnetic anomalies as a fingerprint. That is **not quantum** —
don't dress it up — but it's real, useful, and it pairs beautifully with **P4**: indoor wayfinding for
blind users inside hospitals, malls and metro stations, where GPS dies and no accessible map exists.
File that under Part A if you want it.

---

## Quantum ideas to skip (batch 2 additions)

- **"Build a QKD link."** Needs photonics hardware and a dark fibre. Not a software capstone.
- **Quantum-enhanced federated learning.** Two unproven things multiplied together.
- **Quantum advantage demonstrations / benchmarking suites.** You will be outgunned by national labs.
- **Anything requiring >30 noiseless qubits to show a result.** Simulators cap out; free hardware is noisy.

---

# Part C — Ranking matrix

Scores 1–5, higher = better. **Patent** = strength of a claimable non-obvious technical mechanism under
CRI 2025. **Users** = will real people use it repeatedly. **Prior⁻** = low prior-art/crowding risk
(5 = open field, 1 = Google already ships it). **HW** = 5 pure software, 3 cheap sensor/phone, 1 special hardware.

| ID | Idea | Feas | Patent | Users | Prior⁻ | Data | HW | Demo | Risk⁻ | Tier |
|----|------|:----:|:------:|:-----:|:------:|:----:|:--:|:----:|:-----:|:----:|
| P4 | Runtime accessibility repair ⭐ | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | **S** |
| Q1 | Crypto-agility copilot ⭐ | 4 | 5 | 4 | 3 | 5 | 5 | 3 | 4 | **S** |
| Q7 | Network-adaptive PQC auth ⭐ | 5 | 5 | 4 | 4 | 5 | 5 | 3 | 5 | **S** |
| P2 | Scam interception at payment ⭐ | 3 | 5 | 5 | 3 | 3 | 4 | 5 | 3 | **S** |
| Q9 | Archival signature renewal ⭐ | 4 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | **S** |
| P10 | Counterfeit medicine PUF scan ⭐ | 4 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | **S** |
| P14 | Hands-free blind wayfinding ⭐ | 4 | 5 | 4 | 4 | 4 | 4 | 5 | 4 | **S** |
| P1 | Prescription safety net | 4 | 4 | 5 | 3 | 3 | 5 | 4 | 3 | **A** |
| P11 | Stampede early warning | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 3 | **A** |
| P13 | Hinglish consultation scribe | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | **A** |
| P12 | Milk/oil adulteration test | 4 | 4 | 4 | 4 | 3 | 3 | 5 | 4 | **A** |
| P15 | Speech restoration, atypical | 3 | 4 | 4 | 3 | 2 | 4 | 5 | 3 | **A** |
| P8 | Deepfake video-call verifier | 3 | 5 | 4 | 4 | 3 | 4 | 5 | 3 | **A** |
| Q8 | PQC secure boot, 20-yr devices | 4 | 4 | 4 | 3 | 4 | 3 | 4 | 4 | **A** |
| P5 | Appliance-level bill breakdown | 4 | 4 | 4 | 3 | 5 | 3 | 4 | 4 | **A** |
| Q3 | Per-instance solver router | 4 | 5 | 3 | 4 | 4 | 4 | 3 | 4 | **A** |
| Q11 | Verified NL → optimization model | 4 | 4 | 4 | 3 | 4 | 5 | 4 | 4 | **A** |
| P7 | Camera-free fall detection | 3 | 4 | 4 | 4 | 3 | 3 | 5 | 3 | **A** |
| Q10 | Entanglement-guided compression | 3 | 4 | 4 | 3 | 5 | 4 | 3 | 3 | **A** |
| P6 | DPDP consent + erasure toolkit | 4 | 3 | 3 | 3 | 5 | 5 | 2 | 4 | **B** |
| Q4 | Personal quantum-safe vault | 5 | 3 | 3 | 3 | 5 | 5 | 3 | 5 | **B** |
| Q2 | Tensor-network scheduler | 3 | 4 | 3 | 4 | 4 | 4 | 3 | 3 | **B** |
| Q12 | On-chain exposure analyzer | 4 | 4 | 3 | 4 | 5 | 5 | 3 | 4 | **B** |
| P9 | Road hazard mapper | 4 | 3 | 3 | 2 | 4 | 4 | 4 | 4 | **B** |
| P3 | Two-way Indian Sign Language | 2 | 4 | 5 | 4 | 2 | 4 | 5 | 2 | **B** |
| P16 | Two-wheeler collision warning | 3 | 3 | 5 | 2 | 3 | 4 | 5 | 3 | **B** |
| P17 | Anemia screening from photo | 4 | 2 | 4 | 1 | 3 | 5 | 4 | 4 | **B** |
| Q13 | Tensor-network anomaly detection | 3 | 3 | 3 | 2 | 4 | 4 | 2 | 3 | **C** |
| Q5 | Learned error mitigation | 3 | 3 | 2 | 2 | 4 | 4 | 2 | 3 | **C** |
| Q6 | Quantum kernels, tiny-n | 3 | 3 | 2 | 3 | 4 | 4 | 2 | 2 | **C** |
| Q14 | Magnetic-anomaly navigation | 2 | 4 | 3 | 4 | 2 | 1 | 4 | 2 | **C** |

---

# Part D — Verdict

**If you want one project that is patentable, used by real people, and cannot really fail:**
**P4 (runtime accessibility repair)**. Cleanest claim in the document, no dataset to collect, pure
software, and blind users will tell you within a week whether it works.

**If you want the strongest patent + a customer who is already shopping:** **Q1 (crypto-agility
copilot)**. A regulator has set the deadline for you. Zero dependence on quantum hardware ever working.

**If you want the fastest path from zero to a real number (quantum track):** **Q7 (network-adaptive PQC
authentication)**. No dataset, no GPU, no QPU, no hardware — just a TLS stack and a network emulator.
The problem already breaks ~5% of connections today, so you're fixing something that's currently broken
rather than something that might break in 2030.

**If you want a quantum-track project with a paying customer inside your own college:** **Q9 (archival
signature renewal)**. Your university issues degree certificates that must verify in 2050. Ask the
registrar.

**If you want maximum "this helped someone" and the best demo:** **P2 (scam interception)**. It stops a
real crime in front of the examiner. Hardest engineering, highest reward, and it targets a gap Google's
own 2026 feature structurally cannot cover.

**If the demo is what you're optimising for:** **P10 (counterfeit medicine)**. Two identical strips, one
scan, a verdict — no internet, no setup, examiner holds the phone. It also has the cleanest story of any
idea here: the government's own QR mandate (July 2027) authenticates the *data* on a pack, and a
counterfeiter can copy data; only the object's own microstructure can't be copied. Runner-up on demo alone
is **P14** (blindfolded examiner navigates a building), which pairs with **P4** into one project about
independence indoors — the strongest two-idea combination in this repo.

**Best combination for a 3-person team:** P2 as the product + Q1 as the second workstream is
over-ambitious. Better: **pick one from {P4, Q1, P2}, and use Q3 as the second-semester extension** if
you want the quantum angle on the same paper — Q3's router shares its core with III2 in the master
catalog, so it plugs into work you've already scoped.

**Ordering that protects both goals:** build → measure the technical effect (you need the numbers for
both the claim and the paper) → **file the provisional** → then publish, demo, and open-source.

---

## Sources

Patentability: [CRI Guidelines 2025 analysis](https://www.mondaq.com/india/patent/1663246/a-detailed-analysis-of-indias-new-cri-guidelines-2025) ·
[Intepat §3(k) guide](https://www.intepat.com/blog/cri-guidelines-2025-patent-india-3k) ·
[Decoding §3(k), CNLU](https://www.cnlu.ac.in/wp-content/uploads/2026/01/Decoding-Section-3k-The-Evolving-Landscape-for-Software-and-AI-Patent.pdf)

Quantum reality: [QML reality check 2026](https://postquantum.com/quantum-ai/quantum-machine-learning-reality/) ·
[Quantum kernels under scrutiny](https://link.springer.com/article/10.1007/s42484-025-00273-5) ·
[QKSVM vs classical benchmark](https://arxiv.org/pdf/2604.18837) ·
[Quantum-inspired tensor networks in industry](https://arxiv.org/html/2404.11277v2) ·
[Knapsack/shortest-path via tensor networks](https://arxiv.org/pdf/2506.11711)

PQC handshake/boot/archival: [PQ signature sizes breaking TLS](https://redsift.com/blog/post-quantum-signature-sizes) ·
[Let's Encrypt Merkle Tree Certificates](https://www.techtimes.com/articles/317788/20260604/post-quantum-tls-certificates-lets-encrypt-plans-merkle-tree-rollout-that-shrinks-handshakes.htm) ·
[PQ cert chain impact on TTFB](https://arxiv.org/html/2604.24869v1) ·
[Why IoT is the hardest place to deploy PQC](https://medium.com/@mahad.aqeel7/post-quantum-cryptography-why-iot-is-the-hardest-place-to-deploy-it-6eaf09aa2a1a) ·
[Hash-based signatures for IoT secure boot](https://www.sciencedirect.com/science/article/abs/pii/S2214212626000918) ·
[US 12,531,724 — PQC for secure boot](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12531724) ·
[Post-quantum digital signatures & archival validity](https://postquantum.com/post-quantum/post-quantum-digital-signatures/) ·
[PQ-resilient audit evidence for long-lived systems](https://arxiv.org/pdf/2512.00110)

Quantum-inspired & other: [Rethinking tensor decompositions for LLM compression](https://arxiv.org/pdf/2606.03465) ·
[Saten: sparse augmented tensor networks](https://arxiv.org/pdf/2505.14871) ·
[CompactifAI / quantum-inspired compression](https://www.computing.co.uk/interview/2025/how-to-tame-llms-with-quantum-inspired-compression) ·
[LLM-QUBO](https://arxiv.org/abs/2509.00099) ·
[MERA tensor-network autoencoders for anomaly detection](https://arxiv.org/abs/2604.06541) ·
[BIP-361 post-quantum migration](https://bips.dev/361/) ·
[$2T digital assets at risk](https://fortune.com/2026/08/15/quantum-computing-migration-2-trillion-digital-assets-risk-crypto-market-bitcoin/) ·
[Quantum sensors for positioning & navigation](https://link.springer.com/article/10.1007/s10291-026-02030-y)

PQC: [India's quantum-safe roadmap 2027–29](https://postquantum.com/security-pqc/indias-quantum-safe-roadmap/) ·
[RBI Q-SAFE committee](https://www.whalesbook.com/news/English/bankingfinance/RBI-Assembles-Panel-to-Tackle-Quantum-Computing-Threats-to-Banking-Security/6a14e783b979113840cab662) ·
[RBIH banking whitepaper](https://rbih-website-assets.s3.ap-south-1.amazonaws.com/resources/whitepaper-on-securing-indian-banks-in-the-age-of-quantum-computing.pdf) ·
[CBOM tooling gaps](https://quantumsecuritydefence.com/insights/automated-cryptographic-discovery-tools-pqc/)

Batch-2 products: [India's QR mandate on medicines](https://www.outlookindia.com/national/outlook-explains-how-indias-new-qr-code-system-will-help-you-spot-fake-medicines) ·
[AI vs counterfeit drugs in India](https://www.ijpsjournal.com/article/unmasking-counterfeit-medicines-the-role-of-ai-in-strengthening-india-s-drug-safety) ·
[Inkjet-printed PUFs (Small, 2026)](https://onlinelibrary.wiley.com/doi/10.1002/smll.202514908) ·
[Counterfeit detection from paper texture by mobile camera](https://www.researchgate.net/publication/316173184_Counterfeit_Detection_Based_on_Unclonable_Feature_of_Paper_Using_Mobile_Camera) ·
[Crowd monitoring / stampede early warning (YOLOv8m + CNN-LSTM)](https://ijcttjournal.org/archives/ijctt-v74i6p102) ·
[Rethinking safety at mass gatherings in India (ORF)](https://www.orfonline.org/expert-speak/human-flow-systemic-flaws-rethinking-safety-at-mass-gatherings-in-india) ·
[Crowd risk prediction](https://www.sciencedirect.com/science/article/abs/pii/S0925753522002168) ·
[Smartphone colorimetry for milk adulterants](https://www.sciencedirect.com/science/article/pii/S0026265X20302952) ·
[Paper-based milk adulteration sensor](https://www.researchgate.net/publication/365343821_A_novel_and_low-cost_smartphone_integrated_paper-based_sensor_for_measuring_starch_adulteration_in_milk) ·
[Hinglish medical ASR + diarization (DISPLACE-M)](https://arxiv.org/pdf/2603.06373) ·
[HiACC Hinglish code-switched corpus](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12329218/) ·
[Indoor wayfinding for blind travelers](https://news.ucsc.edu/2024/10/manduchi-wayfinding-apps/) ·
[Lightweight localization for BVI travelers](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10007266/) ·
[CLARIS: intelligible speech from dysarthric voices (CHI 2026)](https://dl.acm.org/doi/10.1145/3772318.3791734) ·
[Few-shot dysarthric personalization](https://arxiv.org/pdf/2509.15516) ·
[AnemiaVision](https://arxiv.org/pdf/2604.22964) ·
[Fingernail-photo hemoglobin (Nature Comms)](https://www.nature.com/articles/s41467-018-07262-2)

Products: [Google fake-call detection](https://blog.google/security/android-fake-call-detection/) ·
[Real-time deepfake detection gap](https://www.adaptivesecurity.com/blog/deepfake-detection-tools-defined) ·
[Assistive tech adoption/abandonment](https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1719746/full) ·
[iSign ISL benchmark](https://exploration-lab.github.io/iSign/) ·
[NILM 2026 review](https://dl.acm.org/doi/10.1145/3814607) ·
[WiFi CSI fall detection](https://www.originwirelessai.com/wp-content/uploads/2024/04/DeFall.pdf) ·
[DPDP Rules timeline](https://www.techprescient.com/blogs/dpdp-act-rules/) ·
[Digital prescriptions / medication error](https://unidoc.in/blog/digital-prescriptions-reducing-medication-errors)
