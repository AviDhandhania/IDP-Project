"""
Crypto-Agility Navigator - Discovery Engine (Stage 1)
Parses Abstract Syntax Trees (AST) of source code to detect cryptographic material,
artefacts, and invocations, identifying algorithms, key parameters, and call sites.
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from .models import CryptoInvocation, CryptoPrimitiveType, QuantumVulnerability


# Known cryptographic signatures and library identifiers
KNOWN_CRYPTO_PATTERNS = {
    "rsa_oaep_encrypt": {
        "primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
        "algo": "RSA-OAEP",
        "key_size": 2048,
        "vulnerability": QuantumVulnerability.SHOR_BROKEN
    },
    "rsa_pkcs1v15_encrypt": {
        "primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
        "algo": "RSA-PKCS1v15",
        "key_size": 2048,
        "vulnerability": QuantumVulnerability.SHOR_BROKEN
    },
    "rsa_sign": {
        "primitive": CryptoPrimitiveType.SIGNATURE,
        "algo": "RSA-PSS",
        "key_size": 2048,
        "vulnerability": QuantumVulnerability.SHOR_BROKEN
    },
    "ecdsa_sign": {
        "primitive": CryptoPrimitiveType.SIGNATURE,
        "algo": "ECDSA-P256",
        "key_size": 256,
        "vulnerability": QuantumVulnerability.SHOR_BROKEN
    },
    "ecdh_exchange": {
        "primitive": CryptoPrimitiveType.KEY_EXCHANGE,
        "algo": "ECDH-X25519",
        "key_size": 256,
        "vulnerability": QuantumVulnerability.SHOR_BROKEN
    },
    "aes_gcm_encrypt": {
        "primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION,
        "algo": "AES-256-GCM",
        "key_size": 256,
        "vulnerability": QuantumVulnerability.QUANTUM_SAFE
    },
    "aes_cbc_encrypt": {
        "primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION,
        "algo": "AES-128-CBC",
        "key_size": 128,
        "vulnerability": QuantumVulnerability.GROVER_WEAKENED
    },
    "sha256": {
        "primitive": CryptoPrimitiveType.HASH,
        "algo": "SHA-256",
        "key_size": 256,
        "vulnerability": QuantumVulnerability.QUANTUM_SAFE
    },
    "sha1": {
        "primitive": CryptoPrimitiveType.HASH,
        "algo": "SHA-1",
        "key_size": 160,
        "vulnerability": QuantumVulnerability.GROVER_WEAKENED
    },
    "md5": {
        "primitive": CryptoPrimitiveType.HASH,
        "algo": "MD5",
        "key_size": 128,
        "vulnerability": QuantumVulnerability.GROVER_WEAKENED
    }
}


class CryptoASTVisitor(ast.NodeVisitor):
    """AST Visitor scanning Python files for cryptographic API invocations."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.invocations: List[CryptoInvocation] = []

    def visit_Call(self, node: ast.Call) -> None:
        call_name = self._get_call_name(node.func)
        if call_name:
            matched_info = self._match_crypto_api(call_name, node)
            if matched_info:
                snippet = self._get_code_snippet(node.lineno)
                params = self._extract_call_parameters(node)
                invocation = CryptoInvocation(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    function_name=call_name,
                    primitive_type=matched_info["primitive"],
                    algorithm_name=matched_info["algo"],
                    key_size=matched_info["key_size"],
                    quantum_vulnerability=matched_info["vulnerability"],
                    raw_code_snippet=snippet,
                    parameters=params
                )
                self.invocations.append(invocation)
        self.generic_visit(node)

    def _get_call_name(self, func_node: ast.AST) -> Optional[str]:
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            base = self._get_call_name(func_node.value)
            if base:
                return f"{base}.{func_node.attr}"
            return func_node.attr
        return None

    def _match_crypto_api(self, call_name: str, node: ast.Call) -> Optional[Dict[str, Any]]:
        # Direct pattern match
        lower_name = call_name.lower()
        for pattern, info in KNOWN_CRYPTO_PATTERNS.items():
            if pattern in lower_name:
                return info

        # Check standard libraries like hashlib or cryptography.hazmat
        if "hashlib" in lower_name:
            algo = call_name.split(".")[-1].upper()
            vuln = QuantumVulnerability.GROVER_WEAKENED if algo in ["MD5", "SHA1"] else QuantumVulnerability.QUANTUM_SAFE
            return {
                "primitive": CryptoPrimitiveType.HASH,
                "algo": algo,
                "key_size": 256 if "256" in algo else 128,
                "vulnerability": vuln
            }

        if "rsa" in lower_name and ("encrypt" in lower_name or "cipher" in lower_name):
            # Inspect node args/keywords to detect OAEP vs PKCS1v15 vs PSS
            node_str = (ast.unparse(node) if hasattr(ast, 'unparse') else "").lower()
            algo = "RSA-2048"
            if "oaep" in node_str or "oaep" in lower_name:
                algo = "RSA-OAEP"
            elif "pkcs1" in node_str or "pkcs1" in lower_name:
                algo = "RSA-PKCS1v15"
            elif "pss" in node_str or "pss" in lower_name:
                algo = "RSA-PSS"

            return {
                "primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
                "algo": algo,
                "key_size": 2048,
                "vulnerability": QuantumVulnerability.SHOR_BROKEN
            }

        return None


    def _get_code_snippet(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].strip()
        return ""

    def _extract_call_parameters(self, node: ast.Call) -> Dict[str, str]:
        params = {}
        for idx, arg in enumerate(node.args):
            arg_str = ast.unparse(arg) if hasattr(ast, 'unparse') else str(arg)
            params[f"arg_{idx}"] = arg_str
        for kw in node.keywords:
            val_str = ast.unparse(kw.value) if hasattr(ast, 'unparse') else str(kw.value)
            params[kw.arg or "kwarg"] = val_str
        return params


class DiscoveryEngine:
    """Stage 1 Engine: Discovers cryptographic invocations across repository files."""

    def __init__(self):
        pass

    def scan_file(self, file_path: str) -> List[CryptoInvocation]:
        path = Path(file_path)
        if not path.exists() or path.suffix != ".py":
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            tree = ast.parse(code, filename=file_path)
            visitor = CryptoASTVisitor(file_path, code)
            visitor.visit(tree)
            return visitor.invocations
        except Exception as e:
            # Handle unparsable files gracefully
            return []

    def scan_directory(self, dir_path: str) -> List[CryptoInvocation]:
        results: List[CryptoInvocation] = []
        path = Path(dir_path)
        for py_file in path.rglob("*.py"):
            results.extend(self.scan_file(str(py_file)))
        return results
