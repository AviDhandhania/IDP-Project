# Review III: Panel Feedback Log and Work Plan Revisions

## Panel Feedback (From Review II)
1. **Section 1 & 4 (Requirements and Architecture)**: The panel noted that Java support was promised but not fully integrated into the AST parser in Review II. 
   - *Action taken*: Integrated `tree-sitter-java` into `discovery.py` to support multi-language scanning (Python and Java).
2. **Rule Corpus Scalability**: The panel observed that the initial 10 rules were insufficient for a production-grade tool.
   - *Action taken*: Expanded `KNOWN_CRYPTO_PATTERNS` to 145 items covering legacy, modern, and quantum-safe algorithms.
3. **S3/GCS Retention Extraction**: The panel requested support for explicit cloud provider APIs rather than just comments.
   - *Action taken*: Implemented regex extraction for boto3/GCS `Days` and `age` lifecycle parameters in `dataflow.py`.

## Work Plan Revisions
- Moved the **benchmark regression harness** forward to Review III (completed) to ensure stability while adding new rules.
- Pushed **ORM retention extraction** (SQLAlchemy, Django ORM) to Review IV to allocate more time for the 145+ rule expansion.
- The next major milestone (Review IV) will heavily focus on inter-procedural backward taint across multiple files, building upon the established `tree-sitter` foundation.

## Updated Requirements (Addressing Sections 1 & 4)
Based on panel feedback, the following Functional Requirements (FR) have been formally updated in our design:
* **FR-1 (Updated)**: Multi-language AST discovery must parse Python (`ast`) and Java (`tree-sitter`) source files, specifically detecting standard library calls and major third-party APIs (JCA, Bouncy Castle, cryptography.hazmat).
* **FR-5 (Updated)**: Retention policy extraction must ingest standard cloud lifecycle configuration objects (e.g. boto3 lifecycle configs, Google Cloud Storage lifecycle dicts) and reliably extract `Days` or `age` properties into numerical year equivalents for the Mosca equation.
