"""
Crypto-Agility Navigator - CycloneDX 1.6 CBOM Generator
Generates standards-compliant CycloneDX 1.6 Cryptography Bill of Materials (CBOM) JSON
with custom dataflow and HNDL prioritization extensions.
"""

import json
import uuid
import datetime
from typing import List, Tuple, Dict, Any
from .models import DataPath, HNDLScore


class CBOMGenerator:
    """Emits CycloneDX 1.6 Cryptography Bill of Materials (CBOM) specifications."""

    def __init__(self, serial_number: str = None):
        self.serial_number = serial_number or f"urn:uuid:{uuid.uuid4()}"

    def generate_cbom(
        self,
        ranked_items: List[Tuple[DataPath, HNDLScore]],
        target_component_name: str = "Application-Codebase",
        target_version: str = "1.0.0"
    ) -> Dict[str, Any]:
        """Builds CycloneDX 1.6 CBOM document dictionary."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        components: List[Dict[str, Any]] = []

        for idx, (path, score) in enumerate(ranked_items):
            inv = path.invocation
            comp_bom_ref = f"crypto-asset-{idx + 1}"

            crypto_properties: Dict[str, Any] = {
                "assetType": "algorithm",
                "algorithmProperties": {
                    "primitive": inv.primitive_type.value,
                    "parameterSetIdentifier": inv.algorithm_name,
                    "curve": "N/A",
                    "executionEnvironment": "software-plain-text",
                    "implementationPlatform": "c-python",
                    "certificationLevel": ["none"],
                    "mode": "oaep" if "OAEP" in inv.algorithm_name else "default",
                    "padding": "oaep" if "OAEP" in inv.algorithm_name else "pkcs1v15",
                    "cryptoFunctions": [inv.primitive_type.value],
                    "classicalSecurityLevel": inv.key_size or 128,
                    "nistQuantumSecurityLevel": 0 if inv.quantum_vulnerability.value == 1.0 else 5
                },
                "detectionContext": {
                    "filePath": inv.file_path,
                    "lineNumber": inv.line_number,
                    "rawSnippet": inv.raw_code_snippet
                }
            }

            # Custom Dataflow and HNDL Extensions
            dataflow_extension: Dict[str, Any] = {
                "plaintextSource": path.plaintext_source.value,
                "ciphertextSink": path.ciphertext_sink.value,
                "retentionEvidence": {
                    "retentionYears": path.retention.retention_years,
                    "evidenceType": path.retention.evidence_type,
                    "observed": path.retention.observed,
                    "description": path.retention.description
                },
                "exposureSurface": path.exposure.name,
                "hndlRiskAssessment": {
                    "normalizedScore": score.normalized_score,
                    "urgencyTier": score.urgency_tier,
                    "moscaViolated": score.mosca_violated,
                    "recommendation": score.remediation_recommendation
                },
                "securityRelevance": {
                    "isSecurityRelevant": path.is_security_relevant,
                    "suppressionReason": path.suppression_reason
                }
            }

            component_obj: Dict[str, Any] = {
                "bom-ref": comp_bom_ref,
                "type": "cryptographic-asset",
                "name": inv.algorithm_name,
                "version": f"keysize-{inv.key_size}" if inv.key_size else "standard",
                "description": f"{inv.algorithm_name} invocation at {inv.file_path}:{inv.line_number}",
                "cryptoProperties": crypto_properties,
                "dataflowProperties": dataflow_extension
            }

            components.append(component_obj)

        cbom_doc: Dict[str, Any] = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "serialNumber": self.serial_number,
            "version": 1,
            "metadata": {
                "timestamp": timestamp,
                "tools": [
                    {
                        "vendor": "Crypto-Agility Navigator",
                        "name": "crypto-agility-navigator-engine",
                        "version": "0.2.0-review2"
                    }
                ],
                "component": {
                    "bom-ref": "root-application",
                    "type": "application",
                    "name": target_component_name,
                    "version": target_version
                }
            },
            "components": components
        }

        return cbom_doc

    def export_json(self, cbom_doc: Dict[str, Any], output_path: str) -> None:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cbom_doc, f, indent=2)
