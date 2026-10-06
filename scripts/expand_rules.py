import re
import random

# Base algorithms
hashes = [
    ("md2", 128, "GROVER_WEAKENED"), ("md4", 128, "GROVER_WEAKENED"), ("md5", 128, "GROVER_WEAKENED"),
    ("sha1", 160, "GROVER_WEAKENED"), ("sha224", 224, "QUANTUM_SAFE"), ("sha256", 256, "QUANTUM_SAFE"),
    ("sha384", 384, "QUANTUM_SAFE"), ("sha512", 512, "QUANTUM_SAFE"),
    ("sha3_224", 224, "QUANTUM_SAFE"), ("sha3_256", 256, "QUANTUM_SAFE"),
    ("sha3_384", 384, "QUANTUM_SAFE"), ("sha3_512", 512, "QUANTUM_SAFE"),
    ("blake2b", 512, "QUANTUM_SAFE"), ("blake2s", 256, "QUANTUM_SAFE"),
    ("blake3", 256, "QUANTUM_SAFE"), ("ripemd160", 160, "GROVER_WEAKENED"),
    ("whirlpool", 512, "QUANTUM_SAFE"), ("tiger", 192, "GROVER_WEAKENED")
]

sym_ciphers = [
    ("aes_128", 128, "GROVER_WEAKENED"), ("aes_192", 192, "QUANTUM_SAFE"), ("aes_256", 256, "QUANTUM_SAFE"),
    ("camellia_128", 128, "GROVER_WEAKENED"), ("camellia_192", 192, "QUANTUM_SAFE"), ("camellia_256", 256, "QUANTUM_SAFE"),
    ("aria_128", 128, "GROVER_WEAKENED"), ("aria_192", 192, "QUANTUM_SAFE"), ("aria_256", 256, "QUANTUM_SAFE"),
    ("des", 56, "GROVER_WEAKENED"), ("3des", 112, "GROVER_WEAKENED"),
    ("blowfish", 128, "GROVER_WEAKENED"), ("twofish", 256, "QUANTUM_SAFE"),
    ("rc4", 128, "GROVER_WEAKENED"), ("chacha20", 256, "QUANTUM_SAFE"),
    ("salsa20", 256, "QUANTUM_SAFE"), ("idea", 128, "GROVER_WEAKENED"),
    ("sm4", 128, "GROVER_WEAKENED")
]
modes = ["_ecb", "_cbc", "_cfb", "_ofb", "_ctr", "_gcm", "_ccm", "_poly1305"]

asym_ciphers = [
    ("rsa", 2048, "SHOR_BROKEN"), ("rsa_1024", 1024, "SHOR_BROKEN"), ("rsa_3072", 3072, "SHOR_BROKEN"),
    ("rsa_4096", 4096, "SHOR_BROKEN"), ("elgamal", 2048, "SHOR_BROKEN"),
    ("sm2", 256, "SHOR_BROKEN"), ("kyber_512", 512, "QUANTUM_SAFE"),
    ("kyber_768", 768, "QUANTUM_SAFE"), ("kyber_1024", 1024, "QUANTUM_SAFE"),
    ("ml_kem_512", 512, "QUANTUM_SAFE"), ("ml_kem_768", 768, "QUANTUM_SAFE"),
    ("ml_kem_1024", 1024, "QUANTUM_SAFE"), ("ntru", 256, "QUANTUM_SAFE")
]

signatures = [
    ("rsa_sign", 2048, "SHOR_BROKEN"), ("ecdsa", 256, "SHOR_BROKEN"),
    ("ed25519", 256, "SHOR_BROKEN"), ("ed448", 448, "SHOR_BROKEN"),
    ("dsa", 2048, "SHOR_BROKEN"), ("dilithium_2", 256, "QUANTUM_SAFE"),
    ("dilithium_3", 384, "QUANTUM_SAFE"), ("dilithium_5", 512, "QUANTUM_SAFE"),
    ("ml_dsa_44", 256, "QUANTUM_SAFE"), ("ml_dsa_65", 384, "QUANTUM_SAFE"),
    ("ml_dsa_87", 512, "QUANTUM_SAFE"), ("falcon_512", 512, "QUANTUM_SAFE"),
    ("falcon_1024", 1024, "QUANTUM_SAFE"), ("sphincs", 256, "QUANTUM_SAFE"),
    ("slh_dsa", 256, "QUANTUM_SAFE")
]

