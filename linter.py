import json
import yaml
import os
import subprocess

from test_runner import TestRunner
from util import make_test_output
import yaml

class CppLinter(TestRunner):
    results = []
    CLANGTDY_CHKS = "*,-google-build-using-namespace,-fuchsia-default-arguments,-llvm-header-guard"

    def __init__(self, code_dir, max_score):
        self.code_dir = code_dir
        self.max_score = max_score
        super().__init__()

    def run_test(self):
        with open('../tests/compile_test', 'r') as file:
            objs = yaml.load_all(file, Loader=yaml.FullLoader)

            for obj in objs:
                srcs = obj['sources']

                cmd = ["clang-tidy", "-checks={}".format(self.CLANGTDY_CHKS), "--warnings-as-errors=*", "-header-filter=.*", srcs[0]]
                process = subprocess.run(cmd, cwd=self.code_dir)

                if process.returncode != 0:
                    msg = "Linter returned errors: {}".format(" ".join(cmd))
                    score = 0
                else:
                    msg = "No linter errors for file: {}".format(srcs[0])
                    score = self.max_score

                self.results.append(make_test_output(test_name="Linter Test",
                                            score=score,
                                            max_score=self.max_score,
                                            output=msg,
                                            visibility="visible"))

