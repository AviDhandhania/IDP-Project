"""
Crypto-Agility Navigator - Data Models
Defines core data structures for cryptographic assets, dataflow paths, risk scoring, and CBOM metadata.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import datetime


class CryptoPrimitiveType(Enum):
    ASYMMETRIC_ENCRYPTION = "asymmetric_encryption"
    SIGNATURE = "signature"
    KEY_EXCHANGE = "key_exchange"
    SYMMETRIC_ENCRYPTION = "symmetric_encryption"
    HASH = "hash"
    MAC = "mac"
    KDF = "kdf"


class QuantumVulnerability(Enum):
    SHOR_BROKEN = 1.0       # Classical asymmetric (RSA, ECDSA, ECDH, DSA)
    GROVER_WEAKENED = 0.3    # Classical symmetric with key < 256 bits or hash < 384 bits
    QUANTUM_SAFE = 0.05      # Standardized PQC (ML-KEM, ML-DSA, SLH-DSA, AES-256)


class SourceClassification(Enum):
    PERSISTENT_STORAGE = "database_read"
    OFFSITE_ARCHIVE = "archive_read"
    USER_CREDENTIAL = "user_credential"
    NETWORK_INPUT = "network_request"
    EPHEMERAL_TOKEN = "local_rng_token"
    COMPUTED_DIGEST = "computed_digest"
    CONSTANT = "constant"
    UNKNOWN = "unknown"


class SinkClassification(Enum):
    CLOUD_OBJECT_STORE = "cloud_object_store"    # S3, GCS, Azure Blob
    PERSISTENT_DATABASE = "database_table"       # PostgreSQL, MySQL, etc.
    CACHE_TEMPORARY = "in_memory_cache"          # Redis, Memcached with TTL
    NETWORK_TRANSMIT = "network_response"        # Public API response
    LOCAL_LOG = "log_file"                       # File/syslog
    PROCESS_MEMORY = "process_memory"            # In-memory only
    UNKNOWN = "unknown"


class ExposureSurface(Enum):
    EXTERNAL_PUBLIC = 1.0       # Egress to public internet / multi-tenant cloud storage
    EXTERNAL_PARTNER = 0.75     # Cross-organization egress / private interconnect
    INTERNAL_CROSS_HOST = 0.5   # Across internal host boundary (internal VPC/RPC)
    INTERNAL_IPC = 0.25         # Across process boundary on same host
    IN_PROCESS = 0.1            # Never leaves memory / process


@dataclass
class CryptoInvocation:
    """Represents a discovered cryptographic call site in source code."""
    file_path: str
    line_number: int
    function_name: str
    primitive_type: CryptoPrimitiveType
    algorithm_name: str
    key_size: Optional[int] = None
    quantum_vulnerability: QuantumVulnerability = QuantumVulnerability.SHOR_BROKEN
    raw_code_snippet: str = ""
    parameters: Dict[str, str] = field(default_factory=dict)


@dataclass
class RetentionEvidence:
    """Retention duration and source of evidence for protected data."""
    retention_years: float
    evidence_type: str          # "orm_field", "s3_lifecycle_policy", "redis_ttl", "default_prior"
    observed: bool = True       # True if statically extracted; False if inferred from sink class
    description: str = ""


@dataclass
class DataPath:
    """Complete semantic path bound to a cryptographic operation."""
    invocation: CryptoInvocation
    plaintext_source: SourceClassification
    ciphertext_sink: SinkClassification
    retention: RetentionEvidence
    exposure: ExposureSurface
    key_reuse_count: int = 1
    is_security_relevant: bool = True
    suppression_reason: Optional[str] = None


@dataclass
class HNDLScore:
    """HNDL Exposure Score operationalizing Mosca's inequality."""
    raw_score: float
    normalized_score: float
    retention_factor: float
    exposure_factor: float
    algorithm_factor: float
    key_reuse_factor: float
    urgency_tier: str           # "IMMEDIATE", "HIGH", "MEDIUM", "LOW", "SUPPRESSED"
    mosca_violated: bool        # x + y > z
    remediation_recommendation: str
