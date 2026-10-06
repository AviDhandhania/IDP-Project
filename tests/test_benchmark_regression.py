import unittest
from pathlib import Path
from src.crypto_agility_navigator.discovery import DiscoveryEngine
from src.crypto_agility_navigator.dataflow import DataflowBindingEngine
from src.crypto_agility_navigator.scorer import HNDLScoringEngine

class TestBenchmarkRegression(unittest.TestCase):
    def test_benchmark_regression(self):
        project_dir = Path("examples/sample_project")
        if not project_dir.exists():
            self.skipTest("Benchmark project not found")
            
        discovery_engine = DiscoveryEngine()
        dataflow_engine = DataflowBindingEngine()
        scorer = HNDLScoringEngine()
        
        # Stage 1: Discovery
        invocations = discovery_engine.scan_directory(str(project_dir))
        self.assertEqual(len(invocations), 3, "Expected 3 cryptographic invocations in the benchmark")
        
        # Stage 2: Dataflow
        paths = [dataflow_engine.bind_invocation(inv) for inv in invocations]
        self.assertEqual(len(paths), 3)
        
        # Stage 3: Scoring
        scored_paths = [(p, scorer.score_data_path(p)) for p in paths]
        
        # Assertions based on expected benchmark results
        actionable = [p for p in scored_paths if p[0].is_security_relevant]
        suppressed = [p for p in scored_paths if not p[0].is_security_relevant]
        
        self.assertEqual(len(actionable), 2, "Expected 2 actionable candidates")
        self.assertEqual(len(suppressed), 1, "Expected 1 context-suppressed finding (noise filtered)")
        
        breaches = [p for p in scored_paths if p[1].mosca_violated]
        self.assertEqual(len(breaches), 1, "Expected 1 Mosca's Inequality Breach")
        
        # Check archive.py specific results
        archive_res = next((p for p in scored_paths if "archive.py" in p[0].invocation.file_path), None)
        self.assertIsNotNone(archive_res)
        self.assertGreater(archive_res[1].normalized_score, 30.0)
        self.assertTrue(archive_res[1].mosca_violated)
        
        # Check session.py specific results
        session_res = next((p for p in scored_paths if "session.py" in p[0].invocation.file_path), None)
        self.assertIsNotNone(session_res)
        self.assertEqual(session_res[1].normalized_score, 0.0)
        self.assertFalse(session_res[1].mosca_violated)
        
        # Check etags.py specific results
        etags_res = next((p for p in scored_paths if "etags.py" in p[0].invocation.file_path), None)
        self.assertIsNotNone(etags_res)
        self.assertFalse(etags_res[0].is_security_relevant)
