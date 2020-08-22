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

def get_executable_name(filepath, build_dir=None):
    name = os.path.basename(os.path.splitext(filepath)[0])
    if build_dir:
        return os.path.join(build_dir, name)
    return name