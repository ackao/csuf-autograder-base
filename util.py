"""
Miscellaneous utility functions for autograder
"""

def make_test_output(test_name=None, score=0, max_score=0, output="", visibility=None):
    """
    Return a dictionary representing results of a test.
    Fields are valid Gradescope autograder JSON.
    """
    output = {
        "score": score,
        "max_score": max_score,
        "output": output
    }
    if visibility:
        output["visibility"] = visibility
    if test_name:
        output["name"] = test_name

    return output

def format_to_string(obj):
    """
    Formatter to print strings and bytes without leading/trailing quotes
    """
    if isinstance(obj, bytes):
        return repr(obj.decode()).strip('"\'')
    if isinstance(obj, str):
        return repr(obj).strip('"\'')
    return obj

def encode_as_bytes(obj):
    """
    Convert any type to bytes
    """
    return str.encode(str(obj))
