"""
    Defines an autograder object based on a YAML config file.
"""

import json
import yaml

from general_tester.blackboxtest_runner import BlackBoxTestRunner
from cpp_tester.cpp_compiler import CppCompiler
from cpp_tester.linter import CppLinter

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

    def __init__(self, config, code_dir, build_dir, debug=False):
        # Init by parsing YAML config
        with open(config, 'r') as file:
            cfg = yaml.safe_load(file)
            if debug:
                print(cfg)

            self.code_dir = code_dir
            self.build_dir = build_dir

            self.linter = None
            self.formatter = None
            self.tester = None

            if cfg['language'] == 'c++':
                self.compiler = CppCompiler(cfg['code'], self.code_dir, self.build_dir)
                if 'linter' in cfg and cfg['linter']:
                    self.linter = CppLinter(cfg['code'], self.code_dir)
                if 'formatter' in cfg and cfg['formatter']:
                    raise NotImplementedError

            if cfg['test_framework'] == 'blackbox':
                self.tester = BlackBoxTestRunner(cfg['blackbox_tests'], self.build_dir)

    def __str__(self):
        return "Autograder(linter={}, formatter={}, code_dir={}".format(
            self.linter,
            self.formatter,
            self.code_dir)

    def make_json(self):
        """
        Return Gradescope-formatted JSON with all results
        """
        tests = self.compiler.results
        if self.linter:
            tests += self.linter.results
        if self.formatter:
            tests += self.formatter.results
        tests += self.tester.results

        output = {
            "visibility" : "visible",
            "stdout_visibility": "visible",
            "tests": tests
        }
        return json.dumps(output)
