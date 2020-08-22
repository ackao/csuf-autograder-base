import json
import os
import subprocess

from test_runner import TestRunner
from util import make_test_output, get_executable_name

class CppLinter(TestRunner):
    results = []
    CLANGTDY_CHKS = "*,-google-build-using-namespace,-fuchsia-default-arguments,-llvm-header-guard"

    def __init__(self, code, code_dir):
        self.code = code
        self.code_dir = code_dir
        super().__init__()

    def run_test(self):
        for obj in self.code:
            main = obj['main']

            cmd = ["clang-tidy", "-checks={}".format(self.CLANGTDY_CHKS), "--warnings-as-errors=*", "-header-filter=.*", main]
            process = subprocess.run(cmd, cwd=self.code_dir)

            if process.returncode != 0:
                msg = "Linter returned errors: {}".format(" ".join(cmd))
                score = 0
            else:
                msg = "No linter errors for file: {}".format(main)
                score = obj['linter_points']

            self.results.append(make_test_output(test_name="Linter Test",
                                score=score,
                                max_score=obj['linter_points'],
                                output=msg,
                                visibility="visible"))

