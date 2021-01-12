"""
    CPPAuditRunner class

    Runs CPPAudit tests
"""

import os
import subprocess
import shutil
import difflib
import xml.etree.ElementTree as ET

from test_runner import TestRunner
from util import make_test_output, recursive_copy_with_overwrite

class CPPAuditRunner(TestRunner):
    """
    Runs CPPAudit tests
    """
    results = {}
    code_cfg = None
    code_dir = None

    def __init__(self, code_cfg, code_dir):
        self.code_cfg = code_cfg
        self.code_dir = code_dir
        
        super().__init__()

    def run_test(self):
        for obj in self.code_cfg:
            if 'cppaudit' in obj:      
                implementation_score = obj['cppaudit']['implementation_score']
                compilation_score = obj['cppaudit']['compilation_score']
                functionality_score = obj['cppaudit']['functionality_score']
                readability_score = obj['cppaudit']['readability_score']

                self.overwrite_test_files(obj['cppaudit']['starter_code'], obj['cppaudit']['base_directory'])
                implem_result = self.check_implementation(obj['cppaudit']['starter_code'], obj['cppaudit']['base_directory'], obj['cppaudit'])
                if (implem_result > 0):
                  self.check_compilation(obj['cppaudit']['base_directory'], compilation_score)
                  self.check_functionality(obj['cppaudit']['base_directory'], functionality_score)
                  self.check_readability(obj['cppaudit']['base_directory'], readability_score)
                                
    def overwrite_test_files(self, starter_code, problem_location):
        # copy Makefile
        # copy tools/cppaudit
        starter_code_loc = os.path.join("../", starter_code['location'])

        makefile_starter_loc = os.path.join(starter_code_loc, "Makefile")
        makefile_loc = os.path.join(self.code_dir, problem_location, "Makefile")
        shutil.copy(makefile_starter_loc, makefile_loc)

        unittest_starter_loc = os.path.join(starter_code_loc, "tools")
        unittest_loc = os.path.join(self.code_dir, problem_location, "tools")
        recursive_copy_with_overwrite(unittest_starter_loc, unittest_loc)

    def check_implementation(self, starter_code, problem_location, cppaudit):
        changes = 0
        score = 0
        msg = None
        starter_code_loc = os.path.join("../", starter_code['location'])
        
        # Code based on answer from: https://stackoverflow.com/questions/19120489/compare-two-files-report-difference-in-python
        for file in starter_code['files']:
          starter_file = open(os.path.join(starter_code_loc, file)).readlines()
          student_file = open(os.path.join(self.code_dir, problem_location, file)).readlines()
          for line in difflib.unified_diff(starter_file, student_file, lineterm='', n=0):
              for prefix in ('---', '+++', '@@'):
                  if line.startswith(prefix):
                      break
              else:
                  changes += 1
              
        if (changes < 5):
            msg = "The grader did not detect a solution to the problem."
        else:
            msg = "You are given full points assuming you submitted code that attempts to solve the problem. " \
                  "However, your score can change after manual grading if the grader finds that the code does " \
                  "not sufficiently solve the problem."
            score = cppaudit['implementation_score']
            
        self.results.append(make_test_output(
                            test_name="Implementation Test: {}".format(problem_location),
                            score=score,
                            max_score=cppaudit['implementation_score'],
                            output=msg,
                            visibility="visible"))

        if (score == 0):
            self.results.append(make_test_output(
                                test_name="Compilation Test: {}".format(problem_location),
                                score=0,
                                max_score=cppaudit['compilation_score'],
                                output=msg,
                                visibility="visible"))
            self.results.append(make_test_output(
                                test_name="Unit Test: {}".format(problem_location),
                                score=0,
                                max_score=cppaudit['functionality_score']['all_pass'],
                                output=msg,
                                visibility="visible"))
            self.results.append(make_test_output(
                                test_name="Style Check: {}".format(problem_location),
                                score=0,
                                max_score=cppaudit['readability_score']['style'],
                                output=msg,
                                visibility="visible"))
            self.results.append(make_test_output(
                                test_name="Format Check: {}".format(problem_location),
                                score=0,
                                max_score=cppaudit['readability_score']['format'],
                                output=msg,
                                visibility="visible"))
            
        return score

    def check_compilation(self, cwd, max_score):
        success = False
        score = None
        try:
          subprocess.check_output("make build", 
                                  cwd=os.path.join(self.code_dir, cwd), 
                                  timeout=10,
                                  stderr=subprocess.STDOUT,
                                  shell=True)
        except subprocess.TimeoutExpired:
          msg = "Compilation failed (timeout)."
        except subprocess.CalledProcessError as err:
          msg = "Compilation failed.\n\n" + err.output.decode() 
        else:
          msg = "Compilation succeeded!"
          success = True

        if success:
            score = max_score
        else:
            score = 0
            
        self.results.append(make_test_output(
            test_name="Compilation Test: {}".format(cwd),
            score=score,
            max_score=max_score,
            output=msg,
            visibility="visible"))
        
    def check_functionality(self, cwd, functionality_score):
        has_xml = True
        score = None
        output = None
        try:
          output = subprocess.check_output("make noskiptest", 
                                  cwd=os.path.join(self.code_dir, cwd), 
                                  timeout=30,
                                  stderr=subprocess.STDOUT,
                                  shell=True).decode()     
        except subprocess.TimeoutExpired:
          output = "Unit test failed (timeout)."
          has_xml = False
        except subprocess.CalledProcessError as err:
          output = "Unit test failed.\n\n" + err.output.decode()
          # if (err.stderr):
          #   output += err.stderr.decode()
          if (not(os.path.exists(os.path.join(self.code_dir, cwd, "tools/output/unittest.xml")))):
              has_xml = False

        if (has_xml):
            (feedback, score) = self.get_unittest_score(cwd, functionality_score)
            if ("ERROR: AddressSanitizer" in output or "ERROR: LeakSanitizer" in output):
                score -= functionality_score['mem_management_deduction']
                feedback += "\n\nMemory management issues were detected in your code."
            output = feedback + "\n\n" + output
    
        else:
            score = 0

        self.results.append(make_test_output(
                            test_name="Unit Test: {}".format(cwd),
                            score=score,
                            max_score=functionality_score['all_pass'],
                            output=output,
                            visibility="visible"))
        
    def check_readability(self, cwd, readability_score):
        self.check_style(cwd, readability_score['style'])
        self.check_format(cwd, readability_score['format'])          

    def check_style(self, cwd, style_score):
        success = False
        score = None
        try:
          output = subprocess.check_output("make stylecheck", 
                                           cwd=os.path.join(self.code_dir, cwd), 
                                           timeout=10,
                                           stderr=subprocess.STDOUT,
                                           shell=True).decode()
        except subprocess.TimeoutExpired:
          msg = "Style checker failed (timeout)."
        except subprocess.CalledProcessError as err:
          msg = "Style checker failed.\n\n" + err.output.decode() 
        else:
          if (": warning: " in output or ": error:" in output):
              msg = "Style checker failed.\n\n"
          else:
              msg = "Style checker succeeded!\n\n"
              success = True
          msg += output

        if success:
            score = style_score
        else:
            score = 0
            
        self.results.append(make_test_output(
            test_name="Style Check: {}".format(cwd),
            score=score,
            max_score=style_score,
            output=msg,
            visibility="visible"))

    def check_format(self, cwd, format_score):
        success = False
        score = None
        output = None
        try:
          output = subprocess.check_output("make formatcheck", 
                                           cwd=os.path.join(self.code_dir, cwd), 
                                           timeout=10,
                                           stderr=subprocess.STDOUT,
                                           shell=True).decode()
        except subprocess.TimeoutExpired:
          msg = "Format checker failed (timeout)."
        except subprocess.CalledProcessError as err:
          msg = "Format checker failed.\n\n" + err.output.decode() 
        else:
          if ("@@" in output):
            msg = "Format checker failed. Please modify your file format " \
                  "according to the following suggestions: \n\n"
            msg += output
          else:
            msg = "Format checker succeeded!\n\n"
            msg += output
            success = True

        if success:
            score = format_score
        else:
            score = 0
            
        self.results.append(make_test_output(
            test_name="Format Check: {}".format(cwd),
            score=score,
            max_score=format_score,
            output=msg,
            visibility="visible"))

    def get_unittest_score(self, cwd, functionality_score):
        """
        Googletest needs to use RecordProperty(key, value) with these keys:

        'points': how many points per test case if there's multiple, defaults to 1 if not set
        'max_score': max score for problem, default: points
        'visibility': if not set, uses Gradescope default
        'all_or_nothing': if True, a single failure in a test case => no points
                                   otherwise => max_score, default: False
        """
        score = 0
        feedback = None
        file = os.path.join(self.code_dir, cwd, "tools/output/unittest.xml")
        root = ET.parse(file).getroot()
        total = len([x for x in root.iter('testcase')])
        fails = len([x for x in root.iter('failure')])
        skips = len([x for x in root.iter('skipped')])
        corrects = total - fails - skips
        if (corrects == total):
            feedback = "All tests passed!"
            score = functionality_score['all_pass']
        elif (corrects > total / 2):
            feedback = "Over half of the tests passed."
            score = functionality_score['over_half_pass']
        elif (corrects > 0):
            feedback = "Less than half of the tests passed."
            score = functionality_score['less_half_pass']
        else:
            feedback = "No tests passed."
            score = functionality_score['no_pass']
        return (feedback, score)
