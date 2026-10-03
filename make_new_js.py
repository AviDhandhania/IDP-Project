import re
import json

base_js = """
const pptxgen = require('pptxgenjs');
const path = require('path');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// -------------------------------------------------------------
// Core Theme & Formatting Constants
// -------------------------------------------------------------
const BG_DARK = '0B0F19';
const CARD_BG = '131B2B';
const BORDER_COLOR = '2A3B5C';
const TEXT_WHITE = 'F8FAFC';
const TEXT_BODY = '94A3B8';
const TEXT_MUTED = '64748B';
const ACCENT_BLUE = '3B82F6';
const ACCENT_GREEN = '10B981';
const ACCENT_RED = 'EF4444';

const TOTAL_SLIDES = 28;

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
    { text: 'Avi Dhandhania (25BCE1207)  |  Anmol Saluja (25BCE1332)  |  Avika Tyagi (25BCE1294)\\n', options: { bold: true, color: TEXT_BODY } },
    { text: 'Guide: Dr. E INIYA NEHRU (54128), SCOPE\\n', options: { color: TEXT_MUTED } },
    { text: 'VIT Chennai Campus | Innovative Design Project | BACSE291', options: { color: TEXT_MUTED } }
  ], { x: 1.0, y: 4.0, w: 8.0, h: 1.0, fontSize: 12, fontFace: 'Arial', lineSpacing: 20 });
}
"""

slides_js = ""
slide_idx = 2

def add_slide(section_name, title, subtitle, content_text):
    global slide_idx
    code = f"""
{{
  const s = addSlideBase(pres, {slide_idx}, {json.dumps(section_name)}, {json.dumps(title)}, {json.dumps(subtitle)});
  s.addShape(pres.ShapeType.rect, {{ x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: {{ color: CARD_BG }}, line: {{ color: BORDER_COLOR, width: 1 }} }});
  s.addText({json.dumps(content_text)}, {{ x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Courier', color: TEXT_WHITE, lineSpacing: 18 }});
}}
"""
    global slides_js
    slides_js += code
    slide_idx += 1

add_slide("1. Executive Summary", "1.1 THE TECHNICAL PROBLEM", "The Unsolved Engineering Challenge", 
"Every enterprise software system depends on cryptography it cannot reliably enumerate or sequence for migration. A typical mid-sized banking or healthcare application invokes RSA, ECDSA, AES and SHA-family primitives from a complex mixture of sources.\n\n"
"Peter Shor's algorithm renders classical public-key cryptography insecure on a CRQC. NIST has standardised post-quantum replacements (FIPS 203, 204, 205).\n\n"
"The unsolved engineering challenge: an organisation cannot migrate what it cannot locate, and cannot sequence a multi-year migration without knowing which of its thousands of cryptographic call sites are actually dangerous."
)

add_slide("1. Executive Summary", "1.1 THREAT MODEL", "Harvest-Now-Decrypt-Later (HNDL)",
"The urgency is set by the Harvest-Now-Decrypt-Later (HNDL) threat model.\n\n"
"A passive adversary intercepts and stores encrypted network traffic and database backups today at negligible storage cost, intending to decrypt the captured ciphertext once a CRQC becomes operational.\n\n"
"Detection after the fact provides no remedy, and forward secrecy cannot protect data retroactively."
)

add_slide("1. Executive Summary", "1.2 SPECIFIC GAP IN TOOLING", "Semantically Flat Outputs",
"Cryptographic inventory scanners have recently emerged (CBOMkit, Crypsy), standardising around CycloneDX 1.6 CBOM. However, output is semantically flat.\n\n"
"1. Findings are not actionable (noise). Over two-thirds of reported findings are noise, predominantly non-security hashing matched by heuristic rules.\n\n"
"2. Findings are not ordered (flat scoring). Where risk scoring exists, it is algorithm-intrinsic. Every RSA-2048 call site receives an identical score, offering no prioritisation signal."
)

add_slide("1. Executive Summary", "1.3 FORMALISATION", "Mosca's Inequality",
"The migration deadline is formalised by Mosca's inequality. For a given data path, let:\n"
"• x = data confidentiality lifetime (years the data must remain secret)\n"
"• y = migration duration (years required to re-engineer the system)\n"
"• z = CRQC operational horizon\n\n"
"A data path is already breached today if: x + y > z\n\n"
"Critically, x is a property of the data being protected, not of the cipher."
)

