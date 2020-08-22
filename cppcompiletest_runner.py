import json
import yaml
import os
import subprocess

from test_runner import TestRunner
from util import make_test_output, get_executable_name

class CppCompileTestRunner(TestRunner):
    results = []
    compile_commands = []

    def __init__(self, code, code_dir, build_dir):
        self.code = code
        self.code_dir = code_dir
        self.build_dir = build_dir
        super().__init__()

    def run_test(self):
        for obj in self.code:
            srcs = [obj['main']]
            if 'implems' in obj:
                srcs += obj['implems']

            max_score = 0
            if 'compile_points' in obj:
                max_score = obj['compile_points']

            # Check that all files are present
            missing_srcs = []
            for src in srcs:
                if not os.path.isfile(os.path.join(self.code_dir, src)):
                    missing_srcs += src

            if missing_srcs != []:
                msg = "Required file(s) are missing: {}".format(missing_srcs)
                score = 0
            else: # Compile
                cmd = ["g++", "-o", get_executable_name(obj['main'], build_dir=self.build_dir)] + srcs
                self.add_compile_command_json(file=obj['main'], command=" ".join(cmd))
                process = subprocess.run(cmd, cwd=self.code_dir)

                if process.returncode != 0:
                    msg = "Compilation failed: {}".format(" ".join(cmd))
                    score = 0
                else:
                    msg = "Compilation succeeded: {}".format(" ".join(cmd))
                    score = max_score


            self.results.append(make_test_output(test_name="Compilation Test",
                                        score=score,
                                        max_score=max_score,
                                        output=msg,
                                        visibility="visible"))

    def add_compile_command_json(self, file="", command=""):
        self.compile_commands.append({
            "directory": self.code_dir,
            "command": command,
            "file": file
        })