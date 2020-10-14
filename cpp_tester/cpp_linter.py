"""
    CppLinter class

    Uses clang-tidy to lint student submissions
"""

import subprocess

from linter import Linter
from util import make_test_output

class CppLinter(Linter):
    """
    Uses clang-tidy to lint student submissions
    """

    CLANGTDY_CHKS = "*,-google-build-using-namespace,-fuchsia-default-arguments,-llvm-header-guard"
    custom_checks = None
    success_msg = "No linter errors found"
    failure_msg = "Linter returned errors"
    files = {}

    def __init__(self, code, code_dir, cfg):
        super().__init__(code, code_dir, linter_cfg=cfg)
        if self.cfg:
            self.custom_checks = self.cfg.get('checks', None)
            self.success_msg = self.cfg.get('success_message', self.success_msg)
            self.failure_msg = self.cfg.get('failure_message', self.failure_msg)
            for lint in self.cfg.get('files', []):
                self.files[lint['file']] = lint.get('points', 1)


    def run(self):
        for (obj, max_score) in self.files.items():
            if max_score == 0:
                continue

            if self.custom_checks:
                checks = self.custom_checks
            else:
                checks = self.CLANGTDY_CHKS

            cmd = ["clang-tidy", "-checks={}".format(checks), "--warnings-as-errors=*", obj]

            try:
                process = subprocess.run(
                    cmd,
                    cwd=self.code_dir,
                    timeout=30,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            except subprocess.TimeoutExpired:
                msg = "Linter timed out"
                score = 0
            else:
                if process.returncode != 0:
                    msg = self.failure_msg
                    score = 0
                else:
                    msg = self.success_msg
                    score = max_score

            self.results.append(make_test_output(
                test_name=self.format_name(obj),
                score=score,
                max_score=max_score,
                output=msg,
                visibility="visible"))
