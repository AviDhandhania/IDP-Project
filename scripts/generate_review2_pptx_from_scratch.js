
const pptxgen = require('pptxgenjs');
const path = require('path');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// -------------------------------------------------------------
// Core Theme & Formatting Constants
// -------------------------------------------------------------
const BG_DARK = 'F8FAFC';
const CARD_BG = 'FFFFFF';
const BORDER_COLOR = 'E2E8F0';
const TEXT_WHITE = '0F172A';
const TEXT_BODY = '334155';
const TEXT_MUTED = '64748B';
const ACCENT_BLUE = '2563EB';
const ACCENT_GREEN = '059669';
const ACCENT_RED = 'DC2626';

const TOTAL_SLIDES = 25;

function addSlideBase(pres, slideNum, sectionName, title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: BG_DARK };
  slide.addShape(pres.ShapeType.line, { x: 0.5, y: 0.68, w: 9.0, h: 0, line: { color: BORDER_COLOR, width: 1 } });
  slide.addText('CRYPTO-AGILITY NAVIGATOR', { x: 0.5, y: 0.35, w: 5.5, h: 0.25, fontSize: 9, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 1.5 });
  slide.addText(sectionName.toUpperCase(), { x: 5.0, y: 0.35, w: 4.5, h: 0.25, fontSize: 9, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true, tracking: 1.5 });
  slide.addText(title, { x: 0.5, y: 0.85, w: 9.0, h: 0.3, fontSize: 12, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 1.2 });
  slide.addText(subtitle, { x: 0.5, y: 1.15, w: 9.0, h: 0.45, fontSize: 18, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  slide.addShape(pres.ShapeType.line, { x: 0.5, y: 5.15, w: 9.0, h: 0, line: { color: BORDER_COLOR, width: 1 } });
  slide.addText(sectionName.toUpperCase(), { x: 0.5, y: 5.25, w: 6.5, h: 0.25, fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, bold: true });
  const numStr = `${String(slideNum).padStart(2, '0')} / ${TOTAL_SLIDES}`;
  slide.addText(numStr, { x: 7.5, y: 5.25, w: 2.0, h: 0.25, fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true });
  return slide;
}

// -------------------------------------------------------------
// TITLE SLIDE
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  slide.background = { color: BG_DARK };
  slide.addText('CRYPTO-AGILITY NAVIGATOR', { x: 1.0, y: 1.8, w: 8.0, h: 0.6, fontSize: 32, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
  slide.addText('Dataflow-Aware Cryptographic Inventory and Prioritised Post-Quantum Migration', { x: 1.0, y: 2.5, w: 8.0, h: 0.8, fontSize: 18, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  slide.addText([
    { text: 'Avi Dhandhania (25BCE1207)  |  Anmol Saluja (25BCE1332)  |  Avika Tyagi (25BCE1294)\n', options: { bold: true, color: TEXT_BODY } },
    { text: 'Guide: Dr. E INIYA NEHRU (54128), SCOPE\n', options: { color: TEXT_MUTED } },
    { text: 'VIT Chennai Campus | Innovative Design Project | BACSE291', options: { color: TEXT_MUTED } }
  ], { x: 1.0, y: 4.0, w: 8.0, h: 1.0, fontSize: 12, fontFace: 'Arial', lineSpacing: 20 });
}

{
  const s = addSlideBase(pres, 2, "1. Executive Summary", "1.1 THE TECHNICAL PROBLEM", "The Unsolved Engineering Challenge");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Every enterprise software system depends on cryptography it cannot reliably enumerate or sequence for migration. A typical mid-sized banking or healthcare application invokes RSA, ECDSA, AES and SHA-family primitives from a complex mixture of sources.\n\nPeter Shor's algorithm renders classical public-key cryptography insecure on a CRQC. NIST has standardised post-quantum replacements (FIPS 203, 204, 205).\n\nThe unsolved engineering challenge: an organisation cannot migrate what it cannot locate, and cannot sequence a multi-year migration without knowing which of its thousands of cryptographic call sites are actually dangerous.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 3, "1. Executive Summary", "1.1 THREAT MODEL", "Harvest-Now-Decrypt-Later (HNDL)");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("The urgency is set by the Harvest-Now-Decrypt-Later (HNDL) threat model.\n\nA passive adversary intercepts and stores encrypted network traffic and database backups today at negligible storage cost, intending to decrypt the captured ciphertext once a CRQC becomes operational.\n\nDetection after the fact provides no remedy, and forward secrecy cannot protect data retroactively.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 4, "1. Executive Summary", "1.2 SPECIFIC GAP IN TOOLING", "Semantically Flat Outputs");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Cryptographic inventory scanners have recently emerged (CBOMkit, Crypsy), standardising around CycloneDX 1.6 CBOM. However, output is semantically flat.\n\n1. Findings are not actionable (noise). Over two-thirds of reported findings are noise, predominantly non-security hashing matched by heuristic rules.\n\n2. Findings are not ordered (flat scoring). Where risk scoring exists, it is algorithm-intrinsic. Every RSA-2048 call site receives an identical score, offering no prioritisation signal.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 5, "1. Executive Summary", "1.3 FORMALISATION", "Mosca's Inequality");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("The migration deadline is formalised by Mosca's inequality. For a given data path, let:\n\u2022 x = data confidentiality lifetime (years the data must remain secret)\n\u2022 y = migration duration (years required to re-engineer the system)\n\u2022 z = CRQC operational horizon\n\nA data path is already breached today if: x + y > z\n\nCritically, x is a property of the data being protected, not of the cipher.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 6, "1. Executive Summary", "1.4 REGULATORY JUSTIFICATION", "Compliance Urgency");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("1. India Critical Information Infrastructure (CII) deadline (2027\u20132029).\n2. Reserve Bank of India (RBI) Q-SAFE Committee.\n3. SEBI Cyber Security and Cyber Resilience Framework (CSCRF).\n4. US Executive Order 14412 (June 2026).\n5. NIST final standards (FIPS 203, 204, 205).", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 7, "2. Literature Survey", "2.1 METHODOLOGY & 2.2 SUMMARY", "16 Core Papers Surveyed");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Survey across ACM Digital Library, IEEE Xplore, IACR Cryptology ePrint, arXiv and Springer (Jan 2024\u2013Aug 2026).\n\nKey baselines:\n\u2022 P1 Crypsy: 214-rule static scanner; real-world actionable precision \u2248 0.30.\n\u2022 P2 Shaw: Regex detection with VQE threat score; algorithm-only scoring.\n\u2022 P3 Pallar\u00e9s et al.: LLM-based migration; degrades sharply on multi-file repos.\n\u2022 P13 CryptoGuard: Backward inter-procedural dataflow analysis at scale.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 8, "2. Literature Survey", "2.3 CRITICAL ANALYSIS", "What Prior Work Gets Wrong");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Critique of P1 (Crypsy):\nFlaw: Context-blindness, no dataflow, no prioritisation.\nCorrection: Inter-procedural semantic dataflow with HNDL Exposure Score.\n\nCritique of P2 (Shaw):\nFlaw: Score cannot discriminate identical algorithms.\nCorrection: Score based on protected data path.\n\nCritique of P3 (Pallar\u00e9s):\nFlaw: Synthetic single-fragment ceiling, superficial verification.\nCorrection: Verified hybrid templates with differential equivalence testing.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 9, "3. Project Objectives", "3.1 PRIMARY OBJECTIVES", "O1 to O7");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("O1: Multi-language discovery. F1 \u2265 0.85.\nO2: Semantic dataflow binding. \u2265 70% binding.\nO3: HNDL exposure scoring. nDCG@20 \u2265 0.80.\nO4: Noise suppression. Actionable precision \u2265 0.70.\nO5: Verified hybrid patch synthesis. \u2265 80% pass rate.\nO6: Public benchmark release.\nO7: Evaluation methodology standardisation.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 10, "3. Project Objectives", "3.2 PILLARS OF NOVELTY", "N1 to N5");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("N1: Retention-aware cryptographic dataflow binding.\nN2: Call-site-discriminating risk score and ranking metric.\nN3: Dataflow-conditioned noise suppression.\nN4: Differentially verified hybrid patch synthesis.\nN5: Public retention-annotated benchmark.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 11, "4. Requirement Analysis", "4.1 STAKEHOLDERS & 4.2 FRs", "Functional Requirements");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Stakeholders: CISO, DevSecOps, Software Developers.\n\nFR-1: Multi-language AST discovery.\nFR-2: Constant propagation and type inference.\nFR-3/FR-4: Backward and forward taint tracing.\nFR-5: Retention policy extraction.\nFR-6: HNDL scoring and Mosca evaluation.\nFR-7: Context noise suppression.\nFR-8: Hybrid patch synthesis and verification.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 12, "4. Requirement Analysis", "4.3 NON-FUNCTIONAL REQUIREMENTS", "NFRs");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("NFR-1: Scanning throughput (50k files in <10 mins).\nNFR-2: Memory footprint (<4 GB peak RAM).\nNFR-3: No specialised hardware (pure software).\nNFR-4: Provenance integrity (observed vs inferred).\nNFR-5: Graceful fallback and soundness (audit bucket).\nNFR-6: Schema conformance (CycloneDX 1.6 CBOM).", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 13, "5. System Design", "5.1 END-TO-END PIPELINE", "Four-Stage Architecture");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("The system is a four-stage pipeline. Each stage consumes structured output of the previous stage:\n\n1. Multi-Language Cryptographic Discovery Layer\n2. Inter-Procedural Semantic Dataflow and Retention Engine\n3. HNDL Prioritisation, Scoring and Noise Suppression\n4. Hybrid Patch Synthesis and Differential Verification", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 14, "5. System Design", "5.2 & 5.3 DISCOVERY AND DATAFLOW", "Subsystems 1 and 2");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Subsystem 1 \u2014 Discovery Layer\n\u2022 Tree-sitter + Python ast module.\n\u2022 Extensible rule corpus for cryptographic namespaces.\n\u2022 Constant propagation.\n\nSubsystem 2 \u2014 Dataflow Engine\n\u2022 Formal dataflow lattice propagating over CFGs.\n\u2022 Backward taint from arguments to sources.\n\u2022 Forward taint from outputs to sinks.\n\u2022 Declarative retention extractor (e.g. redis TTLs, S3 rules).", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 15, "5. System Design", "5.4 SCORING AND SUPPRESSION", "Subsystem 3");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("HNDL Exposure Score:\nExposure(p) = w_r\u00b7R(p) \u00d7 w_e\u00b7E(p) \u00d7 w_a\u00b7A(p) \u00d7 w_k\u00b7K(p)\n\n\u2022 Mosca breach flagged if: RetentionYears + MigrationYears > CRQCHorizon.\n\u2022 Noise suppression reclassifies non-security hashing.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 16, "5. System Design", "5.5 PATCHING & 5.6 SCHEMA", "Subsystems 4 and Data");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("Subsystem 4 \u2014 Verified Patching\n\u2022 Hybrid templates (e.g. X25519 + ML-KEM-768) via liboqs.\n\u2022 3 Gates: Differential equivalence, Property testing, Downgrade resistance.\n\n5.6 Data Schema\n\u2022 Emits CycloneDX 1.6 CBOM enriched with cryptoProperties and custom dataflowProperties.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 17, "6. Component Selection", "6.1 & 6.2 PARSING & TAINT", "Technical Justification");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("6.1 Parsing Infrastructure:\nSelected: Tree-sitter + Python ast (Multi-language, High throughput, robust to errors).\nRejected: ANTLR4, Compiler front-ends.\n\n6.2 Static Analysis & Taint:\nSelected: CodeQL (Java) + AST visitor (Python).\nRejected: Soot/WALA, Semgrep OSS (intra-procedural only).", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 18, "6. Component Selection", "6.3, 6.4, 6.5 TOOLS", "PQC, CBOM & Verification");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("6.3 PQC Library:\nSelected: Open Quantum Safe (liboqs). Full NIST FIPS 203/204/205 conformance.\n\n6.4 CBOM Schema:\nSelected: OWASP CycloneDX 1.6 CBOM.\n\n6.5 Patch Verification Strategy:\nSelected: Differential testing + property tests.\nRejected: Formal verification (Dafny, F*) due to real-world infeasibility.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 19, "7. Initial Prototype", "7.1 IMPLEMENTED PACKAGE STRUCTURE", "TRL 3 Prototype");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("src/crypto_agility_navigator/\n\u251c\u2500\u2500 models.py      # domain models\n\u251c\u2500\u2500 discovery.py   # Stage 1: AST scanner\n\u251c\u2500\u2500 dataflow.py    # Stage 2: backward/forward taint\n\u251c\u2500\u2500 scorer.py      # Stage 3: HNDL exposure scoring\n\u251c\u2500\u2500 cbom.py        # CycloneDX 1.6 CBOM serialiser\n\u251c\u2500\u2500 cli.py         # CLI and reporting\n\u2514\u2500\u2500 server.py      # REST API\ntests/test_navigator.py       # 100% passing tests\nexamples/sample_project/      # Benchmark example", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 20, "7. Initial Prototype", "7.3 EMPIRICAL VALIDATION", "CLI Benchmark Output");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("CLI Output on sample_project:\nDiscovered 3 cryptographic invocation(s).\n\nRANK  ALGORITHM  LOCATION        RETENTION  EXPOSURE         SCORE  URGENCY\n----------------------------------------------------------------------------------\n1     RSA-OAEP   archive.py:11   10.0y      EXTERNAL_PUBLIC  16.7   HIGH (MOSCA BREACH)\n2     RSA-OAEP   session.py:11   <1 hour    INTERNAL_IPC     0.0    LOW\n3     SHA-256    etags.py:9      <1 hour    INTERNAL_IPC     0.0    SUPPRESSED\n\nTwo identical RSA-OAEP sites are correctly discriminated by retention and exposure.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 21, "7. Initial Prototype", "7.4 & 7.5 TESTING AND UI", "Tests and Dashboard");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("7.4 Automated Unit Test Suite\n\u2022 8 automated unit tests covering Stage 1-3 pipeline.\n\u2022 100% passing rate on tests/test_navigator.py.\n\n7.5 Interactive Web Dashboard\n\u2022 Python http.server REST API + React SPA.\n\u2022 Features: KPI overview, Prioritisation table, Dataflow visualiser, Mosca simulation engine, Live AST scanner, CBOM inspector.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 22, "8. Innovation & Feasibility", "8.1 & 8.2 INNOVATION AND FEASIBILITY", "Mathematical Basis & Soundness");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("8.1 Mathematical Basis:\nU(p) \u221d max(0, xp + yp \u2212 z)\nRanks data paths by expected residual exposure under delayed remediation.\n\n8.2 Soundness vs Completeness:\nTargets \u2265 70% dataflow coverage. Unresolvable paths go to an explicit audit bucket.\n\n8.3 Computational Feasibility:\nO(N) discovery. Polynomial inter-procedural taint. <4GB memory.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 23, "9. Project Planning", "9.1 & 9.2 WORK DIVISION PRINCIPLE", "Review II (Completed)");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("9.1 Work Division Principle\nEquitable split of technical and non-technical work across 3 members.\n\n9.2 Work Division for Review II\n\u2022 Avi Dhandhania: Stage 1 AST discovery, backward taint tracing. Sections 1, 4, 5.\n\u2022 Anmol Saluja: Forward taint tracing, retention extractor, Stage 3 HNDL scoring. Sections 2, 3, 6, 8.\n\u2022 Avika Tyagi: CBOM serialiser, CLI, REST API, Web dashboard, tests. Sections 7, 9, 10.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 24, "9. Project Planning", "9.3 WORK PLAN FOR FUTURE REVIEWS", "Review III to VI");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("\u2022 Review III (\u2248 30%): Java support (Tree-sitter), Expand rule corpus, CBOM validation.\n\u2022 Review IV (\u2248 50%): Inter-procedural Java taint (CodeQL), ORM retention extraction, CI integration.\n\u2022 Review V-VI (\u2248 80-100%): Three-gate patch verification harness, nDCG ranking evaluation, Hybrid patch templates (X25519 + ML-KEM), Final public benchmark release.", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

{
  const s = addSlideBase(pres, 25, "10. References", "10. REFERENCES", "Standards");
  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText("10.2 Regulatory and Standards References:\n\u2022 NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA)\n\u2022 OWASP CycloneDX 1.6 CBOM Specification\n\u2022 RBI Q-SAFE Committee Terms of Reference (2026)\n\u2022 SEBI Cyber Security and Cyber Resilience Framework (CSCRF)\n\u2022 US Executive Order 14412 on Cryptography Bills of Materials (June 2026)\n\u2022 Indian Patent Office CRI Guidelines (2025)", { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 });
}

const outputFile = path.join(__dirname, '..', 'Crypto-Agility_Navigator_Review2.pptx');
pres.writeFile({ fileName: outputFile }).then(fileName => {
    console.log(`[+] Successfully generated Review 2 presentation: ${fileName}`);
});
