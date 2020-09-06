import os
from util import format_to_string

class Compiler():
    failures = None
    code = None
    code_dir = None
    build_dir = None
    results = None

    """
    Parent class for compiling student code
    """
    def __init__(self, code, code_dir, build_dir=None):
        self.failures = []
        self.code = code
        self.code_dir = code_dir
        self.build_dir = build_dir
        self.results = []
        return

    """
    Runs test cases and returns Gradescope-readable JSON output
    """
    @classmethod
    def compile(self):
        raise NotImplementedError

    @staticmethod
    def get_executable_name(filepath, build_dir=None):
        name = os.path.basename(os.path.splitext(filepath)[0])
        if build_dir:
            return os.path.join(build_dir, name)
        return name

    def get_failures(self):
        return self.failures