"""
Crypto-Agility Navigator - Discovery Engine (Stage 1)
Parses Abstract Syntax Trees (AST) of source code to detect cryptographic material,
artefacts, and invocations, identifying algorithms, key parameters, and call sites.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import tree_sitter
import tree_sitter_python as tspython
import tree_sitter_java as tsjava

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

class DiscoveryEngine:
    """Stage 1 Engine: Discovers cryptographic invocations across repository files."""

    def __init__(self):
        self.parsers = {
            ".py": tree_sitter.Parser(tree_sitter.Language(tspython.language())),
            ".java": tree_sitter.Parser(tree_sitter.Language(tsjava.language()))
        }

    def scan_file(self, file_path: str) -> List[CryptoInvocation]:
        path = Path(file_path)
        if not path.exists() or path.suffix not in self.parsers:
            return []
        try:
            with open(path, "rb") as f:
                code_bytes = f.read()
            
            source_lines = code_bytes.decode('utf-8').splitlines()
            parser = self.parsers[path.suffix]
            tree = parser.parse(code_bytes)
            
            invocations = []
            env = {} # Environment for constant propagation
            self._walk_tree(tree.root_node, code_bytes, source_lines, path.suffix, file_path, invocations, env)
            
            # Dedup by line number
            dedup = {}
            for inv in invocations:
                key = (inv.line_number, inv.algorithm_name)
                if key not in dedup:
                    dedup[key] = inv
            return list(dedup.values())
        except Exception as e:
            return []

    def scan_directory(self, dir_path: str) -> List[CryptoInvocation]:
        results: List[CryptoInvocation] = []
        path = Path(dir_path)
        for ext in self.parsers.keys():
            for f in path.rglob(f"*{ext}"):
                results.extend(self.scan_file(str(f)))
        return results

    def _walk_tree(self, node, code_bytes, source_lines, ext, file_path, invocations, env):
        # 1. Constant propagation update
        if ext == ".py" and node.type == "assignment":
            # Very basic string assignment tracking (e.g. cipher_algo = "RSA-OAEP")
            left = node.child_by_field_name("left")
            right = node.child_by_field_name("right")
            if left and right and left.type == "identifier" and right.type == "string":
                var_name = code_bytes[left.start_byte:left.end_byte].decode('utf-8')
                val = code_bytes[right.start_byte:right.end_byte].decode('utf-8').strip("'\"")
                env[var_name] = val
        
        elif ext == ".java" and node.type == "local_variable_declaration":
            # Basic java string assignment tracking
            declarator = None
            for child in node.children:
                if child.type == "variable_declarator":
                    declarator = child
                    break
            if declarator:
                left = declarator.child_by_field_name("name")
                right = declarator.child_by_field_name("value")
                if left and right and right.type == "string_literal":
                    var_name = code_bytes[left.start_byte:left.end_byte].decode('utf-8')
                    val = code_bytes[right.start_byte:right.end_byte].decode('utf-8').strip("'\"")
                    env[var_name] = val

        # 2. Call detection
        if (ext == ".py" and node.type == "call") or (ext == ".java" and node.type == "method_invocation"):
            call_name = self._get_call_name(node, code_bytes, ext)
            if call_name:
                matched_info = self._match_crypto_api(call_name, node, code_bytes, ext, env)
                if matched_info:
                    line_number = node.start_point[0] + 1
                    snippet = source_lines[node.start_point[0]].strip() if node.start_point[0] < len(source_lines) else ""
                    params = self._extract_call_parameters(node, code_bytes, ext, env)
                    
                    invocation = CryptoInvocation(
                        file_path=file_path,
                        line_number=line_number,
                        function_name=call_name,
                        primitive_type=matched_info["primitive"],
                        algorithm_name=matched_info["algo"],
                        key_size=matched_info["key_size"],
                        quantum_vulnerability=matched_info["vulnerability"],
                        raw_code_snippet=snippet,
                        parameters=params
                    )
                    invocations.append(invocation)

        # Traverse children
        for child in node.children:
            self._walk_tree(child, code_bytes, source_lines, ext, file_path, invocations, env)

    def _get_call_name(self, node, code_bytes, ext) -> Optional[str]:
        if ext == ".py":
            func = node.child_by_field_name("function")
            if func:
                return code_bytes[func.start_byte:func.end_byte].decode('utf-8')
        elif ext == ".java":
            obj_node = node.child_by_field_name("object")
            name_node = node.child_by_field_name("name")
            if obj_node and name_node:
                obj = code_bytes[obj_node.start_byte:obj_node.end_byte].decode('utf-8')
                name = code_bytes[name_node.start_byte:name_node.end_byte].decode('utf-8')
                return f"{obj}.{name}"
            elif name_node:
                return code_bytes[name_node.start_byte:name_node.end_byte].decode('utf-8')
        return None

    def _match_crypto_api(self, call_name: str, node, code_bytes, ext, env) -> Optional[Dict[str, Any]]:
        lower_name = call_name.lower()
        
        # Direct pattern match
        for pattern, info in KNOWN_CRYPTO_PATTERNS.items():
            if pattern in lower_name:
                return info
                
        # Heuristics based on name/args
        if "hashlib" in lower_name or ("MessageDigest.getInstance" in code_bytes[node.start_byte:node.end_byte].decode('utf-8')):
            algo = call_name.split(".")[-1].upper()
            
            # If java getInstance
            if "getInstance" in call_name:
                args = self._extract_call_parameters(node, code_bytes, ext, env)
                if "arg_0" in args:
                    algo = args["arg_0"].upper()

            vuln = QuantumVulnerability.GROVER_WEAKENED if algo in ["MD5", "SHA1", "SHA-1"] else QuantumVulnerability.QUANTUM_SAFE
            return {
                "primitive": CryptoPrimitiveType.HASH,
                "algo": algo,
                "key_size": 256 if "256" in algo else 128,
                "vulnerability": vuln
            }

        if "rsa" in lower_name and ("encrypt" in lower_name or "cipher" in lower_name):
            node_str = code_bytes[node.start_byte:node.end_byte].decode('utf-8').lower()
            algo = "RSA-2048"
            if "oaep" in node_str:
                algo = "RSA-OAEP"
            elif "pkcs1" in node_str:
                algo = "RSA-PKCS1v15"
            elif "pss" in node_str:
                algo = "RSA-PSS"

            return {
                "primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
                "algo": algo,
                "key_size": 2048,
                "vulnerability": QuantumVulnerability.SHOR_BROKEN
            }
            
        if "cipher.getinstance" in lower_name:
            args = self._extract_call_parameters(node, code_bytes, ext, env)
            if "arg_0" in args:
                algo_str = args["arg_0"].upper()
                if "RSA" in algo_str:
                    algo = "RSA-OAEP" if "OAEP" in algo_str else "RSA-PKCS1v15"
                    return {
                        "primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
                        "algo": algo,
                        "key_size": 2048,
                        "vulnerability": QuantumVulnerability.SHOR_BROKEN
                    }
                if "AES" in algo_str:
                    algo = "AES-256-GCM" if "GCM" in algo_str else "AES-128-CBC"
                    return {
                        "primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION,
                        "algo": algo,
                        "key_size": 256 if "GCM" in algo_str else 128,
                        "vulnerability": QuantumVulnerability.QUANTUM_SAFE if "GCM" in algo_str else QuantumVulnerability.GROVER_WEAKENED
                    }

        return None

    def _extract_call_parameters(self, node, code_bytes, ext, env) -> Dict[str, str]:
        params = {}
        if ext == ".py":
            args_node = node.child_by_field_name("arguments")
            if args_node:
                idx = 0
                for child in args_node.children:
                    if child.type not in ["(", ")", ","]:
                        val_str = code_bytes[child.start_byte:child.end_byte].decode('utf-8')
                        
                        # Apply constant propagation
                        if child.type == "identifier" and val_str in env:
                            val_str = env[val_str]
                        elif child.type == "string":
                            val_str = val_str.strip("'\"")
                            
                        # Handle kwargs
                        if child.type == "keyword_argument":
                            k = child.child_by_field_name("name")
                            v = child.child_by_field_name("value")
                            if k and v:
                                k_str = code_bytes[k.start_byte:k.end_byte].decode('utf-8')
                                v_str = code_bytes[v.start_byte:v.end_byte].decode('utf-8')
                                if v.type == "identifier" and v_str in env:
                                    v_str = env[v_str]
                                elif v.type == "string":
                                    v_str = v_str.strip("'\"")
                                params[k_str] = v_str
                        else:
                            params[f"arg_{idx}"] = val_str
                            idx += 1
                            
        elif ext == ".java":
            args_node = node.child_by_field_name("arguments")
            if args_node:
                idx = 0
                for child in args_node.children:
                    if child.type not in ["(", ")", ","]:
                        val_str = code_bytes[child.start_byte:child.end_byte].decode('utf-8')
                        if child.type == "identifier" and val_str in env:
                            val_str = env[val_str]
                        elif child.type == "string_literal":
                            val_str = val_str.strip("'\"")
                        params[f"arg_{idx}"] = val_str
                        idx += 1
                        
        return params
