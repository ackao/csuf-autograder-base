import json
import os

def make_test_output(test_name=None, score=0, max_score=0, output="", visibility=None):
    o = {
            "score": score,
            "max_score": max_score,
            "output": output
        }
    if visibility:
        o["visibility"] = visibility
    if test_name:
        o["name"] = test_name

    return o

def format_to_string(b):
    if type(b) is bytes:
        return repr(b.decode()).strip('"\'')
    if type(b) is str:
        return repr(b).strip('"\'')
    else:
        return b

def encode_as_bytes(x):
    return str.encode(str(x))