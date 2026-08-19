# IDP — "Holy Shit You Built That" Ideas

Third track, different filter. `IDP-MASTER-CATALOG.md` optimises for a paper.
`IDP-PRODUCT-IDEAS.md` optimises for a patent and real users. **This file optimises for awe** —
the projects that make someone say *"wait, you built that from scratch?"*

Novelty is explicitly **not** required here. Nobody needs a new operating system. Building one
anyway is the point.

> **Read this before you pick from this file.** These projects are *impressive*, not *novel*.
> Most will not produce a publishable paper or a patent. If your college requires either, do one of:
> (a) pick an idea below that has a research seam — **H3**, **H7**, **H8** all do, and I've marked
> where; (b) run a from-scratch build as the engineering artefact and a Section-B idea as the paper;
> or (c) accept the trade knowingly. Don't discover this in month nine.
>
> **The real killer here is scope, not difficulty.** Every idea below can eat the entire year.
> Define your **minimum shippable flex** in week one — the smallest version that still earns the
> reaction — and treat everything beyond it as a stretch goal.

Compiled 2026-08-19.

---

## How to read the ranking

Scores 1–5, higher is better. Same style as the master catalog, different criteria — because
"publishability" is not what you're buying here.

| Criterion | Meaning |
|---|---|
| **Awe** | The "holy shit" reaction. The whole reason this file exists. |
| **Feas** | Can 3 people + Claude Code actually finish it in a year? |
| **Demo** | How good the live demo is |
| **Depth** | How much real engineering you learn — the interview/résumé payload |
| **Cheap** | Low cost (5 = free/laptop; 1 = serious money) |
| **Split** | How cleanly the work divides across 3 people without blocking each other |
| **Risk⁻** | Low failure risk (5 = will definitely work; 1 = might have nothing on demo day) |

---

# The ideas

## H1 — Silicon to Snake: the entire computer, from scratch ⭐

**The flex:** *"We designed our own CPU, built it in hardware, wrote an assembler and a C compiler
for it, wrote an operating system that runs on it — and it plays a game."*

Nothing else in this document lands harder. It is the complete stack, and every layer is yours:

1. **Your own instruction set** (or RV32I, so you get an existing toolchain to check yourself against)
2. **The CPU in Verilog**, running on an FPGA — real hardware, not a simulator
3. **An assembler**, then a **C compiler** targeting your ISA
4. **An OS**: bootloader, interrupts, scheduler, memory, a shell
5. **A game** on top, running on your computer

**Why it's feasible, specifically:** *FemtoRV* is a documented RV32I core in **~400 lines of Verilog**
that fits in **under 1,280 LUTs** — small enough for a Lattice IceStick. There is teaching material
built around FPGA + RISC-V at roughly **$40 per student**. You are not starting from a blank page;
you're starting from a known-good reference you can read, understand, and then beat.

**Why it splits perfectly across 3 people** (rare, and the reason I rank it first): hardware
(CPU/FPGA) · toolchain (assembler/compiler) · systems (OS/game). Three genuinely separate workstreams
with one clean interface between them — the ISA spec — so nobody blocks anybody. Agree the ISA in
week two and you can work in parallel for months.

**Minimum shippable flex:** CPU runs on FPGA + assembler + a program you wrote in your own assembly
executing on it. Everything after that is upside.

**Cost:** ₹3,000–8,000 for an FPGA board. Toolchain (yosys/nextpnr) is free and open source.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 3 | 5 | 5 | 4 | 5 | 3 |

---

## H2 — Tape out a real chip (bolt this onto H1)

**The flex:** you hold up a physical piece of silicon and say *"we designed this."* Not an FPGA
emulating your design — an actual fabricated chip with your logic on it.

**This is real and affordable.** Tiny Tapeout runs shuttles that put student designs on open-source
ASIC processes, with workshops starting around **€150**.

**⚠️ The schedule is the whole story — check it before you commit.** Fabrication takes the better
part of a year:

