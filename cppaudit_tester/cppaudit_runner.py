"""
    CPPAuditTestRunner class

    Runs CPPAudit tests
"""

import os
import subprocess
import xml.etree.ElementTree as ET

from test_runner import TestRunner
from util import make_test_output

class GoogleTestRunner(TestRunner):
    """
    Runs CPPAudit tests
    """
    test_cfg = {}
    results = {}
    test_dir = None

    code_cfg = None

    def __init__(self, code_cfg):
        self.code_cfg = code_cfg
        super().__init__()

    def run_test(self):
        for obj in self.code_cfg:
            implementation_score = obj['implementation_score']
            compilation_score = obj['compilation_score']
            functionality_score = obj['functionality_score']
            readability_score = obj['readability_score']

            self.check_implementation(implementation_score)
            self.check_compilation(compilation_score)
            self.check_functionality(functionality_score)
            self.check_readability(readability_score)
                                

    def check_implementation(self, max_score):
        # TODO: Find a way to distinguish whether a student submitted something or not 
        pass

    def check_compilation(self, max_score):
        success = False
        score = None
        cmd = ["make build"]
        try:
          subprocess.check_output(cmd, 
                                  cwd=self.code_dir, 
                                  timeout=10,
                                  stderr=subprocess.STDOUT,
                                  check=True)
        except subprocess.TimeoutExpired:
          msg = "Compilation failed (timeout)"
        except subprocess.CalledProcessError as err:
          msg = "Compilation failed\n" + err.output 
        else:
          msg = "Compilation succeeded"
          success = True

        if success:
            score = max_score
        else:
            score = 0
        self.results.append(make_test_output(
            test_name="Compilation Test: {}".format(obj['problem']),
            score=score,
            max_score=max_score,
            output=msg,
            visibility="visible"))
        

    def check_functionality(self):
        # TODO: modify to fit the cpp audit unit test
        '''
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
        '''
        
    def check_readability(self):
        # TODO: retrieve data from stylecheck and formatcheck
        pass

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
