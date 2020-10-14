"""
Miscellaneous utility functions for autograder
"""

import os
import shutil

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

def decode_to_string(obj):
    """
    Convert any type to string
    """
    if isinstance(obj, bytes):
        return obj.decode()
    return str(obj)

def recursive_copy_with_overwrite(src, dst):
    """
    Copies contents of src directory to dst, overwriting existing files
    """
    for item in os.listdir(src):
        path = os.path.join(src, item)
        if os.path.isfile(path):
            shutil.copy(path, dst)
        elif os.path.isdir(path):
            new_dst = os.path.join(dst, item)
            if not os.path.exists(new_dst):
                os.mkdir(new_dst)
            recursive_copy_with_overwrite(path, new_dst)

def copy_dir_if_exists(src, dest):
    """
    Copies contents of src directory to dst if src exists
    """
    if os.path.exists(src):
        shutil.copytree(src, dest)
