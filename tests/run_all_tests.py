# run_all_tests.py

import sys
import unittest

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("✅ All tests passed" if result.wasSuccessful() else "❌ Some tests failed")
    return 0 if result.wasSuccessful() else 1

sys.exit(run_tests())  # Always executed, no __main__ block