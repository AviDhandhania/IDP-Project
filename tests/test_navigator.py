"""
Unit tests for Crypto-Agility Navigator prototype (Review II).
"""

import unittest
from pathlib import Path
from src.crypto_agility_navigator.discovery import DiscoveryEngine
from src.crypto_agility_navigator.dataflow import DataflowBindingEngine
from src.crypto_agility_navigator.scorer import HNDLScoringEngine
from src.crypto_agility_navigator.cbom import CBOMGenerator
from src.crypto_agility_navigator.models import (
    CryptoPrimitiveType,
    QuantumVulnerability,
    SourceClassification,
    SinkClassification,
    ExposureSurface
)


class TestCryptoAgilityNavigator(unittest.TestCase):

    def setUp(self):
        self.discovery = DiscoveryEngine()
        self.dataflow = DataflowBindingEngine()
        self.scorer = HNDLScoringEngine()
        self.cbom = CBOMGenerator()

        self.archive_file = "examples/sample_project/payments/archive.py"
        self.session_file = "examples/sample_project/web/session.py"
        self.etag_file = "examples/sample_project/cache/etags.py"

    def test_discovery_engine(self):
        invocations = self.discovery.scan_file(self.archive_file)
        self.assertEqual(len(invocations), 1)
        inv = invocations[0]
        self.assertEqual(inv.algorithm_name, "RSA-OAEP")
        self.assertEqual(inv.key_size, 2048)
        self.assertEqual(inv.quantum_vulnerability, QuantumVulnerability.SHOR_BROKEN)

    def test_semantic_binding_discrimination(self):
        # Scan both files
        inv_archive = self.discovery.scan_file(self.archive_file)[0]
        inv_session = self.discovery.scan_file(self.session_file)[0]

        path_archive = self.dataflow.bind_invocation(inv_archive)
        path_session = self.dataflow.bind_invocation(inv_session)

        # Plaintext source differences
        self.assertEqual(path_archive.plaintext_source, SourceClassification.PERSISTENT_STORAGE)
        self.assertEqual(path_session.plaintext_source, SourceClassification.EPHEMERAL_TOKEN)

        # Ciphertext sink & exposure differences
        self.assertEqual(path_archive.ciphertext_sink, SinkClassification.CLOUD_OBJECT_STORE)
        self.assertEqual(path_archive.exposure, ExposureSurface.EXTERNAL_PUBLIC)

        self.assertEqual(path_session.ciphertext_sink, SinkClassification.CACHE_TEMPORARY)

        # Retention duration differences
        self.assertEqual(path_archive.retention.retention_years, 10.0)
        self.assertTrue(path_session.retention.retention_years < 0.01)

    def test_scoring_and_mosca_inequality(self):
        inv_archive = self.discovery.scan_file(self.archive_file)[0]
        inv_session = self.discovery.scan_file(self.session_file)[0]

        path_archive = self.dataflow.bind_invocation(inv_archive)
        path_session = self.dataflow.bind_invocation(inv_session)

        score_archive = self.scorer.score_data_path(path_archive)
        score_session = self.scorer.score_data_path(path_session)

        # Archive path violates Mosca's inequality (10y retention + 2y migration > 7y CRQC horizon)
        self.assertTrue(score_archive.mosca_violated)
        self.assertFalse(score_session.mosca_violated)

        # Archive path score must significantly exceed ephemeral session score
        self.assertGreater(score_archive.normalized_score, score_session.normalized_score)
        self.assertGreater(score_archive.normalized_score, 15.0)

    def test_context_noise_suppression(self):
        inv_etag = self.discovery.scan_file(self.etag_file)[0]
        path_etag = self.dataflow.bind_invocation(inv_etag)
        score_etag = self.scorer.score_data_path(path_etag)

        self.assertEqual(score_etag.urgency_tier, "SUPPRESSED")
        self.assertEqual(score_etag.normalized_score, 0.0)

    def test_cbom_generation(self):
        inv_archive = self.discovery.scan_file(self.archive_file)[0]
        path_archive = self.dataflow.bind_invocation(inv_archive)
        score_archive = self.scorer.score_data_path(path_archive)

        cbom_doc = self.cbom.generate_cbom([(path_archive, score_archive)])
        self.assertEqual(cbom_doc["bomFormat"], "CycloneDX")
        self.assertEqual(cbom_doc["specVersion"], "1.6")
        self.assertEqual(len(cbom_doc["components"]), 1)
        comp = cbom_doc["components"][0]
        self.assertEqual(comp["name"], "RSA-OAEP")
        self.assertIn("dataflowProperties", comp)
        self.assertEqual(comp["dataflowProperties"]["retentionEvidence"]["retentionYears"], 10.0)

    def test_full_pipeline_ranking(self):
        from src.crypto_agility_navigator.server import scan_target
        results = scan_target("examples/sample_project")
        self.assertEqual(results["status"], "success")
        self.assertEqual(results["metrics"]["totalFindings"], 3)
        self.assertEqual(results["metrics"]["actionableCount"], 2)
        self.assertEqual(results["metrics"]["suppressedCount"], 1)
        self.assertEqual(results["metrics"]["moscaBreaches"], 1)
        self.assertEqual(results["metrics"]["shorBrokenCount"], 2)

        # Rank #1 must be the S3 archive (Mosca breach)
        rank1 = results["findings"][0]
        self.assertEqual(rank1["fileName"], "archive.py")
        self.assertTrue(rank1["moscaViolated"])
        self.assertEqual(rank1["urgencyTier"], "CRITICAL_IMMEDIATE")

    def test_custom_code_snippet_analysis(self):
        from src.crypto_agility_navigator.server import analyze_custom_code
        snippet = '''
import boto3
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def store_secret(data, rsa_key):
    s3 = boto3.client('s3')
    enc = rsa_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    s3.put_object(Bucket='compliance-vault-10yr', Key='audit.enc', Body=enc)
'''
        result = analyze_custom_code(snippet)
        self.assertGreaterEqual(len(result["findings"]), 1)
        # Top-ranked finding must be the RSA encryption
        f = result["findings"][0]
        self.assertEqual(f["algorithm"], "RSA-OAEP")
        self.assertEqual(f["retentionYears"], 10.0)
        self.assertTrue(f["moscaViolated"])
        self.assertEqual(f["urgencyTier"], "CRITICAL_IMMEDIATE")


    def test_quantum_safe_scoring(self):
        # A standardized PQC primitive (ML-KEM) should score very low and not be flagged as Shor-broken
        inv_archive = self.discovery.scan_file(self.archive_file)[0]
        path_archive = self.dataflow.bind_invocation(inv_archive)
        
        # Override to Quantum-Safe
        path_archive.invocation.quantum_vulnerability = QuantumVulnerability.QUANTUM_SAFE
        score = self.scorer.score_data_path(path_archive)
        self.assertLess(score.normalized_score, 5.0)


if __name__ == "__main__":
    unittest.main()

