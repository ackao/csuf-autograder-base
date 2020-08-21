import yaml

class Autograder():
    """
    Defines an autograder object based on a YAML config file.

    self.language : string - must be one of the allowable languages (currently only c++)
    self.test_framework : string - must be an allowed framework (currently only googletest)
    self.linter : int - None if no linter, otherwise number of points
    self.formatter : int - None if no formatter, otherwise number of points
    self.code_dirs: [string] - list of directories containing student code

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

    def __init__(self, config):
        # Init by parsing YAML config
        with open(config, 'r') as file:
            cfg = yaml.safe_load(file)

            self.language = cfg['language']
            self.test_framework = cfg['test_framework']

            self.linter = None
            if 'linter' in cfg and cfg['linter']['enabled']:
                self.linter = cfg['linter']['points']

            self.formatter = None
            if 'formatter' in cfg and cfg['formatter']['enabled']:
                self.formatter = cfg['formatter']['points']

            self.code_dirs = cfg['code_dirs']

    def __str__(self):
        return "Autograder object(language={}, test_framework={}, linter={}, formatter={}, code_dirs={}".format(
            self.language,
            self.test_framework,
            self.linter,
            self.formatter,
            self.code_dirs)