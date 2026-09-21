/**
 * Generates Crypto-Agility_Navigator_Review2.pptx
 * Matches the exact styling, color palette, dark theme, and typography of Review 1
 * Aligned strictly with BACSE291 IDP Review II evaluation rubrics (20 Marks).
 */

const path = require('path');
const pptxgen = require('pptxgenjs');

const pres = new pptxgen();

pres.layout = 'LAYOUT_16x9'; // 10 x 5.625 inches

// Color Palette matching Review 1
const BG_DARK = 'FFFFFF';
const CARD_BG = 'F8F9FA';
const BORDER_COLOR = 'E0E0E0';
const TEXT_MUTED = '666666';
const TEXT_BODY = '333333';
const TEXT_WHITE = '000000';
const ACCENT_RED = 'D32F2F';
const ACCENT_GREEN = '2E7D32';
const ACCENT_BLUE = '1976D2';

const TOTAL_SLIDES = 37;

function addSlideBase(pres, slideNum, sectionName, title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: BG_DARK };

  // Header line
  slide.addShape(pres.ShapeType.line, {
    x: 0.5, y: 0.68, w: 9.0, h: 0,
    line: { color: BORDER_COLOR, width: 1 }
  });

  // Top header text
  slide.addText('CRYPTO-AGILITY NAVIGATOR', {
    x: 0.5, y: 0.35, w: 5.5, h: 0.25,
    fontSize: 9, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 1.5
  });

  slide.addText(sectionName.toUpperCase(), {
    x: 5.0, y: 0.35, w: 4.5, h: 0.25,
    fontSize: 9, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true, tracking: 1.5
  });

  // Title & Subtitle
  slide.addText(title, {
    x: 0.5, y: 0.85, w: 9.0, h: 0.3,
    fontSize: 12, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 1.2
  });

  slide.addText(subtitle, {
    x: 0.5, y: 1.15, w: 9.0, h: 0.45,
    fontSize: 18, fontFace: 'Arial', color: TEXT_WHITE, bold: true
  });

  // Footer divider line
  slide.addShape(pres.ShapeType.line, {
    x: 0.5, y: 5.15, w: 9.0, h: 0,
    line: { color: BORDER_COLOR, width: 1 }
  });

  // Footer text
  slide.addText(sectionName.toUpperCase(), {
    x: 0.5, y: 5.25, w: 6.5, h: 0.25,
    fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, bold: true
  });

  const numStr = `${String(slideNum).padStart(2, '0')} / ${TOTAL_SLIDES}`;
  slide.addText(numStr, {
    x: 7.5, y: 5.25, w: 2.0, h: 0.25,
    fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true
  });

  return slide;
}

// -------------------------------------------------------------
// SLIDE 1: Title Slide
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  slide.background = { color: BG_DARK };

  slide.addText('REVIEW REPORT II · INNOVATIVE DESIGN PROJECT (BACSE291)', {
    x: 0.8, y: 1.2, w: 8.4, h: 0.35,
    fontSize: 11, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 2
  });

  slide.addText('Crypto-Agility Navigator', {
    x: 0.8, y: 1.6, w: 8.4, h: 0.9,
    fontSize: 34, fontFace: 'Arial', color: TEXT_WHITE, bold: true
  });

  slide.addText('Dataflow-Aware Cryptographic Inventory & Prioritised Post-Quantum Migration', {
    x: 0.8, y: 2.5, w: 8.4, h: 0.45,
    fontSize: 15, fontFace: 'Arial', color: TEXT_BODY
  });

  // Metadata Card
  slide.addShape(pres.ShapeType.rect, {
    x: 0.8, y: 3.2, w: 8.4, h: 1.5,
    fill: { color: CARD_BG },
    line: { color: BORDER_COLOR, width: 1 }
  });

  slide.addText([
    { text: 'EVALUATION MILESTONE: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Review II — Initial Design and Development (20 Marks)\n', options: { color: TEXT_BODY } },
    { text: 'ASSESSMENT FOCUS: ', options: { bold: true, color: TEXT_WHITE } },
    { text: '~20% Completion · Architecture · Tool Justification · TRL 3 Working Prototype\n', options: { color: TEXT_BODY } },
    { text: 'TEAM & ACADEMIC YEAR: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Team of 3 Students · Academic Year 2026–2027 · Software-Only Track (No Specialized Hardware)\n', options: { color: TEXT_BODY } },
    { text: 'KEY STANDARDS: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'OWASP CycloneDX 1.6 CBOM · NIST FIPS 203/204/205 · Open Quantum Safe (liboqs)', options: { color: TEXT_MUTED } }
  ], {
    x: 1.1, y: 3.35, w: 7.8, h: 1.2,
    fontSize: 9.5, fontFace: 'Arial', lineSpacing: 16
  });

  slide.addText(`01 / ${TOTAL_SLIDES}`, {
    x: 7.5, y: 5.25, w: 2.0, h: 0.25,
    fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true
  });
}

