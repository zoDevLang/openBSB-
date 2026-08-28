import unittest
from openbsb.interpreter.interpreter import run_text

class TestInterpreter(unittest.TestCase):
    def test_run_hello(self):
        text = '{main{p}{p{"hello world"}}}'
        # should not raise
        run_text(text)

if __name__ == '__main__':
    unittest.main()
