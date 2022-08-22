"""
Invoke a suite of behaviour-driven tests for assignment 3.
"""
import sys
import logging
logger = logging.getLogger("director")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler(sys.stdout))

from director import test

test("a3_tests_1", "a3.py")