add_slide("1. Executive Summary", "1.4 REGULATORY JUSTIFICATION", "Compliance Urgency",
"1. India Critical Information Infrastructure (CII) deadline (2027–2029).\n"
"2. Reserve Bank of India (RBI) Q-SAFE Committee.\n"
"3. SEBI Cyber Security and Cyber Resilience Framework (CSCRF).\n"
"4. US Executive Order 14412 (June 2026).\n"
"5. NIST final standards (FIPS 203, 204, 205)."
)

add_slide("2. Literature Survey", "2.1 METHODOLOGY & 2.2 SUMMARY", "16 Core Papers Surveyed",
"Survey across ACM Digital Library, IEEE Xplore, IACR Cryptology ePrint, arXiv and Springer (Jan 2024–Aug 2026).\n\n"
"Key baselines:\n"
"• P1 Crypsy: 214-rule static scanner; real-world actionable precision ≈ 0.30.\n"
"• P2 Shaw: Regex detection with VQE threat score; algorithm-only scoring.\n"
"• P3 Pallarés et al.: LLM-based migration; degrades sharply on multi-file repos.\n"
"• P13 CryptoGuard: Backward inter-procedural dataflow analysis at scale."
)

add_slide("2. Literature Survey", "2.3 CRITICAL ANALYSIS", "What Prior Work Gets Wrong",
"Critique of P1 (Crypsy):\n"
"Flaw: Context-blindness, no dataflow, no prioritisation.\n"
"Correction: Inter-procedural semantic dataflow with HNDL Exposure Score.\n\n"
"Critique of P2 (Shaw):\n"
"Flaw: Score cannot discriminate identical algorithms.\n"
"Correction: Score based on protected data path.\n\n"
"Critique of P3 (Pallarés):\n"
"Flaw: Synthetic single-fragment ceiling, superficial verification.\n"
"Correction: Verified hybrid templates with differential equivalence testing."
)

add_slide("3. Project Objectives", "3.1 PRIMARY OBJECTIVES", "O1 to O7",
"O1: Multi-language discovery. F1 ≥ 0.85.\n"
"O2: Semantic dataflow binding. ≥ 70% binding.\n"
"O3: HNDL exposure scoring. nDCG@20 ≥ 0.80.\n"
"O4: Noise suppression. Actionable precision ≥ 0.70.\n"
"O5: Verified hybrid patch synthesis. ≥ 80% pass rate.\n"
"O6: Public benchmark release.\n"
"O7: Evaluation methodology standardisation."
)

add_slide("3. Project Objectives", "3.2 PILLARS OF NOVELTY", "N1 to N5",
"N1: Retention-aware cryptographic dataflow binding.\n"
"N2: Call-site-discriminating risk score and ranking metric.\n"
"N3: Dataflow-conditioned noise suppression.\n"
"N4: Differentially verified hybrid patch synthesis.\n"
"N5: Public retention-annotated benchmark."
)

add_slide("4. Requirement Analysis", "4.1 STAKEHOLDERS & 4.2 FRs", "Functional Requirements",
"Stakeholders: CISO, DevSecOps, Software Developers.\n\n"
"FR-1: Multi-language AST discovery.\n"
"FR-2: Constant propagation and type inference.\n"
"FR-3/FR-4: Backward and forward taint tracing.\n"
"FR-5: Retention policy extraction.\n"
"FR-6: HNDL scoring and Mosca evaluation.\n"
"FR-7: Context noise suppression.\n"
"FR-8: Hybrid patch synthesis and verification."
)

add_slide("4. Requirement Analysis", "4.3 NON-FUNCTIONAL REQUIREMENTS", "NFRs",
"NFR-1: Scanning throughput (50k files in <10 mins).\n"
"NFR-2: Memory footprint (<4 GB peak RAM).\n"
"NFR-3: No specialised hardware (pure software).\n"
"NFR-4: Provenance integrity (observed vs inferred).\n"
"NFR-5: Graceful fallback and soundness (audit bucket).\n"
"NFR-6: Schema conformance (CycloneDX 1.6 CBOM)."
)

