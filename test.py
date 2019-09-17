import argparse, logging, os, sys, unittest
from .assetmgr import tests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Test Suite", description="Run specified tests.")
    parser.add_argument("-l", "--logging-level", type=str,
                        help="Desired logging level: debug, info, warning, error, critical")
    parser.add_argument("-f", "--logging-file", type=str,
                        help="Destination file for log.")
    parser.add_argument("specified_tests", nargs='*', action="store", default=None,
                        help="Destination file for log.")
    args = parser.parse_args(sys.argv[1:])
    sys.argv = sys.argv[:1]

    LOGGING_LEVELS = {"critical": logging.CRITICAL,
                    "error": logging.ERROR,
                    "warning": logging.WARNING,
                    "info": logging.INFO,
                    "debug": logging.DEBUG}

    logging_level = LOGGING_LEVELS.get(args.logging_level, logging.NOTSET)
    logging.basicConfig(level=logging_level, filename=args.logging_file,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.debug("Initializing tests with test.py...")
    logging.debug(f"Command line arguments: {args}")
    test_count = 0
    for test in tests.__all__:
        try:
            if args.specified_tests:
                if test in args.specified_tests:
                    unittest.main(f"tests.{test}")
            else:
                unittest.main(f"tests.{test}")
        except SystemExit:
            test_count += 1

    logging.debug(f"{test_count} test suites complete.\n\n")
