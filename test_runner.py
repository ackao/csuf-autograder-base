"""
TestRunner class

Abstract class for running any kind of unit testing
"""
from util import format_to_string

class TestRunner():
    """
    Parent class for running any kind of unit testing
    """
    results = None
    skip = None

    def __init__(self):
        self.results = []
        self.skip = []

    def run_test(self):
        """
        Runs test cases and returns Gradescope-readable JSON output
        """
        raise NotImplementedError

    @staticmethod
    def assert_equal(stdin, expected, value, msg=None, fmt=None):
        """
        Returns whether value and expected are equal.
        If not, returns a string containing a message or a formatted string
        """
        if expected != value:
            if msg:
                return (False, msg)
            if fmt:
                return (False, fmt.format(
                    format_to_string(stdin),
                    format_to_string(expected),
                    format_to_string(value)))
            return (False,
                    "Input:\n{}\nExpected output:\n{}\nYour program's output:\n{}".format(
                        format_to_string(stdin),
                        format_to_string(expected),
                        format_to_string(value)))
        return (True, None)

    def set_skip(self, skip):
        """
        Sets skip to a list of tests to skip
        """
        self.skip = skip

    def get_skip(self):
        """
        Gets skip
        """
        return self.skip
