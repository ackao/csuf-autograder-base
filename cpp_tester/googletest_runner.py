"""
    GoogleTestRunner class

    Runs C++ unit tests using googletest
"""

import os
import subprocess

from test_runner import TestRunner
from util import format_to_string

class GoogleTestRunner(TestRunner):
    """
    Runs C++ unit tests using googletest
    """
    test_cfg = {}
    test_dir = None

    def __init__(self, code_cfg, test_dir):
        for obj in code_cfg:
            if 'googletest' in obj:
                for test in obj['googletest']:
                    self.test_cfg[test] = obj['implems']
        self.test_dir = test_dir
        super().__init__()

    def run_test(self):
        for test, implems in self.test_cfg.items():
            test_path = os.path.join(self.test_dir, test)
            obj = os.path.splitext(test_path)[0]
            cmd = ['g++', '-std=c++17'] + implems
            cmd += [test_path, '-o', obj, '-lgtest_main', '-lgtest', '-lpthread']
            print(cmd)

            try:
                subprocess.check_output(
                    cmd,
                    cwd=self.test_dir,
                    timeout=10,
                    stderr=subprocess.STDOUT)
            except subprocess.TimeoutExpired:
                msg = "Test case compilation timed out for {}".format(implems)
                score = 0
            except subprocess.CalledProcessError as e:
                msg = "Issue compiling test cases for {}:\n{}".format(implems,
                                                                      format_to_string(e.output))
                score = 0
            else:
                try:
                    run_cmd = [obj, '--gtest-output', 'json:{}'.format(obj+'.json')]
                    subprocess.run(run_cmd, cwd=self.test_dir)
                except:
                    msg = "Issue running test cases for {}:\n".format(implems)
                    score = 0
                else:
                    print('todo')
