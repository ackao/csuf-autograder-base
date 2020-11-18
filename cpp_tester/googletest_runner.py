"""
    GoogleTestRunner class

    Runs C++ unit tests using googletest
"""

import os
import subprocess
import xml.etree.ElementTree as ET

from test_runner import TestRunner
from util import make_test_output

class GoogleTestRunner(TestRunner):
    """
    Runs C++ unit tests using googletest
    """
    test_cfg = {}
    test_dir = None

    def __init__(self, code_cfg, test_dir, code_dir):
        for obj in code_cfg:
            if 'googletest' in obj:
                for test in obj['googletest']:
                    implems = [os.path.join(code_dir, x) for x in obj['implems']]
                    self.test_cfg[test['test_file']] = {'implems' : implems,
                                                        'max_score': test.get('max_score', 1)}
        self.test_dir = test_dir
        super().__init__()

    def run_test(self):
        for (test, cfg) in self.test_cfg.items():
            test_path = os.path.join(self.test_dir, test)
            implems = cfg['implems']
            cmd = ['g++', '-std=c++17'] + implems
            cmd += [test_path, '-lgmock', '-lgtest', '-lpthread']

            fail = False
            try:
                subprocess.check_output(
                    cmd,
                    cwd=self.test_dir,
                    timeout=10,
                    stderr=subprocess.STDOUT)
            except subprocess.TimeoutExpired:
                msg = "Test case compilation timed out for {}".format(implems)
                fail = True
            except subprocess.CalledProcessError:
                msg = "Issue compiling test cases for {}:\n".format(implems)
                fail = True
            else:
                try:
                    run_cmd = ['./a.out', '--gtest_output=xml']
                    subprocess.check_output(run_cmd, cwd=self.test_dir)
                except subprocess.CalledProcessError:
                    msg = "Issue running some test cases for {}:\n".format(implems)
                    fail = True

            if fail:
                self.results.append(make_test_output(score=0,
                                                     max_score=cfg['max_score'],
                                                     output=msg,
                                                     visibility="visible"))
            else:
                self.parse_xml(os.path.join(self.test_dir, 'test_detail.xml'))

    def parse_xml(self, file):
        """
        Googletest needs to use RecordProperty(key, value) with these keys:

        'points': how many points per test case if there's multiple, defaults to 1 if not set
        'max_score': max score for problem, default: points
        'visibility': if not set, uses Gradescope default
        'all_or_nothing': if True, a single failure in a test case => no points
                                   otherwise => max_score, default: False
        """
        root = ET.parse(file).getroot()
        for test in root.iter('testcase'):
            name = "{}:{}".format(test.attrib['classname'], test.attrib['name'])
            points_per_case = int(test.attrib.get('points', 1))
            max_score = int(test.attrib.get('max_score', points_per_case))
            visibility = test.attrib.get('visibility', None)
            all_or_nothing = int(test.attrib.get('all_or_nothing', 0))
            output = ''

            num_fails = 0
            for fail in test.iter('failure'):
                num_fails += 1
                output += fail.attrib['message'] + '\n'

            if all_or_nothing and num_fails > 0:
                score = 0
            else:
                score = max(max_score - num_fails * points_per_case, 0)

            self.results.append(make_test_output(test_name=name,
                                                 score=score,
                                                 max_score=max_score,
                                                 output=output,
                                                 visibility=visibility))
