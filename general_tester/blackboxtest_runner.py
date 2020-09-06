"""
BlackBoxTestRunner class

Runs blackbox tests for C++ code.
Specify input for stdin + expected output + expected exit code
Runs the specified executable and compares results
"""
import os
import subprocess

from test_runner import TestRunner
from util import make_test_output, encode_as_bytes

class BlackBoxTestRunner(TestRunner):
    """
    Runs blackbox tests for C++ code.
    Specify input for stdin + expected output + expected exit code
    Runs the specified executable and compares results
    """
    tests = None
    build_dir = None

    def __init__(self, tests, build_dir):
        self.tests = tests
        self.build_dir = build_dir
        super().__init__()

    def run_test(self):
        for test in self.tests:
            self.run_test_case(test)

    def run_test_case(self, test):
        """
        Run an individual test case
        """
        test_name = test.get('test_name', "")
        max_score = test.get('points', 1)
        visibility = test.get('visibility', 'visible')

        if test['obj'] in self.get_skip():
            # code didn't compile correctly, skip test and give 0 points
            (result, msg) = (False, "Skipped test due to non-compiling code")
        else:
            filepath = os.path.join(self.build_dir, test['obj'])
            proc = subprocess.Popen(
                filepath,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.build_dir)
            stdin = encode_as_bytes(test.get('stdin', ""))

            output, _ = proc.communicate(stdin, test.get('timeout', 10))

            if 'output' in test['test_types']:
                expected_output = str.encode(test.get('stdout', ""))
                (result, msg) = self.assert_equal(stdin, expected_output, output)
            if 'exitcode' in test['test_types']:
                expected_returncode = test.get('exitcode', 0)
                (result, msg) = self.assert_equal(
                    stdin,
                    expected_returncode,
                    proc.returncode,
                    fmt="Input:\n{}\nExpected exit code:\n{}\nYour program's exit code:\n{}")

        if result:
            score = max_score
        else:
            score = 0

        self.results.append(make_test_output(
            test_name=test_name,
            score=score,
            max_score=max_score,
            output=msg,
            visibility=visibility))
