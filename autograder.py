"""
    Defines an autograder object based on a YAML config file.
"""

import json
import yaml

from general_tester.blackboxtest_runner import BlackBoxTestRunner
from cpp_tester.cpp_compiler import CppCompiler
from cpp_tester.cpp_format import CppFormatter
from cpp_tester.cpp_linter import CppLinter
from cpp_tester.googletest_runner import GoogleTestRunner
from cppaudit_tester.cppaudit_runner import CPPAuditRunner
class Autograder():
    """
    Defines an autograder object based on a YAML config file.

    self.language : string - must be one of the allowable languages (currently only c++)
    self.test_framework : string - must be an allowed framework (currently only googletest)
    self.linter : CppLinter object - None if no linter, otherwise number of points
    self.formatter : int - None if no formatter, otherwise number of points
    self.code_dir: directory containing student code
    self.compiler : TestRunner - compiler test runner object

    YAML file format is:

    language: c++
    test_framework: googletest
    linter:
        enabled: true
        points: 10
    formatter:
        enabled: true
        points: 10

    """

    def __init__(self, config, code_dir, build_dir, test_dir):
        # Init by parsing YAML config
        with open(config, 'r') as file:
            cfg = yaml.safe_load(file)

            self.code_dir = code_dir
            self.build_dir = build_dir

            self.compiler = None
            self.linter = None
            self.stylecheck = None
            self.tester = None
            self.score_override = cfg.get('score_override', None)

            linter_cfg = cfg.get('linter', None)
            style_cfg = cfg.get('style_check', None)

            if cfg['language'] == 'c++':
              if cfg['test_framework'] != 'cppaudit':
                self.compiler = CppCompiler(cfg['code'], self.code_dir, self.build_dir)
                if linter_cfg and linter_cfg.get('enable', True):
                    self.linter = CppLinter(cfg['code'], self.code_dir, linter_cfg)
                if style_cfg and style_cfg.get('enable', True):
                    self.stylecheck = CppFormatter(
                        cfg['code'],
                        self.code_dir,
                        style_cfg,
                        self.build_dir)

            if cfg['test_framework'] == 'blackbox':
                self.tester = BlackBoxTestRunner(cfg['blackbox_tests'], self.build_dir)
            elif cfg['test_framework'] == 'googletest':
                self.tester = GoogleTestRunner(cfg['code'], test_dir, self.code_dir)
            elif cfg['test_framework'] == 'cppaudit':
                self.tester = CPPAuditRunner(cfg['code'], self.code_dir)

    def __str__(self):
        return "Autograder(linter={}, stylecheck={}, code_dir={}".format(
            self.linter,
            self.stylecheck,
            self.code_dir)

    def make_json(self):
        """
        Return Gradescope-formatted JSON with all results
        """
        tests = []
        if self.compiler:
            tests = self.compiler.results
        if self.linter:
            tests += self.linter.results
        if self.stylecheck:
            tests += self.stylecheck.results
        tests += self.tester.results

        output = {
            "visibility" : "visible",
            "stdout_visibility": "visible",
            "tests": tests
        }

        if self.score_override is not None:
            output["score"] = self.score_override
        # print(output)
        return json.dumps(output)
