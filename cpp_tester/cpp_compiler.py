"""
    CppCompiler class

    Compiles student C++ code and detects failures
"""

import os
import subprocess

from compiler import Compiler
from util import make_test_output

class CppCompiler(Compiler):
    """
    Compiles student C++ code and detects failures
    """
    compile_commands = None

    def __init__(self, code, code_dir, build_dir):
        self.compile_commands = []
        super().__init__(code, code_dir, build_dir)

    def compile(self):
        """
        Compiles student C++ code and detects failures
        """
        for obj in self.code:
            srcs = [obj['main']] + obj.get('implems', [])
            max_score = obj.get('compile_points', None)
            success = False

            exec_name = self.get_executable_name(obj['main'], build_dir=self.build_dir)

            # Check that all files are present
            missing_srcs = []
            for src in srcs:
                if not os.path.isfile(os.path.join(self.code_dir, src)):
                    missing_srcs.append(src)

            if missing_srcs:
                msg = "Required file(s) are missing: {}".format(missing_srcs)
            else: # Compile
                cmd = ["g++", "-o", exec_name] + srcs
                self.add_compile_command(file=obj['main'], command=" ".join(cmd))
                try:
                    subprocess.run(cmd, cwd=self.code_dir, timeout=10, check=True)
                except subprocess.TimeoutExpired:
                    msg = "Compilation failed (timeout)"
                except subprocess.CalledProcessError:
                    msg = "Compilation failed"
                else:
                    msg = "Compilation succeeded"
                    success = True

            if not success:
                self.failures.append(self.get_executable_name(obj['main']))

            if max_score is not None:
                if success:
                    score = max_score
                else:
                    score = 0
                self.results.append(make_test_output(
                    test_name="Compilation Test: {}".format(obj['main']),
                    score=score,
                    max_score=max_score,
                    output=msg,
                    visibility="visible"))

    def add_compile_command(self, file="", command=""):
        """
        Add command for this file that will be written to a compile_commands.json file for clang
        """
        self.compile_commands.append({
            "directory": self.code_dir,
            "command": command,
            "file": file
        })
