"""
    CppFormatter class

    Uses clang-format on student submissions and diffs with the original to find style errors.
"""

import difflib
import filecmp
import os
import shutil
import subprocess

from linter import Linter
from util import make_test_output

class CppFormatter(Linter):
    """
    Uses clang-format on student submissions and diffs with the original to find style errors.
    """

    clangfmt_path = "cpp_tester/.clang-format"
    custom_clangfmt_path = "../.clang-format"
    success_msg = "No style errors found"
    tmp_dir = None

    def __init__(self, code, code_dir, tmp_dir=tmp_dir):
        self.tmp_dir = tmp_dir
        super().__init__(code, code_dir)
        self.test_name_fmt = "Style check: {}"
        if os.path.exists(self.custom_clangfmt_path):
            shutil.copy(self.custom_clangfmt_path, code_dir)
        else:
            shutil.copy(self.clangfmt_path, code_dir)

    def run(self):
        tmpfile = os.path.join(self.tmp_dir, "clang_format_tmp")

        for obj in self.code:
            max_score = obj.get('style_points', 0)
            if max_score == 0:
                continue

            student_file = obj['main']
            cmd = ["clang-format", "-style=file", student_file]

            try:
                subprocess.run(
                    cmd,
                    cwd=self.code_dir,
                    timeout=30,
                    check=False,
                    stdout=open(tmpfile, "w+"))
            except subprocess.TimeoutExpired:
                msg = "Style check timed out"
                score = 0
            else:
                if filecmp.cmp(os.path.join(self.code_dir, student_file), tmpfile):
                    # Files match
                    msg = self.success_msg
                    score = max_score
                else:
                    # Files do not match, generate diff
                    score = 0
                    student_code = open(os.path.join(self.code_dir, student_file), "r").readlines()
                    formatted_code = open(tmpfile, "r").readlines()
                    diff = difflib.context_diff(
                        formatted_code,
                        student_code,
                        fromfile="Correctly formatted code",
                        tofile="Your code: {}".format(student_file))
                    msg = "".join(list(diff))

            self.results.append(make_test_output(
                test_name=self.format_name(student_file),
                score=score,
                max_score=max_score,
                output=msg,
                visibility="visible"))
