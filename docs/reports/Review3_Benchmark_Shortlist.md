# Review III: Literature Survey Refresh & Benchmark Shortlist

## 1. Literature Survey Refresh
Since Review II, we have actively monitored ePrint and arXiv for late 2026 publications on PQC migration tooling. Two minor preprints have emerged regarding LLM-assisted code refactoring, but both remain confined to single-file synthetic snippets, confirming that our Stage 4 (multi-file, verified hybrid patches) remains a novel contribution. The baseline remains Näther & Hirsch's *Crypsy* tool, and our architectural choice to layer inter-procedural dataflow over AST discovery stands validated as the necessary next step.

## 2. Candidate Benchmark Repositories (N5)

For the public retention-annotated cryptographic benchmark (N5), we have shortlisted the following open-source repositories based on language (Python/Java), maturity, and active cryptographic use.

| Repository | Language | Description | Licence |
|---|---|---|---|
| `pallets/flask` | Python | Web framework with session/cookie crypto | BSD-3-Clause |
| `django/django` | Python | Web framework with auth, sessions, crypto | BSD-3-Clause |
| `psf/requests` | Python | HTTP library (TLS configurations) | Apache 2.0 |
| `pypa/warehouse` | Python | PyPI codebase, heavy credential/token use | Apache 2.0 |
| `ansible/ansible` | Python | Vault and secrets management | GPL-3.0 |
| `certbot/certbot` | Python | ACME client handling private keys/certs | Apache 2.0 |
| `mitmproxy/mitmproxy` | Python | TLS interception and certificate generation | MIT |
| `keycloak/keycloak` | Java | Identity and access management | Apache 2.0 |
| `spring-projects/spring-security` | Java | Authentication and access-control | Apache 2.0 |
| `bcgit/bc-java` | Java | Bouncy Castle Crypto APIs | MIT |
| `apache/tomcat` | Java | Web server with TLS/SSL connectors | Apache 2.0 |
| `apache/kafka` | Java | Data streaming with TLS and SASL auth | Apache 2.0 |
| `elastic/elasticsearch` | Java | Search engine with x-pack security | Elastic License |
| `hashicorp/vault` | Go (ref) | Secrets management (reference architecture) | MPL-2.0 |
| `google/tink` | Java/Python | Multi-language crypto API | Apache 2.0 |
| `aws/aws-encryption-sdk-python` | Python | Client-side encryption SDK | Apache 2.0 |
| `dabeaz/passlib` | Python | Password hashing library | BSD-3-Clause |
| `paramiko/paramiko` | Python | SSHv2 protocol implementation | LGPL-2.1 |
