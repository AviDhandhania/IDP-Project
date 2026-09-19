"""
Crypto-Agility Navigator - HTTP API & Dashboard Server
Provides REST API endpoints for discovery, dataflow analysis, Mosca simulation, and CBOM export,
along with serving the interactive web dashboard.
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler
from typing import List, Tuple, Dict, Any
from urllib.parse import urlparse, parse_qs

from .discovery import DiscoveryEngine
from .dataflow import DataflowBindingEngine
from .scorer import HNDLScoringEngine
from .cbom import CBOMGenerator
from .models import DataPath, HNDLScore, CryptoPrimitiveType, QuantumVulnerability, SourceClassification, SinkClassification, ExposureSurface


WEB_DIR = Path(__file__).parent / "web"


def scan_target(target_path: str) -> Dict[str, Any]:
    """Runs the 4-stage pipeline and returns JSON-serializable results."""
    discovery_engine = DiscoveryEngine()
    binding_engine = DataflowBindingEngine()
    scoring_engine = HNDLScoringEngine()
    cbom_generator = CBOMGenerator()

    target = Path(target_path)
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {target_path}")

    if target.is_file():
        invocations = discovery_engine.scan_file(str(target))
    else:
        invocations = discovery_engine.scan_directory(str(target))

    data_paths: List[DataPath] = []
    for inv in invocations:
        dp = binding_engine.bind_invocation(inv)
        data_paths.append(dp)

    ranked = scoring_engine.rank_paths(data_paths)
    cbom_doc = cbom_generator.generate_cbom(ranked, target_component_name=target.name)

    findings = []
    for rank_idx, (path, score) in enumerate(ranked, start=1):
        inv = path.invocation
        findings.append({
            "rank": rank_idx,
            "algorithm": inv.algorithm_name,
            "primitiveType": inv.primitive_type.value,
            "keySize": inv.key_size,
            "quantumVulnerability": inv.quantum_vulnerability.name,
            "filePath": inv.file_path,
            "fileName": Path(inv.file_path).name,
            "lineNumber": inv.line_number,
            "rawCodeSnippet": inv.raw_code_snippet,
            "plaintextSource": path.plaintext_source.value,
            "ciphertextSink": path.ciphertext_sink.value,
            "retentionYears": path.retention.retention_years,
            "retentionEvidenceType": path.retention.evidence_type,
            "retentionObserved": path.retention.observed,
            "retentionDescription": path.retention.description,
            "exposureSurface": path.exposure.name,
            "exposureFactor": score.exposure_factor,
            "hndlScore": score.normalized_score,
            "rawScore": score.raw_score,
            "urgencyTier": score.urgency_tier,
            "moscaViolated": score.mosca_violated,
            "recommendation": score.remediation_recommendation,
            "isSecurityRelevant": path.is_security_relevant,
            "suppressionReason": path.suppression_reason
        })

    total_findings = len(findings)
    suppressed_count = sum(1 for f in findings if f["urgencyTier"] == "SUPPRESSED")
    actionable_count = total_findings - suppressed_count
    mosca_breaches = sum(1 for f in findings if f["moscaViolated"])
    shor_broken_count = sum(1 for f in findings if f["quantumVulnerability"] == "SHOR_BROKEN")
    avg_score = round(sum(f["hndlScore"] for f in findings if f["isSecurityRelevant"]) / max(1, actionable_count), 2)

    return {
        "status": "success",
        "targetPath": str(target),
        "targetName": target.name,
        "metrics": {
            "totalFindings": total_findings,
            "actionableCount": actionable_count,
            "suppressedCount": suppressed_count,
            "noiseFilteredPercent": round(suppressed_count / max(1, total_findings) * 100, 1),
            "moscaBreaches": mosca_breaches,
            "shorBrokenCount": shor_broken_count,
            "averageActionableScore": avg_score
        },
        "findings": findings,
        "cbom": cbom_doc
    }


def analyze_custom_code(code_snippet: str, filename: str = "custom_module.py") -> Dict[str, Any]:
    """Analyzes a raw Python code snippet directly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / filename
        temp_file.write_text(code_snippet, encoding="utf-8")
        result = scan_target(str(temp_file))
        result["targetName"] = filename
        result["targetPath"] = filename
        for f in result["findings"]:
            f["filePath"] = filename
        return result