| Shuttle | Closes | Chips expected | Delivered |
|---|---|---|---|
| TTSKY26c | 2026-09-07 | 2027-03-27 | 2027-05-12 |
| TTIHP26b | 2026-09-21 | 2027-06-25 | 2027-08-16 |

So: **submit by early September 2026 and silicon lands around May 2027** — inside a year-long project
starting now, but only if you submit in the next few weeks. Miss that window and your chip arrives
after you graduate.

**Therefore: never make this the critical path.** Do H1 on the FPGA as the real project, submit the
same core to a shuttle as a parallel bet, and if the chip arrives in time it becomes the most
memorable slide in the presentation. If it doesn't, you lose nothing.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 4 | 4 | 4 | 3 | 2 | 2 |

---

## H3 — Train your own LLM from scratch (has a research seam)

**The flex:** *"We didn't fine-tune anything. We built the tokenizer, pretrained the base model,
did the instruction tuning, wrote the inference server, and this chat window is talking to our
weights."*

**Grounded:** Karpathy's **nanochat** trains a **~1.9B-parameter** model on **~38B tokens** — a
GPT-2-grade model, full pipeline from tokenisation through pretraining, fine-tuning and deployment —
for roughly **$100** and a few hours on an 8×H100 node. On a single GPU it's slower but the pipeline
is identical, and you have a college GPU. **The recipe is public; the engineering is still yours.**

**The research seam — take it, it costs nothing:** pretrain on a corpus that no open model has been
trained on, e.g. a genuinely native (not translated) corpus in an Indian language. Suddenly you have
a defensible contribution *and* the flex, and the evaluation writes itself: your model vs. comparable
open models on that language. This is the one idea here that upgrades to a paper for free.

**Minimum shippable flex:** your own tokenizer + a pretrained base model that produces coherent text
+ a chat UI. Instruction tuning and RLHF are stretch goals.

**Watch out for:** data cleaning will consume more time than training. Budget for it.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 4 | 5 | 3 | 4 | 3 |

---

## H4 — An operating system that boots on real hardware

**The flex:** plug a USB stick into a *real laptop*, reboot it, and your OS comes up. Not QEMU.
The examiner's expectations reset the moment they see it boot on metal.

**Scope:** bootloader → protected/long mode → interrupts → physical and virtual memory → preemptive
scheduler → syscalls → a filesystem → a shell → a couple of userspace programs. Stretch: a TCP/IP
stack, or a window system.

**Why it's more approachable than it sounds:** this is the best-documented hard project in computing
(OSDev wiki, xv6, Writing an OS in Rust). Target **RISC-V** rather than x86 if you also do H1 — then
your OS runs on *your own CPU*, and H1 + H4 become one unified project instead of two.

**Minimum shippable flex:** boots on real hardware, multitasks, has a shell you can type into.

**Risk to manage:** debugging without a debugger is the tax. Get serial-port logging working in
week one — everything after that is tractable, and nothing before it is.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 3 | 5 | 5 | 5 | 4 | 3 |

---

## H5 — Your own distributed database (best demo-to-risk ratio here)

**The flex:** *"We wrote our own Postgres."* Storage engine (B-tree or LSM), write-ahead log, MVCC
transactions, a SQL parser and query planner, and **Raft replication** across nodes.

**The demo is the selling point and it's genuinely dramatic:** run a cluster on three laptops, start
a workload, then **physically kill a node mid-transaction**. The cluster elects a new leader, keeps
serving, and when the dead node rejoins it catches up. Nothing is lost. Then pull the power on the
leader and do it again. Examiners remember this.

**Why I rank it as the safest big build:** it degrades gracefully. A single-node database with
transactions and SQL is already a serious project; Raft on top is the flex. If replication runs late,
you still have something complete to show — which is not true of H4 or H6.

**Splits cleanly:** storage engine · query layer · consensus/replication.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 5 | 5 | 5 | 5 | 4 |

---

## H6 — A browser engine from scratch

