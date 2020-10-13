"""
TestRunner class

Abstract class for running any kind of unit testing
"""
import difflib

from util import format_to_string, decode_to_string

class TestRunner():
    """
    Parent class for running any kind of unit testing
    """
    results = None
    skip = None
    MAX_OUTPUT_LENGTH = 10000

    def __init__(self):
        self.results = []
        self.skip = []

    def run_test(self):
        """
        Runs test cases and returns Gradescope-readable JSON output
        """
        raise NotImplementedError

    @classmethod
    def assert_equal(cls, stdin, expected, value, desc="Output"):
        """
        Returns whether value and expected are equal.
        If not, returns a string containing a message or a formatted string
        """
        exp_msg = "Expected {}".format(desc)
        got_msg = "Your Program's {}".format(desc)

        value = decode_to_string(value)
        expected = decode_to_string(expected)

        if expected != value:
            value = value.splitlines(keepends=True)
            if len(value) > cls.MAX_OUTPUT_LENGTH:
                result = "Input: {}\nYour code produced too much output.\n".format(format_to_string(stdin))
                return (False, result)
            expected = expected.splitlines(keepends=True)
            diff = difflib.context_diff(expected, value, fromfile=exp_msg, tofile=got_msg, n=100)
            result = "Input: {}\n".format(format_to_string(stdin)) + "".join(list(diff))
            return (False, result)
        return (True, None)

    @staticmethod
    def check_exitcode(stdin, expected, got, fmt=None):
        """
        Returns whether got == expected
        Formats an appropriate message for gradescope to print
        """
        if expected == got:
            return (True, None)
        msg = "Input: {}\nExpected Exit Code: {}\nYour Program's Exit Code: {}"
        if fmt:
            msg = fmt
        return (False, msg.format(format_to_string(stdin), expected, got))

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
