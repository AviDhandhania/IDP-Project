"""
Crypto-Agility Navigator - Semantic Binding Engine (Stage 2)
Performs backward taint analysis (plaintext -> source) and forward taint analysis (ciphertext -> sink),
extracts declarative retention evidence (TTL, S3 lifecycle, ORM), and binds cryptographic operations to data paths.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import tree_sitter
import tree_sitter_python as tspython
import tree_sitter_java as tsjava

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
        self.parsers = {
            ".py": tree_sitter.Parser(tree_sitter.Language(tspython.language())),
            ".java": tree_sitter.Parser(tree_sitter.Language(tsjava.language()))
        }

    def bind_invocation(self, invocation: CryptoInvocation) -> DataPath:
        path = Path(invocation.file_path)
        if not path.exists() or path.suffix not in self.parsers:
            return self._create_fallback_datapath(invocation)

        try:
            with open(path, "rb") as f:
                code_bytes = f.read()
            parser = self.parsers[path.suffix]
            tree = parser.parse(code_bytes)
            
            # Structural Analysis
            plaintext_source = self._analyze_source(invocation, tree.root_node, code_bytes, path.suffix)
            ciphertext_sink, exposure = self._analyze_sink_and_exposure(invocation, tree.root_node, code_bytes, path.suffix)
            retention = self._infer_retention(invocation, ciphertext_sink, tree.root_node, code_bytes, path.suffix)
            
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
        except Exception as e:
            return self._create_fallback_datapath(invocation)

    def _analyze_source(self, invocation, root_node, code_bytes, ext) -> SourceClassification:
        plaintext_var = invocation.parameters.get("arg_0", "")
        if not plaintext_var:
            return SourceClassification.UNKNOWN

        # Find the assignment to plaintext_var before the invocation
        assigned_expr = ""
        target_line = invocation.line_number - 1 # 0-indexed

        def walk_assignments(node):
            nonlocal assigned_expr
            if node.start_point[0] >= target_line:
                return
            
            if ext == ".py" and node.type == "assignment":
                left = node.child_by_field_name("left")
                if left and code_bytes[left.start_byte:left.end_byte].decode('utf-8') == plaintext_var:
                    right = node.child_by_field_name("right")
                    if right:
                        assigned_expr = code_bytes[right.start_byte:right.end_byte].decode('utf-8').lower()
            
            for child in node.children:
                walk_assignments(child)
                
        walk_assignments(root_node)

        # Fallback to a window if no structural assignment found
        if not assigned_expr:
            try:
                lines = code_bytes.decode('utf-8').splitlines()
                assigned_expr = "\n".join(lines[max(0, target_line - 15):target_line + 1]).lower()
            except:
                pass

        if any(kw in assigned_expr for kw in ["token", "csrf", "random", "uuid", "nonce", "make_csrf"]):
            return SourceClassification.EPHEMERAL_TOKEN
        if any(kw in assigned_expr for kw in ["settlement", "record", "db.query", "select", "database", "orm"]):
            return SourceClassification.PERSISTENT_STORAGE
        if any(kw in assigned_expr for kw in ["archive", "audit_log", "compliance"]):
            return SourceClassification.OFFSITE_ARCHIVE
        if any(kw in assigned_expr for kw in ["password", "credential", "secret", "private_key"]):
            return SourceClassification.USER_CREDENTIAL
        if any(kw in assigned_expr for kw in ["request.", "req.body", "params", "form."]):
            return SourceClassification.NETWORK_INPUT

        return SourceClassification.UNKNOWN

    def _analyze_sink_and_exposure(self, invocation, root_node, code_bytes, ext) -> Tuple[SinkClassification, ExposureSurface]:
        target_line = invocation.line_number - 1
        
        # We will collect all function calls after the target line in the same scope/file
        calls_after = []
        def walk_calls(node):
            if node.start_point[0] >= target_line:
                if ext == ".py" and node.type == "call":
                    func = node.child_by_field_name("function")
                    if func:
                        calls_after.append(code_bytes[func.start_byte:func.end_byte].decode('utf-8').lower())
                elif ext == ".java" and node.type == "method_invocation":
                    obj_node = node.child_by_field_name("object")
                    name_node = node.child_by_field_name("name")
                    if name_node:
                        calls_after.append(code_bytes[name_node.start_byte:name_node.end_byte].decode('utf-8').lower())
            for child in node.children:
                walk_calls(child)
                
        walk_calls(root_node)
        
        window = " ".join(calls_after)
        
        # Fallback to string matching on following lines just in case
        if not calls_after:
            try:
                lines = code_bytes.decode('utf-8').splitlines()
                window = "\n".join(lines[target_line:min(len(lines), target_line + 15)]).lower()
            except:
                pass

        if any(kw in window for kw in ["put_object", "putobject", "boto3", "blob_client", "gcs.upload", "bucket"]):
            return SinkClassification.CLOUD_OBJECT_STORE, ExposureSurface.EXTERNAL_PUBLIC
        if any(kw in window for kw in ["setex", "redis", "memcached", "cache"]):
            return SinkClassification.CACHE_TEMPORARY, ExposureSurface.INTERNAL_IPC
        if any(kw in window for kw in ["db.commit", "cursor.execute", "session.add", "insert into"]):
            return SinkClassification.PERSISTENT_DATABASE, ExposureSurface.INTERNAL_CROSS_HOST
        if any(kw in window for kw in ["return jsonify", "response.write", "socket.send", "http"]):
            return SinkClassification.NETWORK_TRANSMIT, ExposureSurface.EXTERNAL_PUBLIC
        if any(kw in window for kw in ["logger.", "logging.", "log.info"]):
            return SinkClassification.LOCAL_LOG, ExposureSurface.INTERNAL_CROSS_HOST

        return SinkClassification.PROCESS_MEMORY, ExposureSurface.IN_PROCESS

    def _infer_retention(self, invocation, sink, root_node, code_bytes, ext) -> RetentionEvidence:
        target_line = invocation.line_number - 1
        
        # Look for setex call and extract TTL structurally
        if sink == SinkClassification.CACHE_TEMPORARY:
            ttl_val = None
            def walk_ttl(node):
                nonlocal ttl_val
                if node.start_point[0] >= target_line:
                    if ext == ".py" and node.type == "call":
                        func = node.child_by_field_name("function")
                        if func and "setex" in code_bytes[func.start_byte:func.end_byte].decode('utf-8').lower():
                            args_node = node.child_by_field_name("arguments")
                            if args_node and len(args_node.children) >= 4:
                                # arguments -> ( key , ttl , value )
                                # children: '(', key, ',', ttl, ',', value, ')' -> ttl is index 3
                                ttl_node = args_node.children[3]
                                try:
                                    ttl_val = float(code_bytes[ttl_node.start_byte:ttl_node.end_byte].decode('utf-8'))
                                except:
                                    pass
                for child in node.children:
                    walk_ttl(child)
            walk_ttl(root_node)
            
            if ttl_val is not None:
                years = ttl_val / (365.25 * 86400)
                return RetentionEvidence(
                    retention_years=years,
                    evidence_type="redis_ttl",
                    observed=True,
                    description=f"Explicit cache TTL: {ttl_val} seconds (~{years:.5f} years)"
                )
                
        # S3 lifecycle extraction (string based since it's in string literals or comments often)
        lines = code_bytes.decode('utf-8').splitlines()
        window = "\n".join(lines[max(0, target_line - 10):min(len(lines), target_line + 15)])
        
        import re
        m_years = (
            re.search(r"(?:retain|retention|vault|policy).*?(\d+)\s*(?:years?|yr)", window, re.IGNORECASE) or
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

        if sink == SinkClassification.CLOUD_OBJECT_STORE:
            return RetentionEvidence(retention_years=7.0, evidence_type="default_prior", observed=False, description="Cloud object store default prior (7-year statutory retention)")
        elif sink == SinkClassification.PERSISTENT_DATABASE:
            return RetentionEvidence(retention_years=5.0, evidence_type="default_prior", observed=False, description="Relational database persistence prior (5 years)")
        elif sink == SinkClassification.CACHE_TEMPORARY:
            return RetentionEvidence(retention_years=0.01, evidence_type="default_prior", observed=False, description="Temporary cache prior (approx. 3 days)")
        elif sink == SinkClassification.LOCAL_LOG:
            return RetentionEvidence(retention_years=0.25, evidence_type="default_prior", observed=False, description="Standard log rotation prior (90 days)")

        return RetentionEvidence(retention_years=0.001, evidence_type="default_prior", observed=False, description="Ephemeral in-memory duration")

    def _check_security_relevance(self, invocation, source, sink) -> Tuple[bool, Optional[str]]:
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