**The flex:** your own HTML parser, CSS cascade and layout engine, JavaScript interpreter, and
renderer — and it displays a real website.

**Highest awe-per-line-of-code of anything here**, because everyone in the room has an intuition for
how complicated a browser is. Ladybird proved a from-scratch engine is possible outside a mega-corp.

**But be honest about the risk:** CSS layout is a swamp — floats, flexbox, and the cascade will eat
months, and "renders *most* pages *mostly* right" is the realistic year-one outcome. The JS
interpreter alone is a full project (which is why H10 exists as its own entry).

**Only take this if** you scope it hard: pick **ten target pages** in week one, make those render
correctly, and demo exactly those. A browser that renders ten pages beautifully beats one that
renders everything badly.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 2 | 5 | 5 | 5 | 4 | 2 |

---

## H7 — A real-time path tracer (has a research seam)

**The flex:** physically-correct light simulation — real reflections, soft shadows, global
illumination — running at 60fps, written by you, no game engine.

**The prettiest demo in this document.** Path tracing is trivially explainable ("we simulate actual
light rays") and immediately, obviously beautiful. Move the camera, watch the lighting respond.

**The technical core:** GPU path tracing (CUDA/Vulkan compute), BVH acceleration, importance
sampling, and — the part that makes real-time possible — **a denoiser**, because a real-time budget
buys you only a handful of samples per pixel and the raw output is pure noise.

**The research seam:** this shares its entire stack with **P18 (NeuroRender)** in
`IDP-PRODUCT-IDEAS.md`. Build the path tracer, then use it as your own ground-truth data generator
for neural reconstruction — you control the renderer, so you can emit perfect motion vectors, depth
and reference frames. That turns a flex project into a research pipeline.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 5 | 4 | 4 | 3 | 3 |

---

## H8 — Build a satellite ground station and pull images out of the sky ⭐ (cheapest awe here)

**The flex:** *"We built this antenna out of copper wire, pointed it at the sky, and this is a
photograph of India that we downloaded directly from a satellite."* People do not expect this to be
possible with hobby equipment. It is.

**Cost: about ₹3,000.** RTL-SDR dongle (~₹2,500) + a hand-built V-dipole or QFH antenna (~₹500 of
copper wire and PVC).

**⚠️ Critical 2026 correction — every old tutorial you'll find is out of date.** The NOAA APT
satellites everyone used are **dead**: NOAA-15, the last one transmitting APT, was decommissioned on
**19 August 2025**. Do not build for APT. The live target is **Meteor-M** LRPT — **Meteor-M2-4** is
the current beginner target, also around **137 MHz**, and at **1 km/pixel it's four times sharper**
than the APT it replaced. SatDump handles receive/decode/process.

**Where the depth is** (and how to avoid this being a shopping exercise): **write your own decoder.**
Take the raw IQ samples and do the DSP yourself — Doppler correction, QPSK demodulation, Viterbi,
Reed-Solomon, image assembly — using SatDump only to check your output. That's a real signal-
processing project, and the flex becomes *"we decoded it ourselves."*

**The research seam:** feeds **V1 (satellite remote sensing)** in the master catalog. Your own ground
station providing your own imagery is a genuinely uncommon capstone asset.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 4 | 5 | 4 | 5 | 3 | 3 |

---

## H9 — Run your own mobile network ⚠️ (read the legal warning)

**The flex:** a phone in the room shows *your* network name in its signal bar, and places a call
through hardware sitting on the table.

**Stack:** srsRAN or Open5GS + an SDR (USRP/LimeSDR/BladeRF) + programmable SIM cards.

**⚠️ Legal warning, and this one is not negotiable.** Transmitting on licensed cellular spectrum
without authorisation is **illegal in India** (WPC/Department of Telecommunications) and essentially
everywhere else. It is also genuinely dangerous — you can disrupt emergency calls. If you build this,
you must do it **inside a shielded RF enclosure / Faraday cage**, or under your institution's
experimental licence with a faculty member formally responsible. **Get that in writing before you
buy hardware.** A capstone that ends in a regulatory complaint is not a good capstone.

**Cost:** ₹40,000–1,00,000 for a decent SDR, plus the shielding. The most expensive idea here.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 3 | 5 | 4 | 2 | 3 | 2 |

---

## H10 — A self-hosting compiler for your own language

**The flex:** *"This compiler is written in the language it compiles."* You compile the compiler
**with itself**, live, and the output is byte-identical. Programmers in the room understand instantly
what that means; the bootstrap is a genuinely beautiful thing to watch.

**Scope:** lexer → parser → type checker → IR → optimiser → native code generation (x86-64/ARM64, or
your own ISA from H1). Then rewrite the compiler in your own language and bootstrap it.

**Why it's underrated:** it is much more tractable than H4 or H6 — the problem is well-bounded, the
theory is well-documented, and progress is continuous and visible rather than all-or-nothing. Good
choice if you want the flex without betting the year on a debugging nightmare.

**Minimum shippable flex:** a language that compiles to native code and runs real programs.
Self-hosting is the stretch — and it's the part that gets the reaction.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 4 | 5 | 5 | 4 | 4 |

---

## H11 — A search engine over a real corpus

**The flex:** your own crawler, your own inverted index, your own ranking — searching tens of millions
of real pages, returning results in under 100 ms, on hardware you can point at.

**Where the engineering actually is** (and it's more than people expect): a polite distributed
crawler, index compression, a query engine that isn't a linear scan, and ranking that doesn't
embarrass you. Add semantic/vector search alongside keyword and you have a hybrid engine that beats
a naive baseline you can measure against.

**Demo:** search something obscure, get a better result than you expected, show the latency counter.
Bootstrap on a Common Crawl segment or all of Wikipedia rather than crawling the open web from zero.

**Splits beautifully:** crawler/storage · index/query engine · ranking/UI.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 4 | 4 | 3 | 5 | 3 |

---

## H12 — An emulator that boots real Linux

**The flex:** you wrote a CPU emulator from scratch, and an **unmodified Linux kernel boots on it**
and gives you a shell. Every instruction, the MMU, the interrupt controller, the devices — all yours.

**Why it's a great capstone despite sounding insane:** the target is *unambiguous* and self-checking.
Linux either boots or it doesn't, and the boot log tells you exactly which instruction you got wrong.
You are never guessing whether you're making progress. RISC-V is dramatically easier than x86 here,
and it composes with H1 — emulator first, then the same ISA in hardware.

**Minimum shippable flex:** boots to a shell. That's the whole demo, and it's enough.

| Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 3 | 4 | 5 | 5 | 3 | 3 |

---

## Honourable mentions (real flexes, one notch below)

- **Mind-controlled interface** — cheap EEG headset, motor-imagery classification, control a game.
  Awe 5, but signal quality on consumer EEG is poor and it may simply not work reliably. Cost ₹15k–40k.
- **Autonomous RC car** — perception + planning + control on a real vehicle racing a track. Great demo,
  but it's a hardware project wearing a software costume; mechanical failures will eat your time.
- **Your own Git** — content-addressed store, branching, merging, a real merge algorithm. Excellent
  depth, modest awe (people underestimate it because they use it daily).
- **Your own TCP/IP stack** in userspace, talking to real internet hosts. Same profile as above.
- **A ray-traced game console**: H1 + H7 — your CPU, your renderer, your game. Absurd, magnificent,
  probably too much for one year.

---

# Ranking matrix

| ID | Idea | Awe | Feas | Demo | Depth | Cheap | Split | Risk⁻ | Tier |
|----|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| H1 | Silicon to Snake (whole computer) ⭐ | 5 | 3 | 5 | 5 | 4 | 5 | 3 | **S** |
| H5 | Distributed database + Raft | 4 | 4 | 5 | 5 | 5 | 5 | 4 | **S** |
| H8 | Satellite ground station ⭐ | 5 | 4 | 5 | 4 | 5 | 3 | 3 | **S** |
| H4 | OS booting on real hardware | 5 | 3 | 5 | 5 | 5 | 4 | 3 | **S** |
| H3 | LLM from scratch | 4 | 4 | 4 | 5 | 3 | 4 | 3 | **A** |
| H10 | Self-hosting compiler | 4 | 4 | 4 | 5 | 5 | 4 | 4 | **A** |
| H7 | Real-time path tracer | 4 | 4 | 5 | 4 | 4 | 3 | 3 | **A** |
| H11 | Search engine | 4 | 4 | 4 | 4 | 3 | 5 | 3 | **A** |
| H12 | Emulator that boots Linux | 4 | 3 | 4 | 5 | 5 | 3 | 3 | **A** |
| H2 | Tape out a real chip | 5 | 4 | 4 | 4 | 3 | 2 | 2 | **B** |
| H6 | Browser engine | 5 | 2 | 5 | 5 | 5 | 4 | 2 | **B** |
| H9 | Private mobile network ⚠️ | 5 | 3 | 5 | 4 | 2 | 3 | 2 | **C** |

Tier here weights **Awe × Feasibility × Risk⁻** — an idea you don't finish scores zero on demo day,
which is why H6 and H9 sit below their awe.

---

# Verdict

**If you want the single biggest reaction:** **H1 (Silicon to Snake)**, with **H4** folded in so the
OS runs on your own CPU. It's the only idea here that splits perfectly three ways, it's cheap, and
"we built the whole computer" is a sentence nobody else in your cohort will be saying. Submit the
same core to a **Tiny Tapeout shuttle by early September 2026** (H2) as a free side bet — if the
silicon lands in May 2027, you close your presentation by holding up a chip.

**If you want maximum impressiveness per unit risk:** **H5 (database + Raft)**. Killing a node live
and watching the cluster survive is the best demo-to-risk ratio in this file, and it degrades
gracefully if you run out of time.

**If you want the cheapest possible awe:** **H8 (ground station)**. ₹3,000 and a hand-built antenna
gets you a photograph you pulled out of the sky yourself. Just build for **Meteor-M LRPT, not NOAA
APT** — APT died in August 2025 and most tutorials online haven't caught up.

**If you need the flex *and* a paper:** **H3** (pretrain on a language nobody has covered),
**H7 → P18** (renderer as your own ground-truth generator), or **H8 → V1** (your ground station
feeding the satellite-analysis project). These are the three that pay both bills.

**What I'd actually do with 3 people and a year:** H1 + H4 as the core build (hardware / toolchain /
OS split three ways), H2 submitted early as a lottery ticket, and one Section-B idea running
alongside as the publishable component. That gets you the reaction, the silicon, and the paper.

---

## Sources

[FemtoRV / learn-fpga (RV32I in ~400 lines)](https://github.com/filipkosecek/learn-fpga) ·
[RISC-V development boards 2026](https://lucaberton.com/blog/risc-v-development-boards-2026-guide/) ·
[Tiny Tapeout shuttles & schedule](https://tinytapeout.com/chips/) ·
[Tiny Tapeout for universities](https://tinytapeout.com/teaching/) ·
[nanochat](https://github.com/karpathy/nanochat) ·
[nanochat — train your own LLM for ~$100](https://dig.watch/updates/train-your-own-language-model-for-100-with-nanochat) ·
[NOAA 15/18/19 end of life](https://www.rtl-sdr.com/noaa-15-18-19-end-of-life-announcement-but-transmissions-will-continue-for-hobbyists/) ·
[RTL-SDR weather satellite reception in 2026 — what still works](https://www.sdrstore.eu/rtl-sdr-weather-satellite-reception-2026-what-still-works/) ·
[Meteor-M LRPT decoding tutorial](https://www.rtl-sdr.com/rtl-sdr-tutorial-decoding-meteor-m2-weather-satellite-images-in-real-time-with-an-rtl-sdr/)
