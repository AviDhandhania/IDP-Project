import unittest
import ast
from pathlib import Path
from src.crypto_agility_navigator.discovery import CryptoASTVisitor, DiscoveryEngine
from src.crypto_agility_navigator.models import CryptoPrimitiveType, QuantumVulnerability

class TestAdvancedDataFlowAnalysis(unittest.TestCase):

    def test_python_import_aliasing(self):
        code = """
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
key = generate_private_key(public_exponent=65537, key_size=2048)
"""
        visitor = CryptoASTVisitor("test.py", code)
        visitor.visit(ast.parse(code))
        
        self.assertEqual(len(visitor.invocations), 1)
        self.assertEqual(visitor.invocations[0].primitive_type, CryptoPrimitiveType.ASYMMETRIC_ENCRYPTION)
        self.assertEqual(visitor.invocations[0].algorithm_name, "RSA")

    def test_java_constant_propagation(self):
        engine = DiscoveryEngine()
        if not engine.java_parser:
            self.skipTest("tree-sitter-java not installed")
            
        code = """
class Test {
    private static final String ALGO = "AES/GCM/NoPadding";
    public void doCrypto() {
        Cipher c = Cipher.getInstance(ALGO);
    }
}
"""
        tree = engine.java_parser.parse(bytes(code, "utf-8"))
        invocations = engine._parse_java_tree(tree, "Test.java", code)
        
        self.assertEqual(len(invocations), 1)
        self.assertEqual(invocations[0].algorithm_name, "AES/GCM/NOPADDING")
        self.assertEqual(invocations[0].quantum_vulnerability, QuantumVulnerability.QUANTUM_SAFE)

if __name__ == '__main__':
    unittest.main()
