"""
Compiler class

Abstract class defining a compilation pass
"""

import os

class Compiler():
    """
    Abstract class defining a compilation pass
    """
    failures = None
    code = None
    code_dir = None
    build_dir = None
    results = None

    def __init__(self, code, code_dir, build_dir=None):
        self.failures = []
        self.code = code
        self.code_dir = code_dir
        self.build_dir = build_dir
        self.results = []

    def compile(self):
        """
        Runs test cases and returns Gradescope-readable JSON output
        """
        raise NotImplementedError

    @staticmethod
    def get_executable_name(filepath, build_dir=None):
        """
        Return executable name if build_dir is not specified.
        Otherwise returns fully qualified path of build_dir/exec_name
        """
        name = os.path.basename(os.path.splitext(filepath)[0])
        if build_dir:
            return os.path.join(build_dir, name)
        return name

    def get_failures(self):
        """
        Get failed compilation attempts
        """
        return self.failures
