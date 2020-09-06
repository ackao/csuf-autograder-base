from classes.test_runner import TestRunner
from util import make_test_output, encode_as_bytes
import os
import subprocess
import unittest

class BlackBoxTestRunner(TestRunner):
    tests = None
    build_dir = None
    failed = None

    def __init__(self, tests, build_dir):
        self.tests = tests
        self.build_dir = build_dir
        self.failed = []
        super().__init__()

    def run_test(self, failed=[]):
        self.failed = failed
        for test in self.tests:
            self.run_test_case(test)

    def run_test_case(self, test):
        test_name = test.get('test_name', "")
        max_score = test.get('points', 1)
        visibility = test.get('visibility', 'visible')

        if test['obj'] in self.failed:
            # code didn't compile correctly, skip test and give 0 points
            (result, msg) = (False, "Skipped test due to non-compiling code")
        else:
            filepath = os.path.join(self.build_dir, test['obj'])
            proc = subprocess.Popen(filepath, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.build_dir)
            stdin = encode_as_bytes(test.get('stdin', ""))

            output, err = proc.communicate(stdin, test.get('timeout', 1))

            if 'output' in test['test_types']:
                expected_output = str.encode(test.get('stdout', ""))
                (result, msg) = self.assertEqual(stdin, expected_output, output)
            if 'exitcode' in test['test_types']:
                expected_returncode = test.get('exitcode', 0)
                (result, msg) = self.assertEqual(stdin, expected_returncode, proc.returncode, fmt="Input:\n{}\nExpected exit code:\n{}\nYour program's exit code:\n{}")

        if result:
            score = max_score
        else:
            score = 0

        self.results.append(make_test_output(test_name=test_name, score=score, max_score=max_score, output=msg, visibility=visibility))
