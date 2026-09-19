# Review 2: 2-Person Work Breakdown Structure (WBS)

## Overview
- **Project:** Crypto-Agility Copilot: Dataflow-Aware Cryptographic Inventory and Prioritised Post-Quantum Migration
- **Target Milestone:** Review II (Initial Design and Development — 20 Marks)
- **Team Size:** 2 Members
- **Objective:** Provide a perfectly equitable (50/50) division of all Review 2 deliverables, covering the prototype implementation, theoretical research, report authoring, and presentation preparation.

---

## Avi Dhandhania (25BCE1207): Core Architecture, Dataflow Engine & System Design

**Focus Area:** Static analysis infrastructure, system architecture, and core data flow tracking.

### Code & Prototype (TRL 3)
- **Subsystem 1 (AST Discovery):** Developed the Tree-sitter/AST parsing engine (`discovery.py`) capable of locating cryptographic primitives across codebases and handling constant propagation.
- **Subsystem 2 (Semantic Binding):** Engineered the inter-procedural taint analysis (`dataflow.py`) that traces plaintext sources and ciphertext sinks.
- **Retention Extractor:** Built the declarative retention parser to identify lifecycle policies and TTLs from source code.

### Report & Documentation
- **Section 4 (Requirements):** Formulated the Functional and Non-Functional Requirements (FR/NFR) and stakeholder mapping.
- **Section 5 (System Architecture):** Architected the 4-stage pipeline and drafted the dataflow component schema.
- **Section 6 (Tool Justification):** Conducted and documented the comparative trade-off matrices for parsing frameworks (Tree-sitter vs. ANTLR) and static analysis tools.
- **Literature Review Verification:** Ensure the 16-paper Literature Review is prominently included and correctly formatted within the final Report 2.

### Presentation & Defense
- **Deck Design:** Created the base presentation layout, styling, and Slide generation script (`generate_review2_pptx.js`).
- **Panel Defense Preparation:** Prepared to defend the AST parsing choices, dataflow soundness, memory constraints, and architectural scalability.

---

## Anmol Saluja (25BCE1332): Threat Modeling, HNDL Scoring & Verification Harness

**Focus Area:** Mathematical risk scoring, compliance standards (CBOM), testing, and project novelty/literature gap.

### Code & Prototype (TRL 3)
- **Subsystem 3 (HNDL Scoring):** Programmed the scoring engine (`scorer.py`) that mathematically evaluates Mosca’s Inequality and computes the HNDL risk score based on retention and exposure.
- **CBOM Serialization:** Developed the standard CycloneDX 1.6 formatting and JSON generation module (`cbom.py`, `cli.py`).
- **Testing & Benchmark:** Authored the benchmark sample (S3 Archive vs Redis Cache) and the 100% passing automated unit test suite (`test_copilot.py`).
- **Front-End Integration:** Connect the python static analysis backend with the new front-end dashboard to display dynamic results.

### Report & Documentation
- **Sections 1 & 2 (Literature & Threat Model):** Wrote the formalization of Mosca’s Inequality, the Harvest-Now-Decrypt-Later (HNDL) framework, and the exhaustive 16-paper literature gap matrix.
- **Sections 3 & 8 (Innovation & Feasibility):** Authored the Five Pillars of Novelty (N1–N5) and defended the mathematical viability and patent eligibility (CRI guidelines).
- **Sections 9 & 10 (Planning & Teamwork):** Developed the academic year roadmap, risk register, and finalized the work breakdown structure.
- **Document Correction & Formatting:** Sanitize Report 2 to fix invalid characters, encoding issues, and ASCII tables that are not rendering properly in the final DOCX.
- **Asset Generation:** Capture and embed high-quality software screenshots (e.g., UI dashboard, pipeline outputs) into Report 2.

### Presentation & Defense
- **Content Synthesis:** Translated complex literature gaps, Mosca's math, and testing metrics into high-impact presentation slides.
- **Visual Evidence:** Add the new software screenshots into the light-theme PPTX to visually demonstrate the working prototype.
- **Panel Defense Preparation:** Prepared to defend the mathematical derivation of the scoring algorithm, literature research, and the regulatory/compliance urgency (RBI/CII deadlines).

---

## High-Level Matrix Summary

| Review 2 Deliverable Category | Avi Dhandhania (25BCE1207) | Anmol Saluja (25BCE1332) |
| :--- | :--- | :--- |
| **Research & Literature** | State-of-the-art tool evaluation (CodeQL, Tree-sitter) & Lit Review integration | Academic literature gap analysis (16 papers) & Threat Modeling |
| **System Architecture** | End-to-end Pipeline & Dataflow Design | HNDL Prioritisation Math & Patch Verification Harness |
| **Prototype Implementation** | AST Parsing, Taint Tracking, Front-End UI Dashboard | Mosca Scoring Engine, Unit Tests, Front-End Backend Integration |
| **Report Authoring** | Sections 4, 5, 6 (System & Tooling Specs) | Sections 1, 2, 3, 8, 9, 10 & Document Formatting/Fixes |
| **Presentation Deck** | Visual Design, PPTX Scripting & Light Theme Migration | Content Synthesis, Math Explanations & Adding Screenshots |
| **Overall Contribution %** | **50%** | **50%** |
