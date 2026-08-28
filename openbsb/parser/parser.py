from typing import List, Optional
from openbsb.lexer.lexer import Token, Lexer
from openbsb.ast.nodes import Program, Block, StringLiteral, Identifier, NumberLiteral

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0]

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos]

    def expect(self, ttype: str):
        if self.current.type != ttype:
            raise ParserError(f"Expected {ttype} at {self.current.line}:{self.current.col}, got {self.current.type}")
        val = self.current
        self.advance()
        return val

    def parse(self):
        blocks = []
        while self.current.type != 'EOF':
            if self.current.type == 'LBRACE':
                blocks.append(self.parse_block())
                continue
            # skip unexpected tokens
            self.advance()
        return Program(blocks)

    def parse_block(self):
        self.expect('LBRACE')
        name = None
        args = None
        assign = None
        if self.current.type == 'IDENT':
            name = self.current.value
            self.advance()
            if self.current.type == 'LPAREN':
                args = self.parse_args()
        # possible assignment '='
        if self.current.type == 'EQUAL':
            self.advance()
            # value may be a block or literal
            if self.current.type == 'LBRACE':
                val_block = self.parse_block()
                assign = val_block
            elif self.current.type == 'STRING':
                assign = StringLiteral(self.current.value)
                self.advance()
            else:
                raise ParserError(f"Unexpected token after '=': {self.current}")
        body = []
        # parse body until RBRACE
        while self.current.type != 'RBRACE':
            if self.current.type == 'LBRACE':
                # nested block
                body.append(self.parse_block())
            elif self.current.type == 'STRING':
                body.append(StringLiteral(self.current.value)); self.advance()
            elif self.current.type == 'NUMBER':
                body.append(NumberLiteral(int(self.current.value))); self.advance()
            elif self.current.type == 'IDENT':
                # bare identifier as expression
                body.append(Identifier(self.current.value)); self.advance()
            elif self.current.type == 'EOF':
                raise ParserError('Unterminated block')
            else:
                # skip other tokens
                self.advance()
        self.expect('RBRACE')
        return Block(name, args, body, assign)

    def parse_args(self):
        self.expect('LPAREN')
        args = []
        while self.current.type != 'RPAREN':
            if self.current.type == 'IDENT':
                args.append(Identifier(self.current.value)); self.advance();
            elif self.current.type == 'STRING':
                args.append(StringLiteral(self.current.value)); self.advance();
            elif self.current.type == 'NUMBER':
                args.append(NumberLiteral(int(self.current.value))); self.advance();
            elif self.current.type == 'COMMA':
                self.advance();
            else:
                raise ParserError(f"Unexpected token in args: {self.current}")
        self.expect('RPAREN')
        return args
