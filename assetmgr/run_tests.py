import os, unittest
import tests

for test in tests.__all__:
    unittest.main(f"tests.{test}")