class Autograder():
    """
    Defines an autograder object based on a YAML config file.
    
    YAML file format is:
    
    language: c++
    test_framework: googletest
    linter:
        enabled: true
        points: 10
    formatter:
        enabled: true
        points: 10
    code_dirs:
        - dirname/
        - dirname2/

    """
    
    language = None
    test_framework = None
    linter = None
    formatter = None
    code_dirs = []
    
    def __init__(self, config):
        # Init by parsing YAML config
        return