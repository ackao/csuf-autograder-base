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

    def format_to_string(self, b):
        if type(b) is bytes:
            return repr(b.decode()).strip('"\'')
        if type(b) is str:
            return repr(b).strip('"\'')
        else:
            return b

    def assertEqual(self, input, expected, value, msg=None, fmt=None):
        if expected != value:
            if msg:
                return (False, msg)
            elif fmt:
                return (False, fmt.format(self.format_to_string(input), self.format_to_string(expected), self.format_to_string(value)))
            else:
                return (False, "Input:\n{}\nExpected output:\n{}\nYour program's output:\n{}".format(self.format_to_string(input), self.format_to_string(expected), self.format_to_string(value)))
        else:
            return (True, None)
