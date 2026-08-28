import unittest
from openbsb.lexer.lexer import Lexer
from openbsb.parser.parser import Parser

class TestParser(unittest.TestCase):
    def test_parse_hello(self):
        text = '{main{p}{p{"hello world"}}}'
        tokens = Lexer(text).tokenize()
        prog = Parser(tokens).parse()
        self.assertTrue(len(prog.blocks) > 0)
        self.assertEqual(prog.blocks[0].name, 'main')

if __name__ == '__main__':
    unittest.main()
