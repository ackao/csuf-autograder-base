from test_runner import TestRunner

class GoogleTestRunner(TestRunner):
    def __init__(self):
        super().__init__()
    
    def run_test(self):
        return {}