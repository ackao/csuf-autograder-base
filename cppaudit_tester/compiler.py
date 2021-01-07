"""
    CPPAuditCompiler class

    Compiles student code using CPPAudit's build functionality
"""

import os
import subprocess

from compiler import Compiler
from util import make_test_output

class CPPAuditCompiler(Compiler):
    """
    Compiles student code using CPPAudit's build functionality
    """

    def __init__(self, code, code_dir, build_dir):
        super().__init__(code, code_dir, build_dir)

    def compile(self):
        """
        Compiles student using CPPAudit's build functionality
        """
        for obj in self.code:
            implementation_score = obj['implementation_score']
            compilation_score = obj['compilation_score']
            functionality_score = obj['functionality_score']
            readability_score = obj['readability_score']
            max_score = obj.get('max_score', implementation_score + 
                                compilation_score + functionality_score + readability_score)
            success = False
            cmd = ["make build"]
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
                    self.failures.append(obj['problem'])

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

      
            srcs = [obj['main']] + obj.get('implems', [])
            max_score = obj.get('compile_points', None)
            success = False

            exec_name = self.get_executable_name(obj['main'], build_dir=self.build_dir)

            # Check that all files are present
            missing_srcs = []
            for src in srcs:
                if not os.path.isfile(os.path.join(self.code_dir, src)):
                    missing_srcs.append(src)
                cmd = ["g++", src]
                self.add_compile_command(file=src, command=" ".join(cmd))

            if missing_srcs:
                msg = "Required file(s) are missing: {}".format(missing_srcs)
            elif 'googletest' not in obj: # Compile executable if not using googletest
                cmd = ["g++", "-o", exec_name] + srcs
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