add_slide("5. System Design", "5.1 END-TO-END PIPELINE", "Four-Stage Architecture",
"The system is a four-stage pipeline. Each stage consumes structured output of the previous stage:\n\n"
"1. Multi-Language Cryptographic Discovery Layer\n"
"2. Inter-Procedural Semantic Dataflow and Retention Engine\n"
"3. HNDL Prioritisation, Scoring and Noise Suppression\n"
"4. Hybrid Patch Synthesis and Differential Verification"
)

add_slide("5. System Design", "5.2 & 5.3 DISCOVERY AND DATAFLOW", "Subsystems 1 and 2",
"Subsystem 1 — Discovery Layer\n"
"• Tree-sitter + Python ast module.\n"
"• Extensible rule corpus for cryptographic namespaces.\n"
"• Constant propagation.\n\n"
"Subsystem 2 — Dataflow Engine\n"
"• Formal dataflow lattice propagating over CFGs.\n"
"• Backward taint from arguments to sources.\n"
"• Forward taint from outputs to sinks.\n"
"• Declarative retention extractor (e.g. redis TTLs, S3 rules)."
)

add_slide("5. System Design", "5.4 SCORING AND SUPPRESSION", "Subsystem 3",
"HNDL Exposure Score:\n"
"Exposure(p) = w_r·R(p) × w_e·E(p) × w_a·A(p) × w_k·K(p)\n\n"
"• Mosca breach flagged if: RetentionYears + MigrationYears > CRQCHorizon.\n"
"• Noise suppression reclassifies non-security hashing."
)

add_slide("5. System Design", "5.5 PATCHING & 5.6 SCHEMA", "Subsystems 4 and Data",
"Subsystem 4 — Verified Patching\n"
"• Hybrid templates (e.g. X25519 + ML-KEM-768) via liboqs.\n"
"• 3 Gates: Differential equivalence, Property testing, Downgrade resistance.\n\n"
"5.6 Data Schema\n"
"• Emits CycloneDX 1.6 CBOM enriched with cryptoProperties and custom dataflowProperties."
)

add_slide("6. Component Selection", "6.1 & 6.2 PARSING & TAINT", "Technical Justification",
"6.1 Parsing Infrastructure:\n"
"Selected: Tree-sitter + Python ast (Multi-language, High throughput, robust to errors).\n"
"Rejected: ANTLR4, Compiler front-ends.\n\n"
"6.2 Static Analysis & Taint:\n"
"Selected: CodeQL (Java) + AST visitor (Python).\n"
"Rejected: Soot/WALA, Semgrep OSS (intra-procedural only)."
)

add_slide("6. Component Selection", "6.3, 6.4, 6.5 TOOLS", "PQC, CBOM & Verification",
"6.3 PQC Library:\n"
"Selected: Open Quantum Safe (liboqs). Full NIST FIPS 203/204/205 conformance.\n\n"
"6.4 CBOM Schema:\n"
"Selected: OWASP CycloneDX 1.6 CBOM.\n\n"
"6.5 Patch Verification Strategy:\n"
"Selected: Differential testing + property tests.\n"
"Rejected: Formal verification (Dafny, F*) due to real-world infeasibility."
)

add_slide("7. Initial Prototype", "7.1 IMPLEMENTED PACKAGE STRUCTURE", "TRL 3 Prototype",
"src/crypto_agility_navigator/\n"
"├── models.py      # domain models\n"
"├── discovery.py   # Stage 1: AST scanner\n"
"├── dataflow.py    # Stage 2: backward/forward taint\n"
"├── scorer.py      # Stage 3: HNDL exposure scoring\n"
"├── cbom.py        # CycloneDX 1.6 CBOM serialiser\n"
"├── cli.py         # CLI and reporting\n"
"└── server.py      # REST API\n"
"tests/test_navigator.py       # 100% passing tests\n"
"examples/sample_project/      # Benchmark example"
)