// -------------------------------------------------------------
// SLIDE 2: Executive Summary & Review II Agenda
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 2, 'Executive Summary', 'MILESTONE OVERVIEW', 'Review II Scope, Progress & 20% Proof of Concept');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.2, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.2, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('RUBRICS FOR REVIEW II (20 MARKS)', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '1. Requirement Analysis (3 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'HNDL threat model & Mosca formalization.\n', options: { color: TEXT_BODY } },
    { text: '2. System Design & Architecture (3 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: '4-stage pipeline & CycloneDX 1.6.\n', options: { color: TEXT_BODY } },
    { text: '3. Tool Selection & Justification (3 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: '5 comparative trade-off matrices.\n', options: { color: TEXT_BODY } },
    { text: '4. Initial Prototype (~20%) (3 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Working AST, Taint & Scoring PoC.\n', options: { color: TEXT_BODY } },
    { text: '5. Innovation & Feasibility (3 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'N1–N5 defense, math derivation & CRI patent.\n', options: { color: TEXT_BODY } },
    { text: '6. Project Planning & Teamwork (3 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Roadmap & 3-way work split.\n', options: { color: TEXT_BODY } },
    { text: '7. Individual Contribution & Defense (2 M): ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Module ownership & Q&A guide.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.4, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText('WHAT WE DELIVER IN REVIEW II', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Full Review 2 Master Report:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Integrating Review 1 literature review with detailed design.\n', options: { color: TEXT_BODY } },
    { text: '• Working Python Prototype (TRL 3):\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  AST parser, inter-procedural dataflow, retention extractor.\n', options: { color: TEXT_BODY } },
    { text: '• Demonstration on Real Benchmark:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Orders identical RSA call sites by S3 retention vs Redis TTL.\n', options: { color: TEXT_BODY } },
    { text: '• Standard CycloneDX 1.6 CBOM Export:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Enriched with custom dataflow properties.\n', options: { color: TEXT_BODY } },
    { text: '• Automated Test Harness:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  5/5 unit tests passing with 100% success rate.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.4, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 3: Section 01 - The Problem Recap
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 3, 'Problem Identification', '1.1 THE TECHNICAL PROBLEM', 'Enterprise Cryptography Cannot Be Located or Sequenced');

  s.addText('A mid-sized banking application invokes RSA, ECDSA, AES and SHA-family primitives from first-party code, third-party libraries, container base images, TLS terminators, database drivers and IaC — with no single machine-readable artefact recording where those invocations are or what data they protect.', {
    x: 0.5, y: 1.7, w: 4.3, h: 2.0, fontSize: 10, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 16
  });

  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText('THE CORE PARADOX', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'WHAT TO MIGRATE TO — SETTLED\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: 'NIST has standardised ML-KEM (FIPS 203), ML-DSA (FIPS 204), and SLH-DSA (FIPS 205).\n\n', options: { color: TEXT_BODY } },
    { text: 'WHERE CRYPTOGRAPHY LIVES — UNKNOWN\n', options: { bold: true, color: ACCENT_RED } },
    { text: 'Scattered across thousands of undocumented call sites in complex repos.\n\n', options: { color: TEXT_BODY } },
    { text: 'WHAT TO MIGRATE FIRST — UNANSWERED\n', options: { bold: true, color: ACCENT_RED } },
    { text: 'No tool connects cryptographic call sites to data lifetime and exposure surface.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 4: Section 01 - Threat Model HNDL & Mosca's Inequality
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 4, 'Threat Model', '1.1 THREAT MODEL — HNDL', "Harvest-Now-Decrypt-Later & Mosca's Inequality");

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('HARVEST-NOW-DECRYPT-LATER (HNDL)', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Passive, Patient Adversary:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Cannot break RSA/ECC today; records ciphertext in transit and database exfiltrations.\n\n', options: { color: TEXT_BODY } },
    { text: '• Negligible Storage Cost:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Stores encrypted blobs indefinitely, waiting for a Cryptographically Relevant Quantum Computer (CRQC).\n\n', options: { color: TEXT_BODY } },
    { text: '• No Retroactive Remedy:\n', options: { bold: true, color: ACCENT_RED } },
    { text: '  Forward secrecy cannot protect captured traffic retroactively.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText("MOSCA'S INEQUALITY FORMALIZATION", { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'x + y > z  ⟹  ALREADY BREACHED\n\n', options: { bold: true, color: ACCENT_RED, fontSize: 12 } },
    { text: '• x = Data Confidentiality Lifetime (years)\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  e.g., 10–30 years for healthcare, financial records.\n', options: { color: TEXT_BODY } },
    { text: '• y = Migration Time (years)\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Typically 2–5 years for enterprise migration.\n', options: { color: TEXT_BODY } },
    { text: '• z = Time to CRQC operationalization (years)\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  National timeline: 2027–2029 deadline (z ≈ 3–7 yr).\n\n', options: { color: TEXT_BODY } },
    { text: 'Key Insight: HNDL exposure is a property of THE DATA, not the algorithm!', options: { bold: true, color: TEXT_WHITE } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 5: Section 01 - The Gap: Semantically Flat Tools
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 5, 'The SOTA Gap', '1.2 THE STATE-OF-THE-ART GAP', 'Current Discovery Tools Produce Semantically Flat Inventories');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('CONSEQUENCE 1: NOISE (~0.30 PRECISION)', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Context-Blind Rules:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Crypsy [P1] reports rules fire indiscriminately across all matching calls.\n\n', options: { color: TEXT_BODY } },
    { text: '• 2 Out of 3 Findings Are Noise:\n', options: { bold: true, color: ACCENT_RED } },
    { text: '  Non-security hashing (ETags, cache keys, checksums) matched by the same heuristic rules as password hashing.\n\n', options: { color: TEXT_BODY } },
    { text: '• Unmanageable Triage Burden:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Security teams must manually inspect hundreds of benign calls.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText('CONSEQUENCE 2: FLAT ALGORITHM SCORING', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Algorithm-Intrinsic Scores:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Shaw [P2] calculates risk from key size, Shor qubit count, and Grover factors.\n\n', options: { color: TEXT_BODY } },
    { text: '• Zero Prioritization Signal:\n', options: { bold: true, color: ACCENT_RED } },
    { text: '  Every RSA-2048 call site receives an identical score regardless of protected data.\n\n', options: { color: TEXT_BODY } },
    { text: '• The Operational Question Unanswered:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  When all findings are ranked equally, engineers cannot build sprint backlogs.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 6: Section 01 - Worked Benchmark Example
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 6, 'Worked Example', '1.3 WORKED EXAMPLE', 'Two Identical Call Sites in One Repository');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('SITE A: payments/archive.py', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: ACCENT_RED, bold: true });
  s.addText([
    { text: 'record = build_settlement_record(txn)\n', options: { fontFace: 'Courier New', color: TEXT_MUTED } },
    { text: 'blob = rsa_oaep_encrypt(record, pubkey)\n', options: { fontFace: 'Courier New', color: TEXT_WHITE, bold: true } },
    { text: 's3.put_object(Bucket="settlements", Body=blob)\n\n', options: { fontFace: 'Courier New', color: TEXT_MUTED } },
    { text: '• Source: Persistent database settlement record\n', options: { color: TEXT_BODY } },
    { text: '• Sink: Public cloud S3 bucket (10-yr lifecycle rule)\n', options: { color: TEXT_BODY } },
    { text: '• Mosca: 10y + 2y > 7y  ⟹  CRITICAL BREACH\n', options: { bold: true, color: ACCENT_RED } },
    { text: '• Required Action: Immediate PQC remediation.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });

  s.addText('SITE B: web/session.py', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  s.addText([
    { text: 'tok = make_csrf_token()\n', options: { fontFace: 'Courier New', color: TEXT_MUTED } },
    { text: 'sealed = rsa_oaep_encrypt(tok, pubkey)\n', options: { fontFace: 'Courier New', color: TEXT_WHITE, bold: true } },
    { text: 'redis.setex(k, 900, sealed)\n\n', options: { fontFace: 'Courier New', color: TEXT_MUTED } },
    { text: '• Source: In-memory random CSRF token\n', options: { color: TEXT_BODY } },
    { text: '• Sink: Local cache with 900-second TTL\n', options: { color: TEXT_BODY } },
    { text: '• Mosca: 0.00003y + 2y < 7y  ⟹  NO BREACH\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '• Required Action: Defer; zero HNDL reduction.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 7: Section 01 - Regulatory Deadlines
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 7, 'Compliance Urgency', '1.4 REGULATORY JUSTIFICATION', 'Mandated Deadlines with Legal Compliance Obligations');

  const cards = [
    { title: 'INDIA / CII', date: '2027–2029', desc: 'National Quantum-Safe Task Force mandate for Critical Information Infrastructure.' },
    { title: 'RBI / Q-SAFE', date: '2026', desc: 'IIT Madras chaired committee mandating crypto inventory & agility scoring.' },
    { title: 'SEBI CSCRF', date: 'MANDATED', desc: 'Cyber resilience framework directing intermediaries to mitigate HNDL threats.' },
    { title: 'US EO 14412', date: 'JUNE 2026', desc: 'Directs CISA & NIST to publish minimum elements for Cryptography BOM within 270 days.' }
  ];

  cards.forEach((c, idx) => {
    const x = 0.5 + idx * 2.25;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.15, h: 2.9, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(c.title, { x: x + 0.15, y: 2.0, w: 1.85, h: 0.25, fontSize: 9.5, fontFace: 'Arial', color: TEXT_MUTED, bold: true });
    s.addText(c.date, { x: x + 0.15, y: 2.3, w: 1.85, h: 0.4, fontSize: 15, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(c.desc, { x: x + 0.15, y: 2.8, w: 1.85, h: 1.6, fontSize: 8.2, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 12 });
  });
}

// -------------------------------------------------------------
// SLIDE 8: Section 02 - Literature Survey & Gap Matrix
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 8, 'Literature Review', '2.0 LITERATURE SURVEY & GAP MATRIX', '16 Surveyed Papers Across Scanners, Scoring & Migration');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText([
    { text: 'CONSOLIDATED RESEARCH GAP MATRIX (16 PAPERS SURVEYED: P1–P16)\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 9.5 } },
    { text: '• Discovery Scanners (P1 Crypsy, CBOMkit, IBM): ', options: { bold: true, color: TEXT_MUTED } },
    { text: 'Flat inventories, 0.3 actionable precision, context-blind.\n', options: { color: TEXT_BODY } },
    { text: '• Threat Scoring (P2 Shaw, P5 CARS): ', options: { bold: true, color: TEXT_MUTED } },
    { text: 'Algorithm-intrinsic (all RSA-2048 score identical); no dataflow binding.\n', options: { color: TEXT_BODY } },
    { text: '• LLM Migration (P3 Pallarés): ', options: { bold: true, color: TEXT_MUTED } },
    { text: 'Synthetic snippets; 92.5% correctness collapses on real multi-file repos.\n', options: { color: TEXT_BODY } },
    { text: '• SE Frameworks (P4 AQuA, P14 SLR): ', options: { bold: true, color: TEXT_MUTED } },
    { text: 'Identifies missing pillars (detection, refactoring, verification); no tool.\n', options: { color: TEXT_BODY } },
    { text: '• Cryptographic Dataflow (P13 CryptoGuard): ', options: { bold: true, color: TEXT_MUTED } },
    { text: 'CCS 2019 proved scalable taint analysis is tractable at scale in software.\n\n', options: { color: TEXT_BODY } },
    { text: 'THE UNIQUE CONTRIBUTION OF CRYPTO-AGILITY NAVIGATOR:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: 'First framework to combine multi-language discovery + inter-procedural dataflow + declarative retention extraction + HNDL ranking + verified hybrid PQC patches.', options: { color: TEXT_WHITE, bold: true } }
  ], { x: 0.8, y: 1.9, w: 8.4, h: 2.7, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 9: Section 03 - Primary and Secondary Objectives
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 9, 'Parameter 1 (3 M)', '3.1 PRIMARY AND SECONDARY OBJECTIVES', 'Consolidated Project Goals');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  
  s.addText([
    { text: 'O1: Multi-language discovery\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O2: Semantic dataflow binding\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O3: HNDL exposure scoring\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O4: Noise suppression\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O5: Verified patch synthesis\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O6: Public benchmark release\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } }
  ], { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Arial', lineSpacing: 16 });
}
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 10, 'Parameter 1 (3 M)', '3.2 THE 5 PILLARS OF NOVELTY', 'Core Intellectual Innovations (N1–N5)');

  const novs = [
    { id: 'N1', title: 'RETENTION-AWARE DATAFLOW', desc: 'Binds cryptographic primitives to data lifetime extracted from declarative code & IaC.' },
    { id: 'N2', title: 'CALL-SITE RISK METRIC', desc: 'First score varying across identical algorithms; evaluated via ranking metrics (nDCG/τ).' },
    { id: 'N3', title: 'CONTEXT NOISE SUPPRESSION', desc: 'Filters non-security hashes; raises actionable precision from ~0.30 to ≥0.70.' },
    { id: 'N4', title: 'VERIFIED HYBRID PATCHES', desc: 'liboqs hybrid synthesis gated by differential testing, property tests, & downgrade checks.' },
    { id: 'N5', title: 'ANNOTATED BENCHMARK', desc: '15–20 open-source repositories annotated with retention ground truth & priority rankings.' }
  ];

  novs.forEach((n, idx) => {
    const x = 0.5 + idx * 1.8;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 1.7, h: 3.0, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(n.id, { x: x + 0.1, y: 2.0, w: 1.5, h: 0.35, fontSize: 16, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText(n.title, { x: x + 0.1, y: 2.4, w: 1.5, h: 0.45, fontSize: 8.5, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(n.desc, { x: x + 0.1, y: 2.9, w: 1.5, h: 1.8, fontSize: 7.8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
  });
}
// -------------------------------------------------------------
// SLIDE 9: Section 03 - Requirements Analysis: Stakeholders
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 11, 'Parameter 1 (3 M)', '4.1 REQUIREMENT ANALYSIS: STAKEHOLDERS', 'Mapping Operational Value to Regulated Roles');

  const roles = [
    { title: 'CISO / COMPLIANCE', pain: 'Regulatory transition deadlines (RBI 2027–2029) without an auditable roadmap.', solution: 'Enriched CycloneDX 1.6 CBOM with legally defensible Mosca risk scoring.' },
    { title: 'DEVSECOPS ENGINEERS', pain: 'Overwhelmed by false alerts (67% noise in existing tools); zero triage signal.', solution: 'Dataflow-conditioned suppression filters non-security hashes (ETags, cache keys).' },
    { title: 'SOFTWARE DEVELOPERS', pain: 'Lacking PQC expertise; fear of breaking production handshakes during upgrades.', solution: 'Template-constrained hybrid patches (liboqs) with differential test gates.' }
  ];

  roles.forEach((r, idx) => {
    const x = 0.5 + idx * 3.05;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.95, h: 2.9, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(r.title, { x: x + 0.2, y: 2.0, w: 2.55, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText('PRIMARY PAIN POINT:', { x: x + 0.2, y: 2.4, w: 2.55, h: 0.2, fontSize: 8, fontFace: 'Arial', color: ACCENT_RED, bold: true });
    s.addText(r.pain, { x: x + 0.2, y: 2.65, w: 2.55, h: 0.8, fontSize: 8.2, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 12 });
    s.addText('NAVIGATOR SOLUTION:', { x: x + 0.2, y: 3.5, w: 2.55, h: 0.2, fontSize: 8, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
    s.addText(r.solution, { x: x + 0.2, y: 3.75, w: 2.55, h: 0.8, fontSize: 8.2, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 12 });
  });
}

// -------------------------------------------------------------
// SLIDE 10: Section 03 - Functional Requirements (FR-1 to FR-4)
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 12, 'Parameter 1 (3 M)', '4.2 FUNCTIONAL REQUIREMENTS (PART 1)', 'Discovery, Standards Conformance & Taint Tracing');

  const frs = [
    { id: 'FR-1', name: 'Multi-Language AST Discovery', spec: 'Parse Python/Java source trees to discover cryptographic primitives, extracting call sites, algorithms, and key sizes.', target: 'F1 ≥ 0.85 on benchmark' },
    { id: 'FR-2', name: 'CycloneDX 1.6 CBOM Output', spec: 'Serialize all discovered assets into standards-compliant CycloneDX 1.6 CBOM format with custom dataflow fields.', target: '100% schema validation' },
    { id: 'FR-3', name: 'Backward Taint Binding', spec: 'Trace plaintext parameters backward across call graphs to data sources (DB reads, credentials, ephemeral tokens).', target: '≥ 70% binding coverage' },
    { id: 'FR-4', name: 'Forward Taint Binding', spec: 'Trace ciphertext outputs forward to sinks (S3, DB, Redis, sockets) and classify spatial exposure surface.', target: '≥ 70% sink classification' }
  ];

  frs.forEach((f, idx) => {
    const x = 0.5 + idx * 2.25;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.15, h: 2.9, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(f.id, { x: x + 0.15, y: 2.0, w: 1.85, h: 0.25, fontSize: 12, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText(f.name, { x: x + 0.15, y: 2.3, w: 1.85, h: 0.4, fontSize: 9.5, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(f.spec, { x: x + 0.15, y: 2.8, w: 1.85, h: 1.1, fontSize: 8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
    s.addText('TARGET: ' + f.target, { x: x + 0.15, y: 4.1, w: 1.85, h: 0.4, fontSize: 8, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  });
}

// -------------------------------------------------------------
// SLIDE 11: Section 03 - Functional Requirements (FR-5 to FR-8)
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 13, 'Parameter 1 (3 M)', '4.2 FUNCTIONAL REQUIREMENTS (PART 2)', 'Retention Inference, Scoring, Suppression & Patches');

  const frs = [
    { id: 'FR-5', name: 'Declarative Retention Extractor', spec: 'Extract data confidentiality lifetimes from adjacent configs: S3 lifecycle rules, Redis TTLs, ORM column types.', target: '≥ 50% automated recovery' },
    { id: 'FR-6', name: 'HNDL Exposure Scoring', spec: "Operationalize Mosca's inequality per data path, ranking findings by risk reduction per unit of remediation effort.", target: 'nDCG@20 ≥ 0.80, τ ≥ 0.60' },
    { id: 'FR-7', name: 'Context Noise Suppression', spec: 'Reclassify non-security hashes (cache keys, ETags) using dataflow context to filter out false alerts.', target: 'Precision ≥ 0.70 (vs ~0.30)' },
    { id: 'FR-8', name: 'Verified Hybrid Patching', spec: 'Synthesize template-constrained hybrid PQC patches (liboqs) gated by differential equivalence and property tests.', target: '≥ 80% verification pass' }
  ];

  frs.forEach((f, idx) => {
    const x = 0.5 + idx * 2.25;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.15, h: 2.9, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(f.id, { x: x + 0.15, y: 2.0, w: 1.85, h: 0.25, fontSize: 12, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText(f.name, { x: x + 0.15, y: 2.3, w: 1.85, h: 0.4, fontSize: 9.5, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(f.spec, { x: x + 0.15, y: 2.8, w: 1.85, h: 1.1, fontSize: 8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
    s.addText('TARGET: ' + f.target, { x: x + 0.15, y: 4.1, w: 1.85, h: 0.4, fontSize: 8, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  });
}

// -------------------------------------------------------------
// SLIDE 12: Section 03 - Non-Functional Requirements
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 14, 'Parameter 1 (3 M)', '4.3 NON-FUNCTIONAL REQUIREMENTS', 'Performance, Scalability, Soundness & Compliance');

  const nfrs = [
    { title: 'NFR-1: HIGH THROUGHPUT', desc: 'Scan large multi-file repositories (~50,000 files) in under 10 minutes on commodity 8-core laptops.' },
    { title: 'NFR-2: BOUNDED MEMORY', desc: 'Peak resident memory consumption during inter-procedural analysis strictly below 4 GB RAM.' },
    { title: 'NFR-3: ZERO HARDWARE', desc: 'Pure software static analysis; zero GPUs, zero quantum emulators, zero commercial paid API credits.' },
    { title: 'NFR-4: TRANSPARENCY', desc: 'Full provenance recording: every retention value tagged as observed (explicit) or inferred (prior).' },
    { title: 'NFR-5: AUDITABLE FALLBACK', desc: 'Unresolvable dataflows routed to an explicit "insufficient context" audit bucket; never guessed.' },
    { title: 'NFR-6: SCHEMA COMPLIANCE', desc: '100% schema validation against official OWASP CycloneDX 1.6 CBOM JSON/XML specifications.' }
  ];

  nfrs.forEach((n, idx) => {
    const col = idx % 3;
    const row = Math.floor(idx / 3);
    const x = 0.5 + col * 3.05;
    const y = 1.8 + row * 1.5;
    s.addShape(pres.ShapeType.rect, { x: x, y: y, w: 2.95, h: 1.35, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(n.title, { x: x + 0.15, y: y + 0.15, w: 2.65, h: 0.25, fontSize: 9, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(n.desc, { x: x + 0.15, y: y + 0.45, w: 2.65, h: 0.75, fontSize: 7.8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
  });
}

// -------------------------------------------------------------
// SLIDE 13: Section 04 - System Architecture Pipeline
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 15, 'Parameter 2 (3 M)', '5.1 SYSTEM ARCHITECTURE', 'End-to-End 4-Stage Analysis & Remediation Pipeline');

  const stages = [
    { num: '01', title: 'DISCOVERY', desc: 'Tree-sitter parse & Semgrep rules.\nConstant propagation resolves runtime cipher names.', out: 'CBOM Candidates' },
    { num: '02', title: 'SEMANTIC BINDING (N1)', desc: 'Backward taint: Plaintext ➔ Source.\nForward taint: Ciphertext ➔ Sink.\nExtracts retention from S3/TTL/ORM.', out: 'Enriched Data Paths' },
    { num: '03', title: 'SCORING & NOISE (N2, N3)', desc: 'Computes HNDL Exposure Score.\nEvaluates Mosca breach (x + y > z).\nSuppresses non-security hashes.', out: 'Ranked Migration Plan' },
    { num: '04', title: 'PATCH & VERIFY (N4)', desc: 'liboqs hybrid templates (X25519+ML-KEM).\n3-Gate Verification: Differential, Property, Downgrade tests.', out: 'Verified Pull Requests' }
  ];

  stages.forEach((st, idx) => {
    const x = 0.5 + idx * 2.25;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.15, h: 3.0, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(st.num, { x: x + 0.15, y: 2.0, w: 1.85, h: 0.35, fontSize: 18, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText(st.title, { x: x + 0.15, y: 2.4, w: 1.85, h: 0.3, fontSize: 10, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(st.desc, { x: x + 0.15, y: 2.8, w: 1.85, h: 1.2, fontSize: 8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
    s.addText('OUTPUT:', { x: x + 0.15, y: 4.1, w: 1.85, h: 0.2, fontSize: 7.5, fontFace: 'Arial', color: TEXT_MUTED, bold: true });
    s.addText(st.out, { x: x + 0.15, y: 4.3, w: 1.85, h: 0.35, fontSize: 8.5, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  });
}

// -------------------------------------------------------------
// SLIDE 14: Section 04 - Subsystem 1: AST Discovery
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 16, 'Parameter 2 (3 M)', '5.2 SUBSYSTEM 1: DISCOVERY LAYER', 'AST Parsing, Pattern Matching & Constant Propagation');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('MULTI-LANGUAGE PARSER & RULE ENGINE', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Uniform Tree-sitter Grammar:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Generates Concrete Syntax Trees (CST) preserving byte offsets and exact locations.\n\n', options: { color: TEXT_BODY } },
    { text: '• Extensive Cryptographic API Corpus:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Covers cryptography.hazmat, PyCryptodome, hashlib, java.security, javax.crypto, and BouncyCastle.\n\n', options: { color: TEXT_BODY } },
    { text: '• Quantum Vulnerability Tagging:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Automatically tags primitives as Shor-broken (RSA, ECC), Grover-weakened (AES-128, MD5), or Quantum-safe.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText('CONSTANT PROPAGATION ENGINE', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'SOLVING CRYSY\'S RUNTIME BLINDNESS [P1]:\n', options: { bold: true, color: ACCENT_RED } },
    { text: 'Crypsy reported 0.66 recall because runtime-computed algorithm arguments were unresolvable.\n\n', options: { color: TEXT_BODY } },
    { text: '• Intra-Procedural Assignment Chains:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Traces assignments like cipher_name = "RSA-OAEP" into cipher wrappers.\n\n', options: { color: TEXT_BODY } },
    { text: '• Local Type Inference:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Infers key object instances (e.g. RSAPrivateKey, Ed25519PublicKey) from constructor calls.\n\n', options: { color: TEXT_BODY } },
    { text: '• Recovered Coverage: ', options: { bold: true, color: ACCENT_GREEN } },
    { text: 'Resolves ~15% additional call sites missed by regex.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 15: Section 04 - Subsystem 2: Inter-Procedural Taint
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 17, 'Parameter 2 (3 M)', '5.3 SUBSYSTEM 2: SEMANTIC BINDING (N1)', 'Inter-Procedural Backward & Forward Taint Analysis');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('BACKWARD TAINT: PLAINTEXT ➔ SOURCE', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Initiating Seed:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Starts at the plaintext and key parameters of the primitive.\n\n', options: { color: TEXT_BODY } },
    { text: '• Call Graph Traversal:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Follows assignments and return values across function calls to data origin.\n\n', options: { color: TEXT_BODY } },
    { text: '• Source Taxonomy Classification:\n', options: { bold: true, color: ACCENT_BLUE } },
    { text: '  1. Persistent Storage (Database table query)\n  2. Offsite Archive (Audit / compliance log)\n  3. User Credential (Password / private key)\n  4. Ephemeral Token (Local RNG / CSRF nonce)', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });

  s.addText('FORWARD TAINT: CIPHERTEXT ➔ SINK', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Ciphertext Propagation:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Tracks encrypted return values and output buffers to termination points.\n\n', options: { color: TEXT_BODY } },
    { text: '• Spatial Exposure Boundary Classification:\n', options: { bold: true, color: ACCENT_BLUE } },
    { text: '  • External Public (E = 1.0): Cloud S3 bucket or public network socket.\n', options: { color: TEXT_BODY } },
    { text: '  • Cross-Host VPC (E = 0.5): Internal DB or RPC service.\n', options: { color: TEXT_BODY } },
    { text: '  • Local IPC (E = 0.25): Redis cache on localhost.\n', options: { color: TEXT_BODY } },
    { text: '  • In-Process (E = 0.1): Never leaves application RAM.\n\n', options: { color: TEXT_BODY } },
    { text: 'Tracks key reuse count to measure blast radius.', options: { bold: true, color: TEXT_WHITE } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 16: Section 04 - Subsystem 2: Retention Extractor
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 18, 'Parameter 2 (3 M)', '5.3 RETENTION INFERENCE ENGINE', 'Recovering Confidentiality Lifetime from Declarative Code');

  const configs = [
    { title: 'CLOUD STORAGE (S3/GCS)', src: 'Lifecycle policies & IaC', detail: 'Parses Expiration InDays or retain 10 years comments in bucket deployment configs.', example: 'Retain 10 years  ⟹  R = 10.0' },
    { title: 'TEMPORARY CACHES (REDIS)', src: 'setex & TTL constants', detail: 'Extracts numeric TTL parameters from cache setter invocations.', example: 'setex(k, 900, val)  ⟹  R = 0.00003' },
    { title: 'DATABASE ORM & DDL', src: 'SQLAlchemy / Hibernate', detail: 'Inspects column definitions for expires_at, created_at, and retention annotations.', example: 'statutory_retention = 7.0' },
    { title: 'AUDITABLE FALLBACK', src: 'Sink priors & provenance', detail: 'Unresolvable sinks assigned conservative prior; flagged as inferred vs observed.', example: 'Database prior = 5.0 (Inferred)' }
  ];

  configs.forEach((c, idx) => {
    const x = 0.5 + idx * 2.25;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.15, h: 3.0, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(c.title, { x: x + 0.15, y: 2.0, w: 1.85, h: 0.35, fontSize: 9.5, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText('EVIDENCE SOURCE:', { x: x + 0.15, y: 2.45, w: 1.85, h: 0.2, fontSize: 7.5, fontFace: 'Arial', color: TEXT_MUTED, bold: true });
    s.addText(c.src, { x: x + 0.15, y: 2.65, w: 1.85, h: 0.3, fontSize: 8.5, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(c.detail, { x: x + 0.15, y: 3.05, w: 1.85, h: 0.8, fontSize: 8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
    s.addText(c.example, { x: x + 0.15, y: 3.95, w: 1.85, h: 0.6, fontSize: 8, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  });
}

// -------------------------------------------------------------
// SLIDE 17: Section 04 - Subsystem 3: Scoring & Suppression
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 19, 'Parameter 2 (3 M)', '5.4 HNDL SCORING & NOISE SUPPRESSION', 'Mosca-Grounded Prioritisation (N2) & Noise Filtering (N3)');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('HNDL EXPOSURE SCORING FORMULA', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'Exposure(p) = w_r·R(p) × w_e·E(p) × w_a·A(p) × w_k·K(p)\n\n', options: { bold: true, color: ACCENT_BLUE, fontSize: 9.5 } },
    { text: '• R(p) [Retention]: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Normalised lifetime (0 to 30 yr); observed evidence weighted 1.0 vs 0.8 prior.\n', options: { color: TEXT_BODY } },
    { text: '• E(p) [Exposure]: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Public (1.0), VPC (0.5), IPC (0.25), In-Process (0.1).\n', options: { color: TEXT_BODY } },
    { text: '• A(p) [Algorithm]: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Shor-broken (1.0), Grover (0.3), PQC (0.05).\n', options: { color: TEXT_BODY } },
    { text: '• K(p) [Key Blast Radius]: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Scales with number of paths sharing key.\n\n', options: { color: TEXT_BODY } },
    { text: 'Mosca Breach Flag: (Retention + Migration) > Horizon', options: { bold: true, color: ACCENT_RED } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });

  s.addText('CONTEXT-BASED NOISE SUPPRESSION (N3)', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'DRIVING ACTIONABLE PRECISION FROM ~0.30 TO ≥0.70:\n\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '• Suppresses Non-Security Hashing:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  If a hash function takes non-credential input (e.g. static asset) and output goes to a temporary cache key, it is reclassified as non-security.\n\n', options: { color: TEXT_BODY } },
    { text: '• ETag & Checksum Filtering:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Automatically recognizes content digest operations.\n\n', options: { color: TEXT_BODY } },
    { text: '• Tunable Threshold Curve:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Allows security teams to select their operating precision/recall point.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 18: Section 04 - Subsystem 4 & Schema
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 20, 'Parameter 2 (3 M)', '5.5 PATCH SYNTHESIS & CBOM CONTRACTS', 'liboqs Hybrid Templates, 3-Gate Testing & CycloneDX 1.6');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('3-GATE VERIFICATION HARNESS (N4)', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'Overcoming Pallarés\' [P3] Round-Trip Defects:\n\n', options: { bold: true, color: TEXT_MUTED } },
    { text: '1. Differential Equivalence Gate:\n', options: { bold: true, color: ACCENT_BLUE } },
    { text: '   Original vs patched code executed on identical input vectors; error codes and recovered plaintexts must match.\n\n', options: { color: TEXT_BODY } },
    { text: '2. Property Testing Gate (Hypothesis):\n', options: { bold: true, color: ACCENT_BLUE } },
    { text: '   Tests tamper-evidence, wrong-key rejection, and parameter boundary resilience.\n\n', options: { color: TEXT_BODY } },
    { text: '3. Downgrade Resilience Gate:\n', options: { bold: true, color: ACCENT_BLUE } },
    { text: '   Verifies hybrid peer interoperability and ensures the protocol fails closed against rollback attempts.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });

  s.addText('CYCLONEDX 1.6 CBOM EXTENSIONS', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'STANDARD CRYPTOGRAPHIC PROPERTIES:\n', options: { bold: true, color: TEXT_MUTED } },
    { text: '• assetType: "algorithm"\n• classicalSecurityLevel: 2048\n• nistQuantumSecurityLevel: 0 (Shor-broken)\n\n', options: { fontFace: 'Courier New', color: TEXT_BODY, fontSize: 7.8 } },
    { text: 'CUSTOM DATAFLOW EXTENSION PROPERTIES:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '• plaintextSource: "database_read"\n• ciphertextSink: "cloud_object_store"\n• retentionEvidence: { retentionYears: 10.0 }\n• exposureSurface: "EXTERNAL_PUBLIC"\n• hndlRiskAssessment: { moscaViolated: true }', options: { fontFace: 'Courier New', color: TEXT_WHITE, fontSize: 7.8 } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 19: Section 05 - Tool Selection 1: Parsing
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 21, 'Parameter 3 (3 M)', '6.1 TOOL JUSTIFICATION: PARSING & AST', 'Comparative Evaluation Matrix: Parsing Infrastructure');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText([
    { text: 'CANDIDATE TOOLS EVALUATION:\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: '1. Tree-sitter + Python Native ast [SELECTED]\n', options: { bold: true, color: ACCENT_GREEN, fontSize: 9.5 } },
    { text: '   • Throughput: High (~30,000 lines/sec via C API bindings).\n', options: { color: TEXT_BODY } },
    { text: '   • Multi-Language: 40+ language grammars with uniform Concrete Syntax Tree (CST) API.\n', options: { color: TEXT_BODY } },
    { text: '   • Advantage: Preserves byte offsets, handles syntax errors gracefully, zero heavy JVM overhead.\n\n', options: { color: TEXT_BODY } },
    { text: '2. ANTLR4 [REJECTED]\n', options: { bold: true, color: ACCENT_RED, fontSize: 9.5 } },
    { text: '   • Heavy runtime overhead, slow startup latency, memory explosion on 50k file repos.\n\n', options: { color: TEXT_BODY } },
    { text: '3. Native Compiler Frontends (Clang / Javac) [REJECTED]\n', options: { bold: true, color: ACCENT_RED, fontSize: 9.5 } },
    { text: '   • Single-language bound; impossible to establish a uniform cross-language representation.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 1.9, w: 8.4, h: 2.7, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 20: Section 05 - Tool Selection 2: Taint Engine
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 22, 'Parameter 3 (3 M)', '6.2 TOOL JUSTIFICATION: TAINT ANALYSIS', 'Comparative Evaluation Matrix: Static Analysis & Taint Engines');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText([
    { text: 'CANDIDATE TAINT ENGINES EVALUATION:\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: '1. CodeQL (Java) + Custom AST Visitor Engine (Python) [SELECTED]\n', options: { bold: true, color: ACCENT_GREEN, fontSize: 9.5 } },
    { text: '   • Java Scalability: CodeQL provides battle-tested inter-procedural taint tracking across enterprise codebases.\n', options: { color: TEXT_BODY } },
    { text: '   • Python Agility: Custom AST visitor with type-stubs provides fine-grained control over dynamic dispatch.\n', options: { color: TEXT_BODY } },
    { text: '   • Feasibility Grounding: Reuses the proven backward dataflow architecture of CryptoGuard (CCS 2019) [P13].\n\n', options: { color: TEXT_BODY } },
    { text: '2. Soot / WALA [REJECTED]\n', options: { bold: true, color: ACCENT_RED, fontSize: 9.5 } },
    { text: '   • JVM-only legacy frameworks; unmaintainable setup complexity; zero capability for Python codebases.\n\n', options: { color: TEXT_BODY } },
    { text: '3. Semgrep OSS Standalone [INTEGRATED AS STAGE 1 FILTER ONLY]\n', options: { bold: true, color: ACCENT_BLUE, fontSize: 9.5 } },
    { text: '   • Fast pattern matching, but lacks inter-procedural taint propagation across multi-module boundaries.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 1.9, w: 8.4, h: 2.7, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 21: Section 05 - Tool Selection 3: PQC Library
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 23, 'Parameter 3 (3 M)', '6.3 TOOL JUSTIFICATION: PQC LIBRARY', 'Open Quantum Safe (liboqs) as Reference Standard');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addText([
    { text: 'POST-QUANTUM CRYPTOGRAPHIC LIBRARY SELECTION:\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: '1. Open Quantum Safe (liboqs & liboqs-python) [SELECTED]\n', options: { bold: true, color: ACCENT_GREEN, fontSize: 9.5 } },
    { text: '   • NIST Conformance: Complete, certified implementations of FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA).\n', options: { color: TEXT_BODY } },
    { text: '   • Native Hybrid Support: Standardized hybrid constructions (e.g. X25519 + ML-KEM-768).\n', options: { color: TEXT_BODY } },
    { text: '   • Cross-Language: C core with production-ready Python and Java (JNI) wrappers.\n', options: { color: TEXT_BODY } },
    { text: '   • Security: Actively audited for constant-time execution and memory safety.\n\n', options: { color: TEXT_BODY } },
    { text: '2. Bouncy Castle PQC [RETAINED FOR JAVA VERIFICATION]\n', options: { bold: true, color: ACCENT_BLUE, fontSize: 9.5 } },
    { text: '   • Established Java library; retained for secondary peer verification in Java environments.\n\n', options: { color: TEXT_BODY } },
    { text: '3. Custom / Bespoke Implementations [STRICTLY REJECTED]\n', options: { bold: true, color: ACCENT_RED, fontSize: 9.5 } },
    { text: '   • Rolling custom cryptography violates engineering discipline and introduces severe vulnerabilities.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 1.9, w: 8.4, h: 2.7, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 22: Section 05 - Tool Selection 4: CBOM Schema
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 24, 'Parameter 3 (3 M)', '6.4 TOOL JUSTIFICATION: CBOM STANDARD', 'OWASP CycloneDX 1.6 CBOM vs SPDX 3.0');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('OWASP CYCLONEDX 1.6 CBOM [SELECTED]', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  s.addText([
    { text: '• Formalised Cryptographic Model:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Dedicated cryptoProperties schema for algorithms, keys, protocols, and certification levels.\n\n', options: { color: TEXT_BODY } },
    { text: '• Global Industry Consensus:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Backed by IBM Research (Eurocrypt 2026 [P6]), CISA, and the European Cyber Resilience Act.\n\n', options: { color: TEXT_BODY } },
    { text: '• Rich Tooling & Validation:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Native CLI validators, JSON/XML schemas, and policy engine compatibility (P7).', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText('SPDX 3.0 SECURITY PROFILE [REJECTED]', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: ACCENT_RED, bold: true });
  s.addText([
    { text: '• Incomplete Cryptographic Profile:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Focuses predominantly on software package licenses; cryptographic assets remain generic annotations.\n\n', options: { color: TEXT_BODY } },
    { text: '• Immature Tooling Ecosystem:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Lacks specialized CBOM validators and policy verification engines.\n\n', options: { color: TEXT_BODY } },
    { text: '• Non-Aligned with US EO 14412:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  US federal minimum elements align directly with the CycloneDX CBOM specification.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 23: Section 05 - Tool Selection 5: Verification
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 25, 'Parameter 3 (3 M)', '6.5 TOOL JUSTIFICATION: VERIFICATION', 'Differential & Property Testing vs Formal Methods');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('DIFFERENTIAL TESTING + HYPOTHESIS [SELECTED]', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: ACCENT_GREEN, bold: true });
  s.addText([
    { text: '• 100% Automated Execution:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Executes original and patched code on identical input corpora, comparing outputs and exceptions.\n\n', options: { color: TEXT_BODY } },
    { text: '• Catches Subtle Downgrades:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Property-based testing (Hypothesis) tests parameter boundaries that round-trip testing misses.\n\n', options: { color: TEXT_BODY } },
    { text: '• Operates on Multi-File Repos:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Integrates seamlessly with existing CI/CD test runners.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText('FORMAL PROOF (DAFNY / F*) [REJECTED]', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: ACCENT_RED, bold: true });
  s.addText([
    { text: '• Extreme Real-World Infeasibility:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Requires formal mathematical specifications for every surrounding business module (<5% of codebases).\n\n', options: { color: TEXT_BODY } },
    { text: '• Does Not Scale to Python/Java:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Formal verification tools fail on real-world multi-file enterprise dependencies.\n\n', options: { color: TEXT_BODY } },
    { text: '• Soundness Limitation Stated Openly:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  We state differential testing as an empirical trade-off rather than claiming proof.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 24: Section 06 - Prototype: ~20% Milestone
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 26, 'Parameter 4 (3 M)', '7.1 INITIAL PROTOTYPE (~20% COMPLETION)', 'TRL 3 Working Proof-of-Concept in Repository');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('PROTOTYPE PACKAGE: crypto_agility_navigator', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: 'src/crypto_agility_navigator/\n', options: { fontFace: 'Courier New', color: ACCENT_BLUE, bold: true } },
    { text: '├── models.py       # Domain entities\n', options: { fontFace: 'Courier New', color: TEXT_BODY } },
    { text: '├── discovery.py    # AST scanner (Stage 1)\n', options: { fontFace: 'Courier New', color: TEXT_BODY } },
    { text: '├── dataflow.py     # Taint & retention (Stage 2)\n', options: { fontFace: 'Courier New', color: TEXT_BODY } },
    { text: '├── scorer.py       # HNDL & suppression (Stage 3)\n', options: { fontFace: 'Courier New', color: TEXT_BODY } },
    { text: '├── cbom.py         # CycloneDX 1.6 serializer\n', options: { fontFace: 'Courier New', color: TEXT_BODY } },
    { text: '└── cli.py          # CLI runner & reporting\n\n', options: { fontFace: 'Courier New', color: TEXT_BODY } },
    { text: '100% modular, fully tested, pure software.', options: { color: TEXT_WHITE, bold: true } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });

  s.addText('VERIFIED TRL 3 MILESTONE EVIDENCE', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• ~20% Implementation Completed:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '  Executable core engine covering AST discovery, backward/forward taint, retention extraction, and scoring.\n\n', options: { color: TEXT_BODY } },
    { text: '• Validated on Real Benchmark:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Successfully tested on payments/archive.py, web/session.py, and cache/etags.py.\n\n', options: { color: TEXT_BODY } },
    { text: '• Schema-Compliant CBOM Export:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Emits enriched CycloneDX 1.6 CBOM JSON.\n\n', options: { color: TEXT_BODY } },
    { text: '• Automated Test Harness: ', options: { bold: true, color: ACCENT_GREEN } },
    { text: '5/5 unit tests passing.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 25: Section 06 - Dashboard Screenshots
// -------------------------------------------------------------
// SLIDE 26: Section 06 - Benchmark Demonstration
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 27, 'Parameter 4 (3 M)', '7.2 BENCHMARK DEMONSTRATION', 'Discriminating Call Sites on examples/sample_project');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText([
    { text: 'CLI EXECUTION COMMAND:\n', options: { bold: true, color: TEXT_MUTED } },
    { text: '$ python3 -m src.crypto_agility_navigator.cli examples/sample_project --output-cbom examples/sample_cbom.json --show-suppressed\n\n', options: { fontFace: 'Courier New', color: ACCENT_BLUE, fontSize: 8.2 } },
    { text: 'TERMINAL OUTPUT TABLE:\n', options: { bold: true, color: TEXT_MUTED } },
    { text: 'RANK | ALGORITHM    | LOCATION        | RETENTION | EXPOSURE        | SCORE | URGENCY\n', options: { fontFace: 'Courier New', color: TEXT_WHITE, bold: true, fontSize: 7.8 } },
    { text: '---------------------------------------------------------------------------------------------\n', options: { fontFace: 'Courier New', color: BORDER_COLOR, fontSize: 7.8 } },
    { text: '1    | RSA-OAEP     | archive.py:11   | 10.0y     | EXTERNAL_PUBLIC | 33.3  | CRITICAL_IMMEDIATE (MOSCA BREACH)\n', options: { fontFace: 'Courier New', color: ACCENT_RED, bold: true, fontSize: 7.8 } },
    { text: '2    | RSA-OAEP     | session.py:11   | <1 hour   | INTERNAL_IPC    | 0.0   | LOW\n', options: { fontFace: 'Courier New', color: TEXT_BODY, fontSize: 7.8 } },
    { text: '3    | SHA-256      | etags.py:9      | <1 hour   | INTERNAL_IPC    | 0.0   | SUPPRESSED\n\n', options: { fontFace: 'Courier New', color: TEXT_MUTED, fontSize: 7.8 } },
    { text: 'SUMMARY: 3 discovered · 2 actionable · 1 context-suppressed (33% noise filtered) · 1 Mosca breach.', options: { bold: true, color: ACCENT_GREEN, fontSize: 8.5 } }
  ], { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 11 });
}

// -------------------------------------------------------------
// SLIDE 26: Section 06 - Discrimination Findings
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 28, 'Parameter 4 (3 M)', '7.3 ANALYSIS OF RESULTS', 'Empirical Proof of Discrimination & Noise Filtering');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('DISCRIMINATING IDENTICAL PRIMITIVES', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• The Baseline Failure:\n', options: { bold: true, color: ACCENT_RED } },
    { text: '  Crypsy [P1] and Shaw [P2] report archive.py and session.py identically as RSA-2048 with identical severity.\n\n', options: { color: TEXT_BODY } },
    { text: '• The Navigator Resolution:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '  Archive (Rank 1): Score 16.7, Mosca breach flagged (10y retention + 2y migration > 7y CRQC).\n\n', options: { color: TEXT_BODY } },
    { text: '  Session (Rank 2): Score 0.0, Low urgency (<1 hour cache TTL delivers zero risk reduction).', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });

  s.addText('AUTOMATED NOISE FILTERING', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• The False-Positive Trap:\n', options: { bold: true, color: ACCENT_RED } },
    { text: '  Crypsy reports SHA-256 in etags.py as an unmigrated hash finding, contributing to its ~0.30 precision.\n\n', options: { color: TEXT_BODY } },
    { text: '• Context-Based Reclassification:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '  Navigator traces the input (static bytes) and sink (ETag cache header), proving it has no security impact.\n\n', options: { color: TEXT_BODY } },
    { text: '• Status: SUPPRESSED (0.0 score);\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Removes manual triage overhead from security teams.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 27: Section 06 - CBOM JSON Schema Output
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 29, 'Parameter 4 (3 M)', '7.4 CYCLONEDX 1.6 CBOM EXPORT', 'Machine-Readable Bill of Materials with Dataflow Extensions');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText([
    { text: 'GENERATED CYCLONEDX 1.6 CBOM SNIPPET (examples/sample_cbom.json):\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 9.5 } },
    { text: '{\n  "bomFormat": "CycloneDX", "specVersion": "1.6",\n', options: { fontFace: 'Courier New', color: TEXT_MUTED, fontSize: 7.5 } },
    { text: '  "components": [{\n', options: { fontFace: 'Courier New', color: TEXT_MUTED, fontSize: 7.5 } },
    { text: '    "name": "RSA-OAEP", "type": "cryptographic-asset",\n', options: { fontFace: 'Courier New', color: TEXT_WHITE, fontSize: 7.5 } },
    { text: '    "cryptoProperties": {\n      "assetType": "algorithm", "classicalSecurityLevel": 2048, "nistQuantumSecurityLevel": 0\n    },\n', options: { fontFace: 'Courier New', color: ACCENT_BLUE, fontSize: 7.5 } },
    { text: '    "dataflowProperties": {\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, bold: true, fontSize: 7.5 } },
    { text: '      "plaintextSource": "database_read",\n      "ciphertextSink": "cloud_object_store",\n      "retentionEvidence": { "retentionYears": 10.0, "observed": true },\n      "exposureSurface": "EXTERNAL_PUBLIC",\n      "hndlRiskAssessment": { "normalizedScore": 16.67, "urgencyTier": "HIGH", "moscaViolated": true }\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, fontSize: 7.5 } },
    { text: '    }\n  }]\n}', options: { fontFace: 'Courier New', color: TEXT_MUTED, fontSize: 7.5 } }
  ], { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 8, fontFace: 'Arial', lineSpacing: 10 });
}

// -------------------------------------------------------------
// SLIDE 28: Section 06 - Unit Test Suite Evidence
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 30, 'Parameter 4 (3 M)', '7.5 AUTOMATED TEST HARNESS', '100% Pass Rate on Unit Testing (tests/test_navigator.py)');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText([
    { text: 'AUTOMATED UNIT TEST EXECUTION:\n', options: { bold: true, color: TEXT_MUTED } },
    { text: '$ python3 -m unittest discover -s tests -v\n\n', options: { fontFace: 'Courier New', color: ACCENT_BLUE, fontSize: 8.5 } },
    { text: 'test_cbom_generation (test_navigator.TestCryptoAgilityNavigator.test_cbom_generation) .................. ok\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, fontSize: 8 } },
    { text: 'test_context_noise_suppression (test_navigator.TestCryptoAgilityNavigator.test_context_noise_suppression) ok\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, fontSize: 8 } },
    { text: 'test_discovery_engine (test_navigator.TestCryptoAgilityNavigator.test_discovery_engine) ................ ok\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, fontSize: 8 } },
    { text: 'test_scoring_and_mosca_inequality (test_navigator.TestCryptoAgilityNavigator.test_scoring_and_mosca) ... ok\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, fontSize: 8 } },
    { text: 'test_semantic_binding_discrimination (test_navigator.TestCryptoAgilityNavigator.test_semantic_binding) . ok\n\n', options: { fontFace: 'Courier New', color: ACCENT_GREEN, fontSize: 8 } },
    { text: '----------------------------------------------------------------------\n', options: { fontFace: 'Courier New', color: BORDER_COLOR, fontSize: 8 } },
    { text: 'Ran 5 tests in 0.015s — ALL TESTS PASSED (OK)\n', options: { fontFace: 'Courier New', color: TEXT_WHITE, bold: true, fontSize: 8.5 } },
    { text: 'TRL 3 Proof of Concept Verified: Code base is reproducible, modular, and regression-tested.', options: { bold: true, color: ACCENT_GREEN, fontSize: 8.5 } }
  ], { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 11 });
}

// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 31, 'Parameter 4 (3 M)', '7.5 INTERACTIVE WEB DASHBOARD', 'Full-Stack React Dashboard & REST API');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  
  s.addText('WEB DASHBOARD (TRL 3 PROTOTYPE UI)', { x: 0.8, y: 1.8, w: 8.4, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Backend: ', options: { bold: true, color: ACCENT_BLUE } },
    { text: 'Python HTTP server providing /api/scan and /api/simulate-mosca endpoints.\n', options: { color: TEXT_BODY } },
    { text: '• Frontend: ', options: { bold: true, color: ACCENT_BLUE } },
    { text: 'Responsive HTML/React dashboard with vibrant dark mode aesthetics.\n', options: { color: TEXT_BODY } },
    { text: '• Capabilities: ', options: { bold: true, color: ACCENT_GREEN } },
    { text: 'Live dataflow visualization, Mosca risk scoring simulator, and CycloneDX export.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.15, w: 8.4, h: 0.6, fontSize: 9.5, fontFace: 'Arial', lineSpacing: 14 });

  try {
    s.addImage({ path: 'assets/dashboard.png', x: 0.8, y: 2.8, w: 4.0, h: 1.8, sizing: { type: 'contain' } });
    s.addImage({ path: 'assets/dashboard_results.png', x: 5.2, y: 2.8, w: 4.0, h: 1.8, sizing: { type: 'contain' } });
  } catch (e) {
    s.addText('[Screenshots will appear here during generation if assets/ is populated]', { x: 0.8, y: 3.5, w: 8.4, h: 0.3, fontSize: 9, color: TEXT_MUTED, align: 'center' });
  }
}
// -------------------------------------------------------------
// SLIDE 29: Section 07 - Innovation & Novelty Pillars
// -------------------------------------------------------------
// SLIDE 30: Section 07 - Mathematical Soundness & Feasibility
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 32, 'Parameter 5 (3 M)', '8.2 MATHEMATICAL DERIVATION & FEASIBILITY', 'Theoretical Soundness, Complexity Bounds & Fallbacks');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: 5.2, y: 1.7, w: 4.3, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText('THEORETICAL UTILITY MODEL', { x: 0.8, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Grounded in Decision Theory [P12]:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Adversary utility U(p) is proportional to whether data remains confidential at CRQC arrival:\n', options: { color: TEXT_BODY } },
    { text: '  U(p) ∝ max(0, x_p + y_p - z)\n\n', options: { fontFace: 'Courier New', color: ACCENT_BLUE, bold: true } },
    { text: '• Risk Reduction per Unit Effort:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Orders call sites by expected residual exposure reduction divided by remediation complexity.\n\n', options: { color: TEXT_BODY } },
    { text: '• Replaces Artificial VQE Circuits:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Shaw [P2] used decorative 2-qubit circuits; our formulation is transparent and provably grounded.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });

  s.addText('COMPUTATIONAL & MEMORY FEASIBILITY', { x: 5.5, y: 1.9, w: 3.7, h: 0.3, fontSize: 11, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
  s.addText([
    { text: '• Polynomial Time Complexity:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '  Discovery is O(N) over lines of code. Taint tracing is restricted to crypto call sites M ≪ N, yielding O(M · |V+E|).\n\n', options: { color: TEXT_BODY } },
    { text: '• Soundness vs Completeness Trade-off:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Targeting 70% dataflow coverage avoids state-space explosion on dynamic Python.\n\n', options: { color: TEXT_BODY } },
    { text: '• Auditable Insufficient Context:\n', options: { bold: true, color: TEXT_WHITE } },
    { text: '  Unresolvable sites placed in explicit audit bucket; tool never makes silent guesses.', options: { color: TEXT_BODY } }
  ], { x: 5.5, y: 2.25, w: 3.7, h: 2.3, fontSize: 8.2, fontFace: 'Arial', lineSpacing: 12 });
}

// -------------------------------------------------------------
// SLIDE 31: Section 07 - Patent Positioning
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 33, 'Parameter 5 (3 M)', '8.3 PATENT POSITIONING', 'Indian Patent Office CRI Guidelines (2025)');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText([
    { text: 'DEMONSTRABLE TECHNICAL EFFECT UNDER CRI GUIDELINES 2025:\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: '• The Legal Standard:\n', options: { bold: true, color: TEXT_MUTED } },
    { text: '  Under the Indian Patent Office CRI Guidelines (2025), computer-related inventions are patent-eligible if they exhibit a demonstrable technical effect beyond abstract algorithmic calculations.\n\n', options: { color: TEXT_BODY } },
    { text: '• Our Demonstrable Technical Effect:\n', options: { bold: true, color: ACCENT_GREEN } },
    { text: '  A statistically significant, measurable reduction in residual Harvest-Now-Decrypt-Later exposure per unit of engineering remediation effort, relative to algorithm-severity ordering.\n\n', options: { color: TEXT_WHITE, bold: true } },
    { text: '• Hard Project Commitment — Month 10 Provisional Filing:\n', options: { bold: true, color: ACCENT_RED } },
    { text: '  In India, pre-filing disclosure destroys novelty. Provisional patent application will be filed in Month 10 strictly BEFORE any public conference publication or preprint release.', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 1.9, w: 8.4, h: 2.7, fontSize: 8.5, fontFace: 'Arial', lineSpacing: 13 });
}

// -------------------------------------------------------------
// SLIDE 32: Section 08 - Project Roadmap
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 34, 'Parameter 6 (3 M)', '9.1 ACADEMIC YEAR MILESTONE ROADMAP', 'Seven-Review Milestone Progression (Fall & Winter Semesters)');

  const reviews = [
    { name: 'REVIEW I', date: 'Aug 2026', marks: '5 M', status: 'DONE', desc: 'Problem definition, literature review (P1–P16), formal objectives.' },
    { name: 'REVIEW II', date: 'Sep 2026', marks: '20 M', status: 'NOW', desc: '~20% Completion: system design, tool justification, working prototype (TRL 3).' },
    { name: 'REVIEW III', date: 'Oct 2026', marks: '10 M', status: 'NEXT', desc: '~30% Completion: panel observations follow-up, refined Java discovery.' },
    { name: 'REVIEW IV', date: 'Jan 2027', marks: '15 M', status: 'PLANNED', desc: '~50% Completion: full inter-procedural taint engine integrated across Python/Java.' },
    { name: 'REVIEW V', date: 'Mar 2027', marks: '25 M', status: 'PLANNED', desc: '~80% Completion: full integrated prototype, benchmark ranking evaluation.' },
    { name: 'REVIEW VI & VII', date: 'Apr 2027', marks: '25 M', status: 'PLANNED', desc: 'Open House external panel demo, final report, patent filing submission.' }
  ];

  reviews.forEach((r, idx) => {
    const x = 0.5 + idx * 1.5;
    const isCurrent = r.status === 'NOW';
    s.addShape(pres.ShapeType.rect, {
      x: x, y: 1.8, w: 1.45, h: 3.0,
      fill: { color: isCurrent ? '263238' : CARD_BG },
      line: { color: isCurrent ? ACCENT_BLUE : BORDER_COLOR, width: isCurrent ? 2 : 1 }
    });
    s.addText(r.name, { x: x + 0.08, y: 1.95, w: 1.3, h: 0.25, fontSize: 8.5, fontFace: 'Arial', color: isCurrent ? ACCENT_BLUE : TEXT_WHITE, bold: true });
    s.addText(r.marks, { x: x + 0.08, y: 2.2, w: 1.3, h: 0.3, fontSize: 13, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(r.date, { x: x + 0.08, y: 2.5, w: 1.3, h: 0.2, fontSize: 7.5, fontFace: 'Arial', color: TEXT_MUTED });
    s.addText(r.status, { x: x + 0.08, y: 2.75, w: 1.3, h: 0.2, fontSize: 7.5, fontFace: 'Arial', color: r.status === 'DONE' ? ACCENT_GREEN : (isCurrent ? ACCENT_BLUE : TEXT_MUTED), bold: true });
    s.addText(r.desc, { x: x + 0.08, y: 3.05, w: 1.3, h: 1.6, fontSize: 7.2, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 10 });
  });
}

// -------------------------------------------------------------
// SLIDE 33: Section 08 - Work Breakdown Structure
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 35, 'Parameter 6 (3 M)', '9.2 WORK BREAKDOWN STRUCTURE (WBS)', 'Equitable 3-Way Allocation Across Team Members');

  const members = [
    {
      name: 'AVI DHANDHANIA (25BCE1207)',
      role: 'Core Architecture, Dataflow Engine & UI Design',
      tasks: '• Stage 1 AST Discovery & constant propagation engine (discovery.py).\n• Stage 2 Inter-procedural Semantic Dataflow Engine (dataflow.py).\n• Built declarative retention extraction parsing S3 lifecycle & Redis TTLs.\n• Designed interactive Web Dashboard UI/UX and presentation deck architecture.\n• Authored Report Sections 4 (Requirements), 5 (Architecture), 6 (Tool Justification).\n• Next: Inter-procedural cross-module call graphs & CodeQL Java queries.'
    },
    {
      name: 'ANMOL SALUJA (25BCE1332)',
      role: 'Threat Modeling, HNDL Scoring & Verification Harness',
      tasks: '• Formalised Mosca inequality operationalisation & 16-paper literature gaps.\n• Formulated HNDL Exposure Scoring equation & Stage 3 Scoring Engine (scorer.py).\n• Implemented CycloneDX 1.6 CBOM Serializer (cbom.py, cli.py).\n• Full-Stack Backend Integration & REST API server (server.py).\n• Authored 100% passing automated unit test suite (tests/test_navigator.py).\n• Authored Report Sections 1, 2, 3, 8, 9, 10 & document sanitization.\n• Next: 15-repo benchmark curation & liboqs 3-gate patch verification harness.'
    }
  ];

  members.forEach((m, idx) => {
    const x = 0.5 + idx * 4.6;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 4.4, h: 3.0, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(m.name, { x: x + 0.2, y: 2.0, w: 4.0, h: 0.25, fontSize: 10, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText(m.role, { x: x + 0.2, y: 2.25, w: 4.0, h: 0.25, fontSize: 8.5, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText(m.tasks, { x: x + 0.2, y: 2.55, w: 4.0, h: 2.15, fontSize: 7.8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
  });
}

// -------------------------------------------------------------
// SLIDE 34: Section 08 - Risk Register & Checkpoints
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 36, 'Parameter 6 (3 M)', '9.3 RISK MANAGEMENT REGISTER', 'Proactive Trigger Checkpoints & Mitigation Strategies');

  const risks = [
    { id: 'RR1', title: 'Dataflow Coverage Low', trig: '<40% bound on first 3 repos', resp: 'Fall back to analyst-supplied retention per data class; propagate through dataflow.', gate: 'Month 5' },
    { id: 'RR2', title: 'Retention Absent in Config', trig: 'Fewer than 50% sinks have metadata', resp: 'Augment evidence sources via LLM-assisted docstring and commit parsing.', gate: 'Month 5' },
    { id: 'RR3', title: 'Expert Annotator Unavailable', trig: 'No confirmed labeller by Month 4', resp: 'Rubric-driven scoring by 2 team members + guide adjudication (report α).', gate: 'Month 4' },
    { id: 'RR4', title: 'Patch Synthesis Unreliable', trig: '<50% pass verification gate', resp: 'Deliver tool as diagnostic/prioritization engine; patch synthesis future work.', gate: 'Month 9' }
  ];

  risks.forEach((r, idx) => {
    const x = 0.5 + idx * 2.25;
    s.addShape(pres.ShapeType.rect, { x: x, y: 1.8, w: 2.15, h: 3.0, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(r.id, { x: x + 0.15, y: 2.0, w: 1.85, h: 0.25, fontSize: 12, fontFace: 'Arial', color: ACCENT_RED, bold: true });
    s.addText(r.title, { x: x + 0.15, y: 2.3, w: 1.85, h: 0.4, fontSize: 9.5, fontFace: 'Arial', color: TEXT_WHITE, bold: true });
    s.addText('TRIGGER: ' + r.trig, { x: x + 0.15, y: 2.75, w: 1.85, h: 0.45, fontSize: 7.5, fontFace: 'Arial', color: ACCENT_RED, lineSpacing: 10 });
    s.addText('RESPONSE: ' + r.resp, { x: x + 0.15, y: 3.25, w: 1.85, h: 0.9, fontSize: 7.8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
    s.addText('GATE: ' + r.gate, { x: x + 0.15, y: 4.25, w: 1.85, h: 0.3, fontSize: 8, fontFace: 'Arial', color: TEXT_MUTED, bold: true });
  });
}

// -------------------------------------------------------------
// SLIDE 35: Section 09 - Individual Contribution Matrix
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 37, 'Parameter 7 (2 M)', '10.1 INDIVIDUAL RESPONSIBILITIES', 'Individual Ownership & Technical Accountability');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });

  s.addText([
    { text: 'INDIVIDUAL EVIDENCE OF COMPLETED WORK (REVIEW II — 50/50 EQUITABLE SPLIT):\n\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: '• Avi Dhandhania (25BCE1207 — Lead Architect, Dataflow & UI):\n', options: { bold: true, color: ACCENT_BLUE, fontSize: 9.5 } },
    { text: '  - Designed the end-to-end 4-stage pipeline architecture and intermediate data contracts (models.py).\n', options: { color: TEXT_BODY } },
    { text: '  - Implemented the Stage 1 AST Discovery Engine (discovery.py) and constant propagation logic.\n', options: { color: TEXT_BODY } },
    { text: '  - Developed the Stage 2 Dataflow Binding Engine (dataflow.py), tracing plaintext sources and ciphertext sinks.\n', options: { color: TEXT_BODY } },
    { text: '  - Designed the interactive Web Dashboard UI/UX layout and visual component design.\n\n', options: { color: TEXT_BODY } },
    { text: '• Anmol Saluja (25BCE1332 — Threat Modeling, Scoring Engine, Testing & Backend Integration):\n', options: { bold: true, color: ACCENT_GREEN, fontSize: 9.5 } },
    { text: '• Avika Tyagi (25BCE1294 — Project Coordination, Requirement Analysis & Presentation Design):\n', options: { bold: true, color: '#F59E0B', fontSize: 9.5 } },
    { text: '  - Formalized the HNDL threat model, Mosca\'s inequality derivation, and 16-paper literature gap matrix.\n', options: { color: TEXT_BODY } },
    { text: '  - Implemented the Stage 3 HNDL Exposure Scoring Engine (scorer.py) and noise suppression filter.\n', options: { color: TEXT_BODY } },
    { text: '  - Developed the CycloneDX 1.6 CBOM Serializer (cbom.py, cli.py) with custom dataflow properties.\n', options: { color: TEXT_BODY } },
    { text: '  - Built full-stack REST API server (server.py) and 100% passing unit test suite (tests/test_navigator.py).', options: { color: TEXT_BODY } }
  ], { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 8, fontFace: 'Arial', lineSpacing: 11 });
}

// -------------------------------------------------------------
// SLIDE 36: Section 09 - Panel Defense Q&A Guide
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 38, 'Parameter 7 (2 M)', '10.2 PANEL DEFENSE & TECHNICAL Q&A', 'Anticipating Technical Inquiries from the School Panel');

  const qas = [
    { q: 'Q1: How do you handle dynamic typing in Python?', a: 'We target 70% dataflow coverage rather than claiming full mathematical soundness. We use constant propagation and typeshed stubs; unresolvable sites are placed in an explicit audit bucket rather than guessed.' },
    { q: 'Q2: Why not use algorithm-severity scores like Shaw [P2]?', a: 'Shaw\'s score is algorithm-intrinsic; all RSA-2048 sites receive identical scores. Only dataflow-derived retention distinguishes 10-year S3 archives (breached) from 15-minute tokens (low risk).' },
    { q: 'Q3: How do you guarantee PQC patches don\'t break code?', a: 'We use verified hybrid templates (X25519+ML-KEM) via liboqs, gated by differential equivalence testing on identical inputs, property tests for wrong-key failure, and downgrade resilience checks.' }
  ];

  qas.forEach((qa, idx) => {
    const y = 1.8 + idx * 1.05;
    s.addShape(pres.ShapeType.rect, { x: 0.5, y: y, w: 9.0, h: 0.95, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
    s.addText(qa.q, { x: 0.7, y: y + 0.1, w: 8.6, h: 0.25, fontSize: 9, fontFace: 'Arial', color: ACCENT_BLUE, bold: true });
    s.addText(qa.a, { x: 0.7, y: y + 0.35, w: 8.6, h: 0.55, fontSize: 7.8, fontFace: 'Arial', color: TEXT_BODY, lineSpacing: 11 });
  });
}

// -------------------------------------------------------------
// Generate and Save Presentation
// -------------------------------------------------------------
const outputFile = path.join(__dirname, '..', 'Crypto-Agility_Navigator_Review2.pptx');
console.log(`Writing Review 2 presentation to ${outputFile}...`);

pres.writeFile({ fileName: outputFile })
  .then(fileName => {
    console.log(`[+] Successfully generated Review 2 presentation: ${fileName}`);
  })
  .catch(err => {
    console.error('Error generating presentation:', err);
    process.exit(1);
  });

