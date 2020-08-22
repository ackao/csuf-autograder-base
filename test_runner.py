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

    def assertEqual(self, expected, value, msg=None, fmt=None):
        if expected != value:
            if msg:
                return (False, msg)
            elif fmt:
                return (False, fmt.format(expected.value))
            else:
                return (False, "Expected output of {}, got {}".format(expected, value))
        else:
            return (True, None)