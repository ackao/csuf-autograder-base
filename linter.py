"""
Linter class

Abstract class defining a linter pass
"""

class Linter():
    """
    Abstract class defining a linter pass
    """
    cfg = None
    code = None
    code_dir = None
    results = None
    test_name_fmt = "Linter Test: {}"

    def __init__(self, code, code_dir, linter_cfg):
        self.cfg = linter_cfg
        self.code = code
        self.code_dir = code_dir
        self.results = []

        if self.cfg:
            self.test_name_fmt = self.cfg.get('test_name', self.test_name_fmt)

    def run_linter(self):
        """
        Runs linter and returns Gradescope-readable JSON output
        """
        raise NotImplementedError

    def format_name(self, obj):
        """
        Returns string of test name formatted using test_name_fmt
        """
        return self.test_name_fmt.format(obj)
