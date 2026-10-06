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
    "md2": {"primitive": CryptoPrimitiveType.HASH, "algo": "MD2", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "md4": {"primitive": CryptoPrimitiveType.HASH, "algo": "MD4", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "md5": {"primitive": CryptoPrimitiveType.HASH, "algo": "MD5", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "sha1": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA1", "key_size": 160, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "sha224": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA224", "key_size": 224, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha256": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA256", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha384": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA384", "key_size": 384, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha512": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA512", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha3_224": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA3_224", "key_size": 224, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha3_256": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA3_256", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha3_384": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA3_384", "key_size": 384, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sha3_512": {"primitive": CryptoPrimitiveType.HASH, "algo": "SHA3_512", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "blake2b": {"primitive": CryptoPrimitiveType.HASH, "algo": "BLAKE2B", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "blake2s": {"primitive": CryptoPrimitiveType.HASH, "algo": "BLAKE2S", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "blake3": {"primitive": CryptoPrimitiveType.HASH, "algo": "BLAKE3", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ripemd160": {"primitive": CryptoPrimitiveType.HASH, "algo": "RIPEMD160", "key_size": 160, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "whirlpool": {"primitive": CryptoPrimitiveType.HASH, "algo": "WHIRLPOOL", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "tiger": {"primitive": CryptoPrimitiveType.HASH, "algo": "TIGER", "key_size": 192, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-ECB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-CBC", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-CFB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-OFB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-CTR", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-GCM", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-CCM", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_128_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-128-POLY1305", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aes_192_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-ECB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-CBC", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-CFB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-OFB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-CTR", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-GCM", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-CCM", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_192_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-192-POLY1305", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-ECB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-CBC", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-CFB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-OFB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-CTR", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-GCM", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-CCM", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aes_256_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "AES-256-POLY1305", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_128_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-ECB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-CBC", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-CFB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-OFB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-CTR", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-GCM", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-CCM", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_128_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-128-POLY1305", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "camellia_192_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-ECB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-CBC", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-CFB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-OFB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-CTR", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-GCM", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-CCM", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_192_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-192-POLY1305", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-ECB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-CBC", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-CFB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-OFB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-CTR", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-GCM", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-CCM", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "camellia_256_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CAMELLIA-256-POLY1305", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_128_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-ECB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-CBC", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-CFB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-OFB", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-CTR", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-GCM", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-CCM", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_128_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-128-POLY1305", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "aria_192_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-ECB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-CBC", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-CFB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-OFB", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-CTR", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-GCM", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-CCM", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_192_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-192-POLY1305", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_ecb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-ECB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_cbc": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-CBC", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_cfb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-CFB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_ofb": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-OFB", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_ctr": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-CTR", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_gcm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-GCM", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_ccm": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-CCM", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "aria_256_poly1305": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "ARIA-256-POLY1305", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "des": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "DES", "key_size": 56, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "3des": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "3DES", "key_size": 112, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "blowfish": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "BLOWFISH", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "twofish": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "TWOFISH", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "rc4": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "RC4", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "chacha20": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "CHACHA20", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "salsa20": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "SALSA20", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "idea": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "IDEA", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "sm4": {"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "SM4", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "rsa": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "rsa_1024": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA_1024", "key_size": 1024, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "rsa_3072": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA_3072", "key_size": 3072, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "rsa_4096": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA_4096", "key_size": 4096, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "elgamal": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "ELGAMAL", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "sm2": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "SM2", "key_size": 256, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "kyber_512": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "KYBER_512", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "kyber_768": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "KYBER_768", "key_size": 768, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "kyber_1024": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "KYBER_1024", "key_size": 1024, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ml_kem_512": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "ML_KEM_512", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ml_kem_768": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "ML_KEM_768", "key_size": 768, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ml_kem_1024": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "ML_KEM_1024", "key_size": 1024, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ntru": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "NTRU", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "rsa_sign": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "RSA_SIGN", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "ecdsa": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "ECDSA", "key_size": 256, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "ed25519": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "ED25519", "key_size": 256, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "ed448": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "ED448", "key_size": 448, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "dsa": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "DSA", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "dilithium_2": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "DILITHIUM_2", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "dilithium_3": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "DILITHIUM_3", "key_size": 384, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "dilithium_5": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "DILITHIUM_5", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ml_dsa_44": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "ML_DSA_44", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ml_dsa_65": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "ML_DSA_65", "key_size": 384, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "ml_dsa_87": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "ML_DSA_87", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "falcon_512": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "FALCON_512", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "falcon_1024": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "FALCON_1024", "key_size": 1024, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "sphincs": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "SPHINCS", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "slh_dsa": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "SLH_DSA", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "dh": {"primitive": CryptoPrimitiveType.KEY_EXCHANGE, "algo": "DH", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "ecdh": {"primitive": CryptoPrimitiveType.KEY_EXCHANGE, "algo": "ECDH", "key_size": 256, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "x25519": {"primitive": CryptoPrimitiveType.KEY_EXCHANGE, "algo": "X25519", "key_size": 256, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "x448": {"primitive": CryptoPrimitiveType.KEY_EXCHANGE, "algo": "X448", "key_size": 448, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "kyber_kex": {"primitive": CryptoPrimitiveType.KEY_EXCHANGE, "algo": "KYBER_KEX", "key_size": 768, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "hmac_md5": {"primitive": CryptoPrimitiveType.MAC, "algo": "HMAC_MD5", "key_size": 128, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "hmac_sha1": {"primitive": CryptoPrimitiveType.MAC, "algo": "HMAC_SHA1", "key_size": 160, "vulnerability": QuantumVulnerability.GROVER_WEAKENED},
    "hmac_sha256": {"primitive": CryptoPrimitiveType.MAC, "algo": "HMAC_SHA256", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "hmac_sha512": {"primitive": CryptoPrimitiveType.MAC, "algo": "HMAC_SHA512", "key_size": 512, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "poly1305": {"primitive": CryptoPrimitiveType.MAC, "algo": "POLY1305", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "cmac_aes": {"primitive": CryptoPrimitiveType.MAC, "algo": "CMAC_AES", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "pbkdf2_hmac_sha256": {"primitive": CryptoPrimitiveType.KDF, "algo": "PBKDF2_HMAC_SHA256", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "scrypt": {"primitive": CryptoPrimitiveType.KDF, "algo": "SCRYPT", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "argon2": {"primitive": CryptoPrimitiveType.KDF, "algo": "ARGON2", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "hkdf_sha256": {"primitive": CryptoPrimitiveType.KDF, "algo": "HKDF_SHA256", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "bcrypt": {"primitive": CryptoPrimitiveType.KDF, "algo": "BCRYPT", "key_size": 192, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "rsa_oaep_encrypt": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA-OAEP", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "rsa_pkcs1v15_encrypt": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA-PKCS1v15", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN},
    "urlsafetimedserializer": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "HMAC", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE},
    "itsdangerous": {"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "HMAC", "key_size": 256, "vulnerability": QuantumVulnerability.QUANTUM_SAFE}
}


class CryptoASTVisitor(ast.NodeVisitor):
    """AST Visitor scanning Python files for cryptographic API invocations, with DFA-lite aliasing."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.invocations: List[CryptoInvocation] = []
        self.import_aliases: Dict[str, str] = {}
        self.assignments: Dict[str, str] = {}

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.name
            asname = alias.asname or name.split('.')[-1]
            self.import_aliases[asname] = name
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ''
        for alias in node.names:
            name = alias.name
            asname = alias.asname or name
            self.import_aliases[asname] = f"{module}.{name}"
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        # Very simple constant propagation for strings
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.assignments[target.id] = node.value.value
        self.generic_visit(node)

    def _resolve_name(self, name: str) -> str:
        parts = name.split('.')
        if parts[0] in self.import_aliases:
            parts[0] = self.import_aliases[parts[0]]
        return '.'.join(parts)

    def visit_Call(self, node: ast.Call) -> None:
        raw_call_name = self._get_call_name(node.func)
        if raw_call_name:
            full_call_name = self._resolve_name(raw_call_name)
            matched_info = self._match_crypto_api(full_call_name, node)
            if matched_info:
                snippet = self._get_code_snippet(node.lineno)
                params = self._extract_call_parameters(node)
                
                # Check if any params are resolved by DFA
                for k, v in params.items():
                    if v in self.assignments:
                        params[k] = self.assignments[v]
                        # Overwrite UNKNOWN algo if resolved
                        if matched_info["algo"] == "UNKNOWN":
                            resolved_algo = self.assignments[v].upper()
                            matched_info["algo"] = resolved_algo

                invocation = CryptoInvocation(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    function_name=full_call_name,
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
        lower_name = call_name.lower()
        
        # Check standard libraries like hashlib or cryptography.hazmat first
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

        # Fix False Negatives for cryptography library (Python Import Aliasing problem)
        if "generate_private_key" in lower_name:
            node_str = (ast.unparse(node) if hasattr(ast, 'unparse') else "").lower()
            algo = "UNKNOWN"
            if "rsa" in node_str or "rsa" in lower_name:
                algo = "RSA"
            elif "ec" in node_str or "ellipticcurve" in node_str or "ec." in node_str:
                algo = "ECDSA"
            elif "ed25519" in node_str:
                algo = "ED25519"
            elif "x25519" in node_str:
                algo = "X25519"
            
            return {
                "primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
                "algo": algo,
                "key_size": 2048,
                "vulnerability": QuantumVulnerability.SHOR_BROKEN
            }

        # Direct pattern match
        # Match longest pattern first to avoid generic names swallowing specific ones
        for pattern in sorted(KNOWN_CRYPTO_PATTERNS.keys(), key=len, reverse=True):
            # Use regex to ensure word boundaries (e.g., to prevent "dh" matching "addhandler" or "des" matching "description")
            # We replace '_' in pattern with `[_.:]` to allow separators, but for simple matching, 
            # we can just use `\b` around the pattern where the pattern's non-word characters are escaped.
            escaped_pattern = re.escape(pattern)
            # Since pattern might have underscores which are word characters, we can just check if it's isolated 
            # or part of a snake_case/camelCase/dot separated string.
            # A simple way: check if the pattern is surrounded by non-alphanumeric characters, or start/end of string.
            if re.search(r'(?:^|[^a-z0-9])' + escaped_pattern + r'(?:[^a-z0-9]|$)', lower_name):
                return KNOWN_CRYPTO_PATTERNS[pattern]

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
        self.java_parser = None
        try:
            import tree_sitter
            import tree_sitter_java
            self.java_parser = tree_sitter.Parser(tree_sitter.Language(tree_sitter_java.language()))
        except ImportError:
            pass

    def scan_file(self, file_path: str) -> List[CryptoInvocation]:
        path = Path(file_path)
        if not path.exists():
            return []
            
        if path.suffix == ".py":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                tree = ast.parse(code, filename=file_path)
                visitor = CryptoASTVisitor(file_path, code)
                visitor.visit(tree)
                return visitor.invocations
            except Exception:
                return []
        elif path.suffix in [".java", ".groovy"] and self.java_parser:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                tree = self.java_parser.parse(bytes(code, "utf-8"))
                return self._parse_java_tree(tree, file_path, code)
            except Exception:
                return []
        return []

    def _parse_java_tree(self, tree, file_path: str, code: str) -> List[CryptoInvocation]:
        invocations = []
        constants = {}
        
        # Pass 1: Constant Propagation (Find String Literals assigned to variables)
        def find_constants(node):
            if node.type == 'variable_declarator':
                name_node = None
                value_node = None
                for child in node.children:
                    if child.type == 'identifier':
                        name_node = child
                    elif child.type == 'string_literal':
                        value_node = child
                if name_node and value_node:
                    name = code[name_node.start_byte:name_node.end_byte]
                    val = code[value_node.start_byte:value_node.end_byte].strip('"')
                    constants[name] = val
            for child in node.children:
                find_constants(child)
        find_constants(tree.root_node)
        
        # Pass 2: Discovery
        def walk(node):
            if node.type == 'method_invocation':
                call_text = code[node.start_byte:node.end_byte]
                lower_call = call_text.lower()
                
                if "getinstance" in lower_call and ("cipher" in lower_call or "signature" in lower_call or "messagedigest" in lower_call or "keyagreement" in lower_call or "mac" in lower_call or "keygenerator" in lower_call or "keypairgenerator" in lower_call or "secretkeyfactory" in lower_call):
                    algo = "UNKNOWN"
                    primitive = CryptoPrimitiveType.SYMMETRIC_ENCRYPTION
                    vuln = QuantumVulnerability.SHOR_BROKEN
                    
                    # Extract arguments to check constants
                    arg_list = [c for c in node.children if c.type == 'argument_list']
                    if arg_list:
                        for arg in arg_list[0].children:
                            if arg.type == 'identifier':
                                arg_name = code[arg.start_byte:arg.end_byte]
                                if arg_name in constants:
                                    algo = constants[arg_name].upper()
                            elif arg.type == 'string_literal':
                                algo = code[arg.start_byte:arg.end_byte].strip('"').upper()
                    
                    if algo == "UNKNOWN":
                        if "rsa" in lower_call:
                            algo = "RSA"
                            primitive = CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION
                        elif "aes" in lower_call:
                            algo = "AES"
                            vuln = QuantumVulnerability.QUANTUM_SAFE
                        elif "sha-256" in lower_call:
                            algo = "SHA-256"
                            primitive = CryptoPrimitiveType.HASH
                            vuln = QuantumVulnerability.QUANTUM_SAFE
                        elif "ecdsa" in lower_call:
                            algo = "ECDSA"
                            primitive = CryptoPrimitiveType.SIGNATURE
                    else:
                        if "RSA" in algo:
                            primitive = CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION
                        elif "AES" in algo:
                            vuln = QuantumVulnerability.QUANTUM_SAFE
                        elif "SHA" in algo:
                            primitive = CryptoPrimitiveType.HASH
                            vuln = QuantumVulnerability.QUANTUM_SAFE
                            
                    invocations.append(CryptoInvocation(
                        file_path=file_path,
                        line_number=node.start_point[0] + 1,
                        function_name="getInstance",
                        primitive_type=primitive,
                        algorithm_name=algo,
                        key_size=None,
                        quantum_vulnerability=vuln,
                        raw_code_snippet=call_text.splitlines()[0],
                        parameters={}
                    ))
                elif "bouncycastleprovider" in lower_call:
                    invocations.append(CryptoInvocation(
                        file_path=file_path,
                        line_number=node.start_point[0] + 1,
                        function_name="BouncyCastleProvider",
                        primitive_type=CryptoPrimitiveType.SYMMETRIC_ENCRYPTION,
                        algorithm_name="BouncyCastle-Init",
                        key_size=None,
                        quantum_vulnerability=QuantumVulnerability.SHOR_BROKEN,
                        raw_code_snippet=call_text.splitlines()[0],
                        parameters={}
                    ))
                    
            for child in node.children:
                walk(child)
                
        walk(tree.root_node)
        return invocations
    def scan_directory(self, dir_path: str) -> List[CryptoInvocation]:
        results: List[CryptoInvocation] = []
        path = Path(dir_path)
        for src_file in path.rglob("*.*"):
            if src_file.suffix in [".py", ".java", ".groovy"]:
                results.extend(self.scan_file(str(src_file)))
        return results
