"""
Crypto-Agility Navigator - Semantic Binding Engine (Stage 2)
Performs backward taint analysis (plaintext -> source) and forward taint analysis (ciphertext -> sink),
extracts declarative retention evidence (TTL, S3 lifecycle, ORM), and binds cryptographic operations to data paths.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from .models import (
    CryptoInvocation,
    DataPath,
    SourceClassification,
    SinkClassification,
    ExposureSurface,
    RetentionEvidence,
    CryptoPrimitiveType
)


class DataflowBindingEngine:
    """Stage 2 Engine: Binds crypto invocations to protected data sources, sinks, and retention."""

    def __init__(self):
        pass

    def bind_invocation(self, invocation: CryptoInvocation) -> DataPath:
        """Analyzes the context of an invocation to construct a complete DataPath."""
        source_code = self._read_file(invocation.file_path)
        if not source_code:
            return self._create_fallback_datapath(invocation)

        # 1. Backward Analysis: Identify Plaintext Source
        plaintext_source = self._analyze_source(invocation, source_code)

        # 2. Forward Analysis: Identify Ciphertext Sink
        ciphertext_sink, exposure = self._analyze_sink_and_exposure(invocation, source_code)

        # 3. Retention Inference: Extract retention policy
        retention = self._infer_retention(invocation, ciphertext_sink, source_code)

        # 4. Context-Based Security Relevance
        is_security_relevant, reason = self._check_security_relevance(
            invocation, plaintext_source, ciphertext_sink
        )

        return DataPath(
            invocation=invocation,
            plaintext_source=plaintext_source,
            ciphertext_sink=ciphertext_sink,
            retention=retention,
            exposure=exposure,
            key_reuse_count=1,
            is_security_relevant=is_security_relevant,
            suppression_reason=reason
        )

    def _read_file(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _analyze_source(self, invocation: CryptoInvocation, source_code: str) -> SourceClassification:
        """Traces where the data entering the crypto call originated by inspecting assignment to the plaintext variable."""
        lines = source_code.splitlines()
        target_line_idx = invocation.line_number - 1

        # Extract the plaintext argument variable name (typically arg_0)
        plaintext_var = invocation.parameters.get("arg_0", "")

        # Look for assignment to this variable in previous lines
        assigned_expr = ""
        for i in range(target_line_idx - 1, max(-1, target_line_idx - 20), -1):
            line = lines[i].strip()
            # Strip comments
            code_part = line.split("#")[0].strip()
            if plaintext_var and code_part.startswith(f"{plaintext_var}") and "=" in code_part:
                assigned_expr = code_part.split("=", 1)[1].strip().lower()
                break

        target_context = assigned_expr if assigned_expr else "\n".join(lines[max(0, target_line_idx - 15):target_line_idx + 1]).lower()

        if any(kw in target_context for kw in ["token", "csrf", "random", "uuid", "nonce", "make_csrf"]):
            return SourceClassification.EPHEMERAL_TOKEN
        if any(kw in target_context for kw in ["settlement", "record", "db.query", "select ", "database", "orm"]):
            return SourceClassification.PERSISTENT_STORAGE
        if any(kw in target_context for kw in ["archive", "audit_log", "compliance"]):
            return SourceClassification.OFFSITE_ARCHIVE
        if any(kw in target_context for kw in ["password", "credential", "secret", "private_key"]):
            return SourceClassification.USER_CREDENTIAL
        if any(kw in target_context for kw in ["request.", "req.body", "params", "form."]):
            return SourceClassification.NETWORK_INPUT

        return SourceClassification.UNKNOWN

    def _analyze_sink_and_exposure(
        self, invocation: CryptoInvocation, source_code: str
    ) -> Tuple[SinkClassification, ExposureSurface]:
        """Traces forward to determine where the ciphertext/hash output terminates."""
        lines = source_code.splitlines()
        target_line_idx = invocation.line_number - 1

        # Check the 15 lines following the call site
        window_end = min(len(lines), target_line_idx + 15)
        window = "\n".join(lines[target_line_idx:window_end]).lower()

        # Cloud Object Store
        if any(kw in window for kw in ["s3.put_object", "boto3", "blob_client", "gcs.upload", "bucket"]):
            return SinkClassification.CLOUD_OBJECT_STORE, ExposureSurface.EXTERNAL_PUBLIC

        # In-Memory Cache with TTL
        if any(kw in window for kw in ["setex", "redis", "memcached", "cache"]):
            return SinkClassification.CACHE_TEMPORARY, ExposureSurface.INTERNAL_IPC

        # Database
        if any(kw in window for kw in ["db.commit", "cursor.execute", "session.add", "insert into"]):
            return SinkClassification.PERSISTENT_DATABASE, ExposureSurface.INTERNAL_CROSS_HOST

        # Network transmission
        if any(kw in window for kw in ["return jsonify", "response.write", "socket.send", "http"]):
            return SinkClassification.NETWORK_TRANSMIT, ExposureSurface.EXTERNAL_PUBLIC

        # Logging
        if any(kw in window for kw in ["logger.", "logging.", "log.info"]):
            return SinkClassification.LOCAL_LOG, ExposureSurface.INTERNAL_CROSS_HOST

        return SinkClassification.PROCESS_MEMORY, ExposureSurface.IN_PROCESS

    def _infer_retention(
        self, invocation: CryptoInvocation, sink: SinkClassification, source_code: str
    ) -> RetentionEvidence:
        """Recovers retention evidence from comments, constants, TTL calls, or sink priors."""
        lines = source_code.splitlines()
        target_line_idx = invocation.line_number - 1
        window_start = max(0, target_line_idx - 10)
        window_end = min(len(lines), target_line_idx + 15)
        window = "\n".join(lines[window_start:window_end])

        # Check for explicit S3 lifecycle / multi-year retention evidence (comments, bucket names, policies)
        m_years = (
            re.search(r"(?:retain|retention|vault|policy)[\w\s-]*?(\d+)\s*(?:years?|yr)", window, re.IGNORECASE) or
            re.search(r"(\d+)[ -]years?\s+(?:retention|statutory|lifecycle|policy|archive)", window, re.IGNORECASE) or
            re.search(r"(\d+)yr", window, re.IGNORECASE)
        )
        if m_years:
            years = float(m_years.group(1))
            return RetentionEvidence(
                retention_years=years,
                evidence_type="s3_lifecycle_policy",
                observed=True,
                description=f"Explicit cloud storage lifecycle: retain {years} years"
            )


        # Check for Redis TTL (e.g., redis.setex(k, 900, sealed))
        m_ttl = re.search(r"setex\s*\([^,]+,\s*(\d+)", window, re.IGNORECASE)
        if m_ttl:
            seconds = float(m_ttl.group(1))
            years = seconds / (365.25 * 86400)
            return RetentionEvidence(
                retention_years=years,
                evidence_type="redis_ttl",
                observed=True,
                description=f"Explicit cache TTL: {seconds} seconds (~{years:.5f} years)"
            )

        # Check for DDL / database column retention
        if sink == SinkClassification.CLOUD_OBJECT_STORE:
            return RetentionEvidence(
                retention_years=7.0,
                evidence_type="default_prior",
                observed=False,
                description="Cloud object store default prior (7-year statutory retention)"
            )
        elif sink == SinkClassification.PERSISTENT_DATABASE:
            return RetentionEvidence(
                retention_years=5.0,
                evidence_type="default_prior",
                observed=False,
                description="Relational database persistence prior (5 years)"
            )
        elif sink == SinkClassification.CACHE_TEMPORARY:
            return RetentionEvidence(
                retention_years=0.01,
                evidence_type="default_prior",
                observed=False,
                description="Temporary cache prior (approx. 3 days)"
            )
        elif sink == SinkClassification.LOCAL_LOG:
            return RetentionEvidence(
                retention_years=0.25,
                evidence_type="default_prior",
                observed=False,
                description="Standard log rotation prior (90 days)"
            )

        # Ephemeral / in-process default
        return RetentionEvidence(
            retention_years=0.001,
            evidence_type="default_prior",
            observed=False,
            description="Ephemeral in-memory duration"
        )

    def _check_security_relevance(
        self,
        invocation: CryptoInvocation,
        source: SourceClassification,
        sink: SinkClassification
    ) -> Tuple[bool, Optional[str]]:
        """Determines if the finding is actionable or a non-security usage (N3 suppression)."""
        # If it's a hash function (like SHA256 or MD5) used solely for caching or checksums
        if invocation.primitive_type == CryptoPrimitiveType.HASH:
            if source == SourceClassification.EPHEMERAL_TOKEN and sink == SinkClassification.CACHE_TEMPORARY:
                return False, "Hash used strictly for cache key generation without credential input"
            if "checksum" in invocation.raw_code_snippet.lower() or "etag" in invocation.raw_code_snippet.lower():
                return False, "Hash used strictly as content checksum or HTTP ETag"

        return True, None

    def _create_fallback_datapath(self, invocation: CryptoInvocation) -> DataPath:
        return DataPath(
            invocation=invocation,
            plaintext_source=SourceClassification.UNKNOWN,
            ciphertext_sink=SinkClassification.UNKNOWN,
            retention=RetentionEvidence(retention_years=1.0, evidence_type="unresolved_fallback", observed=False),
            exposure=ExposureSurface.INTERNAL_CROSS_HOST,
            key_reuse_count=1,
            is_security_relevant=True,
            suppression_reason=None
        )
