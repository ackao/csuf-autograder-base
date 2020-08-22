import json
import yaml
import os
import subprocess

from test_runner import TestRunner
from util import make_test_output

class CppCompileTestRunner(TestRunner):
    results = []

    def __init__(self, code_dir):
        self.code_dir = code_dir
        super().__init__()

    def run_test(self):
        with open('../tests/compile_test', 'r') as file:
            objs = yaml.load_all(file, Loader=yaml.FullLoader)

            for obj in objs:
                srcs = obj['sources']
                max_score = 0
                if 'points' in obj:
                    max_score = obj['points']


                # Check that all files are present
                missing_srcs = []
                for src in srcs:
                    if not os.path.isfile(os.path.join(self.code_dir, src)):
                        missing_srcs += src

                if missing_srcs != []:
                    msg = "Required file(s) are missing: {}".format(missing_srcs)
                    score = 0
                else: # Compile
                    cmd = ["g++"] + srcs
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
