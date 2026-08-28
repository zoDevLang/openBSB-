import unittest
from openbsb.lexer.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_hello_tokens(self):
        text = '{main{p}{p"hello"}}'
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertIn('LBRACE', types)
        self.assertIn('RBRACE', types)
        self.assertIn('IDENT', types)
        self.assertIn('STRING', types)

if __name__ == '__main__':
    unittest.main()
