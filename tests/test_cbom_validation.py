import unittest
import json
import urllib.request
import os

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

from src.crypto_agility_navigator.models import DataPath, HNDLScore, CryptoInvocation, CryptoPrimitiveType, QuantumVulnerability, SourceClassification, SinkClassification, ExposureSurface, RetentionEvidence
from src.crypto_agility_navigator.cbom import CBOMGenerator


class TestCBOMValidation(unittest.TestCase):
    SCHEMA_URL = "https://raw.githubusercontent.com/CycloneDX/specification/master/schema/bom-1.6.schema.json"
    SCHEMA_FILE = "tests/bom-1.6.schema.json"

    @classmethod
    def setUpClass(cls):
        if HAS_JSONSCHEMA:
            if not os.path.exists(cls.SCHEMA_FILE):
                try:
                    urllib.request.urlretrieve(cls.SCHEMA_URL, cls.SCHEMA_FILE)
                except Exception as e:
                    print(f"Warning: could not download CycloneDX schema: {e}")

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema module not installed")
    def test_cbom_schema_validation(self):
        if not os.path.exists(self.SCHEMA_FILE):
            self.skipTest("Schema file not downloaded")

        with open(self.SCHEMA_FILE, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        invocation = CryptoInvocation(
            file_path="dummy.py",
            line_number=10,
            function_name="encrypt",
            primitive_type=CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION,
            algorithm_name="RSA-2048",
            key_size=2048,
            quantum_vulnerability=QuantumVulnerability.SHOR_BROKEN,
            raw_code_snippet="encrypt(data)"
        )
        path = DataPath(
            invocation=invocation,
            plaintext_source=SourceClassification.NETWORK_INPUT,
            ciphertext_sink=SinkClassification.CLOUD_OBJECT_STORE,
            retention=RetentionEvidence(10.0, "s3_lifecycle_policy", True, "Retain 10 years"),
            exposure=ExposureSurface.EXTERNAL_PUBLIC
        )
        score = HNDLScore(33.3, 33.3, 1.0, 1.0, 1.0, 1.0, "CRITICAL", True, "Migrate")

        generator = CBOMGenerator()
        cbom_doc = generator.generate_cbom([(path, score)])

        try:
            jsonschema.validate(instance=cbom_doc, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            self.fail(f"CBOM output did not validate against CycloneDX 1.6 schema: {e}")
