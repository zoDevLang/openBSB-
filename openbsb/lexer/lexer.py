from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r}, {self.line}, {self.col})"

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current = self.text[self.pos] if self.text else None

    def advance(self):
        if self.current == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1
        self.current = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        nxt = self.text[self.pos+1] if self.pos+1 < len(self.text) else None
        return nxt

    def skip_whitespace(self):
        while self.current is not None and self.current.isspace():
            self.advance()

    def read_string(self):
        # current is '"'
        start_line, start_col = self.line, self.col
        self.advance()  # skip opening quote
        chars = []
        while self.current is not None and self.current != '"':
            if self.current == '\\':
                self.advance()
                if self.current is None:
                    raise LexerError(f"Unterminated escape at {self.line}:{self.col}")
                escapes = {'n':'\n','t':'\t','"':'"','\\':'\\'}
                chars.append(escapes.get(self.current, self.current))
                self.advance()
            else:
                chars.append(self.current)
                self.advance()
        if self.current != '"':
            raise LexerError(f"Unterminated string at {start_line}:{start_col}")
        self.advance()  # skip closing quote
        return Token('STRING', ''.join(chars), start_line, start_col)

    def read_identifier(self):
        start_line, start_col = self.line, self.col
        chars = []
        while self.current is not None and (self.current.isalnum() or self.current in ['_','.',':']):
            chars.append(self.current)
            self.advance()
        return Token('IDENT', ''.join(chars), start_line, start_col)

    def read_number(self):
        start_line, start_col = self.line, self.col
        chars = []
        while self.current is not None and self.current.isdigit():
            chars.append(self.current)
            self.advance()
        return Token('NUMBER', ''.join(chars), start_line, start_col)

    def tokenize(self):
        tokens = []
        while self.current is not None:
            if self.current.isspace():
                self.skip_whitespace()
                continue
            if self.current == '{':
                tokens.append(Token('LBRACE','{',self.line,self.col)); self.advance(); continue
            if self.current == '}':
                tokens.append(Token('RBRACE','}',self.line,self.col)); self.advance(); continue
            if self.current == '(':
                tokens.append(Token('LPAREN','(',self.line,self.col)); self.advance(); continue
            if self.current == ')':
                tokens.append(Token('RPAREN',')',self.line,self.col)); self.advance(); continue
            if self.current == '=':
                # support '==' as operator
                if self.peek() == '=':
                    start_line, start_col = self.line, self.col
                    self.advance(); self.advance()
                    tokens.append(Token('EQEQ','==',start_line,start_col))
                else:
                    tokens.append(Token('EQUAL','=',self.line,self.col)); self.advance()
                continue
            if self.current == '"':
                tokens.append(self.read_string()); continue
            if self.current.isalpha() or self.current in ['_']:
                tokens.append(self.read_identifier()); continue
            if self.current.isdigit():
                tokens.append(self.read_number()); continue
            # Operators
            if self.current in ['<','>','!','+','-','*','/']:
                start_line, start_col = self.line, self.col
                op = self.current
                if self.peek() == '=':
                    op += '='
                    self.advance();
                    self.advance();
                else:
                    self.advance();
                tokens.append(Token('OP',op,start_line,start_col))
                continue
            # commas
            if self.current == ',':
                tokens.append(Token('COMMA',',',self.line,self.col)); self.advance(); continue

            raise LexerError(f"Unknown character {self.current!r} at {self.line}:{self.col}")
        tokens.append(Token('EOF','',self.line,self.col))
        return tokens
