from openbsb.lexer.lexer import Lexer
from openbsb.parser.parser import Parser
from openbsb.ast.nodes import Program, Block, StringLiteral

class InterpreterError(Exception):
    pass

class Interpreter:
    def __init__(self, program: Program):
        self.program = program
        self.env = {}

    def run(self):
        # find main block
        for blk in self.program.blocks:
            if isinstance(blk, Block) and blk.name == 'main':
                return self.execute_main(blk)
        raise InterpreterError('No main block found')

    def execute_main(self, main_blk: Block):
        # find p block inside main
        for item in main_blk.body:
            if isinstance(item, Block) and item.name == 'p':
                return self.execute_p(item)
        raise InterpreterError('No p block found in main')

    def execute_p(self, p_blk: Block):
        # p block body may contain nested block with STRING
        for inner in p_blk.body:
            if isinstance(inner, Block):
                for leaf in inner.body:
                    if isinstance(leaf, StringLiteral):
                        print(leaf.value)
                        return 0
            if isinstance(inner, StringLiteral):
                print(inner.value)
                return 0
        raise InterpreterError('p block has no string to print')

# convenience runner
def run_text(text: str):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    prog = parser.parse()
    interp = Interpreter(prog)
    return interp.run()