class CopilotApiHandler(SimpleHTTPRequestHandler):
    """Handles API routes and serves dashboard web UI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def _send_json(self, data: Any, status_code: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "service": "Crypto-Agility Navigator",
                "version": "0.2.0-review2",
                "trl": "TRL 3 - Proof of Concept"
            })
            return

        if path == "/api/scan":
            query = parse_qs(parsed.query)
            target = query.get("target", ["examples/sample_project"])[0]
            try:
                results = scan_target(target)
                self._send_json(results)
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status_code=500)
            return

        if path == "/api/cbom":
            query = parse_qs(parsed.query)
            target = query.get("target", ["examples/sample_project"])[0]
            try:
                results = scan_target(target)
                self._send_json(results["cbom"])
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status_code=500)
            return

        # Fallback to static files
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            payload = json.loads(post_body)
        except json.JSONDecodeError:
            payload = {}

        if path == "/api/scan-code":
            code = payload.get("code", "")
            filename = payload.get("filename", "snippet.py")
            if not code.strip():
                self._send_json({"status": "error", "message": "Code snippet cannot be empty."}, status_code=400)
                return
            try:
                results = analyze_custom_code(code, filename)
                self._send_json(results)
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status_code=500)
            return

        if path == "/api/simulate-mosca":
            retention_years = float(payload.get("retentionYears", 10.0))
            migration_years = float(payload.get("migrationYears", 2.0))
            crqc_horizon_years = float(payload.get("crqcHorizonYears", 7.0))
            exposure_surface = payload.get("exposureSurface", "EXTERNAL_PUBLIC")
            vulnerability = payload.get("quantumVulnerability", "SHOR_BROKEN")
            key_reuse = int(payload.get("keyReuseCount", 1))

            engine = HNDLScoringEngine(
                migration_years=migration_years,
                crqc_horizon_years=crqc_horizon_years
            )

            # Build mock DataPath
            from .models import CryptoInvocation, RetentionEvidence
            inv = CryptoInvocation(
                file_path="simulated_target.py",
                line_number=42,
                function_name="encrypt_payload",
                primitive_type=CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
                algorithm_name="RSA-2048",
                key_size=2048,
                quantum_vulnerability=QuantumVulnerability[vulnerability]
            )
            dp = DataPath(
                invocation=inv,
                plaintext_source=SourceClassification.PERSISTENT_STORAGE,
                ciphertext_sink=SinkClassification.CLOUD_OBJECT_STORE,
                retention=RetentionEvidence(retention_years=retention_years, evidence_type="simulation", observed=True),
                exposure=ExposureSurface[exposure_surface],
                key_reuse_count=key_reuse
            )

            score = engine.score_data_path(dp)

            self._send_json({
                "status": "success",
                "parameters": {
                    "retentionYears_x": retention_years,
                    "migrationYears_y": migration_years,
                    "crqcHorizonYears_z": crqc_horizon_years,
                    "moscaEquation": f"x ({retention_years}y) + y ({migration_years}y) vs z ({crqc_horizon_years}y)",
                    "sum_x_plus_y": round(retention_years + migration_years, 2)
                },
                "score": {
                    "normalizedScore": score.normalized_score,
                    "rawScore": score.raw_score,
                    "urgencyTier": score.urgency_tier,
                    "moscaViolated": score.mosca_violated,
                    "recommendation": score.remediation_recommendation,
                    "factors": {
                        "retention": score.retention_factor,
                        "exposure": score.exposure_factor,
                        "algorithm": score.algorithm_factor,
                        "keyReuse": score.key_reuse_factor
                    }
                }
            })
            return

        self._send_json({"status": "error", "message": "Endpoint not found"}, status_code=404)


def run_server(port: int = 8000, host: str = "127.0.0.1"):
    """Starts the HTTP server on specified host and port."""
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, CopilotApiHandler)
    print(f"[*] Crypto-Agility Navigator Dashboard & API running at http://{host}:{port}/")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()



if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