kex = [
    ("dh", 2048, "SHOR_BROKEN"), ("ecdh", 256, "SHOR_BROKEN"),
    ("x25519", 256, "SHOR_BROKEN"), ("x448", 448, "SHOR_BROKEN"),
    ("kyber_kex", 768, "QUANTUM_SAFE")
]

macs = [
    ("hmac_md5", 128, "GROVER_WEAKENED"), ("hmac_sha1", 160, "GROVER_WEAKENED"),
    ("hmac_sha256", 256, "QUANTUM_SAFE"), ("hmac_sha512", 512, "QUANTUM_SAFE"),
    ("poly1305", 256, "QUANTUM_SAFE"), ("cmac_aes", 256, "QUANTUM_SAFE")
]

kdfs = [
    ("pbkdf2_hmac_sha256", 256, "QUANTUM_SAFE"), ("scrypt", 256, "QUANTUM_SAFE"),
    ("argon2", 256, "QUANTUM_SAFE"), ("hkdf_sha256", 256, "QUANTUM_SAFE"),
    ("bcrypt", 192, "QUANTUM_SAFE")
]

entries = []

for h, sz, v in hashes:
    entries.append(f'    "{h}": {{"primitive": CryptoPrimitiveType.HASH, "algo": "{h.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')
    
for c, sz, v in sym_ciphers:
    if "aes" in c or "camellia" in c or "aria" in c:
        for m in modes:
            name = c + m
            algo = name.upper().replace("_", "-")
            entries.append(f'    "{name}": {{"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "{algo}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')
    else:
        entries.append(f'    "{c}": {{"primitive": CryptoPrimitiveType.SYMMETRIC_ENCRYPTION, "algo": "{c.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')

for c, sz, v in asym_ciphers:
    entries.append(f'    "{c}": {{"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "{c.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')

for s, sz, v in signatures:
    entries.append(f'    "{s}": {{"primitive": CryptoPrimitiveType.SIGNATURE, "algo": "{s.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')

for k, sz, v in kex:
    entries.append(f'    "{k}": {{"primitive": CryptoPrimitiveType.KEY_EXCHANGE, "algo": "{k.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')

for m, sz, v in macs:
    entries.append(f'    "{m}": {{"primitive": CryptoPrimitiveType.MAC, "algo": "{m.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')

for k, sz, v in kdfs:
    entries.append(f'    "{k}": {{"primitive": CryptoPrimitiveType.KDF, "algo": "{k.upper()}", "key_size": {sz}, "vulnerability": QuantumVulnerability.{v}}}')

entries.append('    "rsa_oaep_encrypt": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA-OAEP", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN}')
entries.append('    "rsa_pkcs1v15_encrypt": {"primitive": CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION, "algo": "RSA-PKCS1v15", "key_size": 2048, "vulnerability": QuantumVulnerability.SHOR_BROKEN}')


with open("src/crypto_agility_navigator/discovery.py", "r") as f:
    content = f.read()

# Replace KNOWN_CRYPTO_PATTERNS
pattern = re.compile(r"KNOWN_CRYPTO_PATTERNS = \{.*?\n\}", re.DOTALL)
new_dict = "KNOWN_CRYPTO_PATTERNS = {\n" + ",\n".join(entries) + "\n}"
content = pattern.sub(new_dict, content)

with open("src/crypto_agility_navigator/discovery.py", "w") as f:
    f.write(content)

print(f"Generated {len(entries)} entries in KNOWN_CRYPTO_PATTERNS")
