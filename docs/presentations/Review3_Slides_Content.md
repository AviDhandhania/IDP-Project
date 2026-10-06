# Review III Presentation Slides Outline

## Slide 1: Title Slide
* **Title:** Crypto-Agility Navigator: Dataflow-Aware Cryptographic Inventory and Prioritised Post-Quantum Migration
* **Subtitle:** Review III Update (30% Completion)
* **Team:** Avi Dhandhania, Anmol Saluja, Avika Tyagi
* **Guide:** Dr. E INIYA NEHRU

## Slide 2: Review III Milestones Achieved
* **Avi:** Added Java support to Stage 1 using `tree-sitter`, addressing panel feedback on multi-language capability.
* **Anmol:** Expanded discovery rule corpus to 145+ variants; integrated explicit S3/GCS lifecycle retention rules.
* **Avika:** Validated CBOM output against CycloneDX 1.6 schemas; built an automated benchmark regression harness.

## Slide 3: Expanding the Rule Corpus (Anmol)
* Scaled from 10 to 145+ cryptographic patterns.
* Coverage includes hashes, symmetric/asymmetric ciphers, key exchanges, MACs, KDFs, and quantum-safe algorithms.
* Resolves panel concerns about the scalability of the AST-based discovery engine.

## Slide 4: Cloud Lifecycle Retention Engine (Anmol)
* Upgraded `dataflow.py` to extract `Days` and `age` from raw `boto3` and GCS JSON/dict APIs.
* Translates cloud retention days directly into years for Mosca's Inequality: `x + y > z`.

## Slide 5: Java Support via Tree-Sitter (Avi)
* Integrated `tree-sitter` and `tree-sitter-java` bindings into `discovery.py`.
* Enables semantic parsing of `.java` files natively from Python.
* Extends capabilities to identify Java Cryptography Architecture (JCA) and Bouncy Castle signatures.

## Slide 6: Automated Quality Assurance (Avika)
* **CBOM Validation:** Python `jsonschema` dynamically validates JSON outputs against the official CycloneDX 1.6 spec.
* **Regression Harness:** End-to-end `unittest` ensuring dataflow mapping, noise-suppression, and ranking scores remain absolutely stable as rules expand.

## Slide 7: Non-Technical Updates & Next Steps
* Refreshed literature survey confirms our Stage 4 (verified patches) remains highly novel.
* 18 open-source repositories shortlisted for our public retention-annotated benchmark (N5).
* **Next for Review IV (50%):** Deep inter-procedural backward taint, ORM retention extraction, and CI integrations.
