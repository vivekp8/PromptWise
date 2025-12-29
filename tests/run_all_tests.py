import sys
import unittest


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate status code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
