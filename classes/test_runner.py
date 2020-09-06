from util import format_to_string

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

    def assertEqual(self, input, expected, value, msg=None, fmt=None):
        if expected != value:
            if msg:
                return (False, msg)
            elif fmt:
                return (False, fmt.format(format_to_string(input), format_to_string(expected), format_to_string(value)))
            else:
                return (False, "Input:\n{}\nExpected output:\n{}\nYour program's output:\n{}".format(format_to_string(input), format_to_string(expected), format_to_string(value)))
        else:
            return (True, None)
