import json

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

    return json.dumps(o)