add_slide("7. Initial Prototype", "7.3 EMPIRICAL VALIDATION", "CLI Benchmark Output",
"CLI Output on sample_project:\n"
"Discovered 3 cryptographic invocation(s).\n\n"
"RANK  ALGORITHM  LOCATION        RETENTION  EXPOSURE         SCORE  URGENCY\n"
"----------------------------------------------------------------------------------\n"
"1     RSA-OAEP   archive.py:11   10.0y      EXTERNAL_PUBLIC  16.7   HIGH (MOSCA BREACH)\n"
"2     RSA-OAEP   session.py:11   <1 hour    INTERNAL_IPC     0.0    LOW\n"
"3     SHA-256    etags.py:9      <1 hour    INTERNAL_IPC     0.0    SUPPRESSED\n\n"
"Two identical RSA-OAEP sites are correctly discriminated by retention and exposure."
)

add_slide("7. Initial Prototype", "7.4 & 7.5 TESTING AND UI", "Tests and Dashboard",
"7.4 Automated Unit Test Suite\n"
"• 8 automated unit tests covering Stage 1-3 pipeline.\n"
"• 100% passing rate on tests/test_navigator.py.\n\n"
"7.5 Interactive Web Dashboard\n"
"• Python http.server REST API + React SPA.\n"
"• Features: KPI overview, Prioritisation table, Dataflow visualiser, Mosca simulation engine, Live AST scanner, CBOM inspector."
)

add_slide("8. Innovation & Feasibility", "8.1 & 8.2 INNOVATION AND FEASIBILITY", "Mathematical Basis & Soundness",
"8.1 Mathematical Basis:\n"
"U(p) ∝ max(0, xp + yp − z)\n"
"Ranks data paths by expected residual exposure under delayed remediation.\n\n"
"8.2 Soundness vs Completeness:\n"
"Targets ≥ 70% dataflow coverage. Unresolvable paths go to an explicit audit bucket.\n\n"
"8.3 Computational Feasibility:\n"
"O(N) discovery. Polynomial inter-procedural taint. <4GB memory."
)

add_slide("9. Project Planning", "9.1 & 9.2 WORK DIVISION PRINCIPLE", "Review II (Completed)",
"9.1 Work Division Principle\n"
"Equitable split of technical and non-technical work across 3 members.\n\n"
"9.2 Work Division for Review II\n"
"• Avi Dhandhania: Stage 1 AST discovery, backward taint tracing. Sections 1, 4, 5.\n"
"• Anmol Saluja: Forward taint tracing, retention extractor, Stage 3 HNDL scoring. Sections 2, 3, 6, 8.\n"
"• Avika Tyagi: CBOM serialiser, CLI, REST API, Web dashboard, tests. Sections 7, 9, 10."
)

add_slide("9. Project Planning", "9.3 WORK PLAN FOR FUTURE REVIEWS", "Review III to VI",
"• Review III (≈ 30%): Java support (Tree-sitter), Expand rule corpus, CBOM validation.\n"
"• Review IV (≈ 50%): Inter-procedural Java taint (CodeQL), ORM retention extraction, CI integration.\n"
"• Review V-VI (≈ 80-100%): Three-gate patch verification harness, nDCG ranking evaluation, Hybrid patch templates (X25519 + ML-KEM), Final public benchmark release."
)

add_slide("10. References", "10. REFERENCES", "Standards",
"10.2 Regulatory and Standards References:\n"
"• NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA)\n"
"• OWASP CycloneDX 1.6 CBOM Specification\n"
"• RBI Q-SAFE Committee Terms of Reference (2026)\n"
"• SEBI Cyber Security and Cyber Resilience Framework (CSCRF)\n"
"• US Executive Order 14412 on Cryptography Bills of Materials (June 2026)\n"
"• Indian Patent Office CRI Guidelines (2025)"
)

# Output generation
final_js = base_js + slides_js + """
const outputFile = path.join(__dirname, '..', 'Crypto-Agility_Navigator_Review2.pptx');
pres.writeFile({ fileName: outputFile }).then(fileName => {
    console.log(`[+] Successfully generated Review 2 presentation: ${fileName}`);
});
"""

# Update TOTAL_SLIDES
final_js = final_js.replace("const TOTAL_SLIDES = 28;", f"const TOTAL_SLIDES = {slide_idx - 1};")

with open("scripts/generate_review2_pptx_from_scratch.js", "w") as f:
    f.write(final_js)

print(f"Generated JS for {slide_idx - 1} slides")
