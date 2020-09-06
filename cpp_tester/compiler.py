import json
import yaml
import os
import subprocess

from classes.compiler import Compiler
from util import make_test_output

class CppCompiler(Compiler):
    compile_commands = None

    def __init__(self, code, code_dir, build_dir):
        self.compile_commands = []
        super().__init__(code, code_dir, build_dir)

    def compile(self):
        for obj in self.code:
            srcs = [obj['main']] + obj.get('implems', [])
            max_score = obj.get('compile_points', 0)
            ok = False

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
                self.add_compile_command_json(file=obj['main'], command=" ".join(cmd))
                try:
                    process = subprocess.run(cmd, cwd=self.code_dir, timeout=10)
                except subprocess.TimeoutExpired:
                    msg = "Compilation failed (timeout)"
                else:
                    if process.returncode != 0:
                        msg = "Compilation failed"
                    else:
                        msg = "Compilation succeeded"
                        ok = True

            if ok:
                score = max_score
            else:
                score = 0
                self.failures.append(self.get_executable_name(obj['main']))

            if max_score > 0:
                self.results.append(make_test_output(test_name="Compilation Test: {}".format(obj['main']),
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
