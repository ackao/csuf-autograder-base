class TestRunner():
    """
    Parent class for running any kind of unit testing
    """
    def __init__(self):
        return

    """
    Runs test cases and returns Gradescope-readable JSON output
    """
    @classmethod
    def run_test(self):
        raise NotImplementedError