"""
Unit tests for Crypto-Agility Copilot prototype (Review II).
"""

import unittest
from pathlib import Path
from src.crypto_agility_copilot.discovery import DiscoveryEngine
from src.crypto_agility_copilot.dataflow import DataflowBindingEngine
from src.crypto_agility_copilot.scorer import HNDLScoringEngine
from src.crypto_agility_copilot.cbom import CBOMGenerator
from src.crypto_agility_copilot.models import (
    CryptoPrimitiveType,
    QuantumVulnerability,
    SourceClassification,
    SinkClassification,
    ExposureSurface
)


class TestCryptoAgilityCopilot(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
