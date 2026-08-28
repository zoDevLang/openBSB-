#!/usr/bin/env python3
import argparse
import sys
from openbsb.lexer.lexer import Lexer
from openbsb.parser.parser import Parser
from openbsb.interpreter.interpreter import Interpreter

VERSION = '0.1.0'

def cmd_run(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    prog = parser.parse()
    interp = Interpreter(prog)
    return interp.run()

def cmd_ast(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    prog = parser.parse()
    import json
    def node_to_obj(node):
        if isinstance(node, list):
            return [node_to_obj(n) for n in node]
        if node is None:
            return None
        d = {'type': node.__class__.__name__}
        for k,v in node.__dict__.items():
            d[k]= node_to_obj(v)
        return d
    print(json.dumps(node_to_obj(prog), indent=2))
    return 0

def cmd_check(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        prog = parser.parse()
        print('OK')
        return 0
    except Exception as e:
        print('Error:', e)
        return 2

def main(argv=None):
    parser = argparse.ArgumentParser(prog='openbsb')
    sub = parser.add_subparsers(dest='cmd')
    runp = sub.add_parser('run')
    runp.add_argument('file')
    astp = sub.add_parser('ast')
    astp.add_argument('file')
    checkp = sub.add_parser('check')
    checkp.add_argument('file')
    sub.add_parser('version')

    args = parser.parse_args(argv)
    if args.cmd == 'run':
        return cmd_run(args.file)
    if args.cmd == 'ast':
        return cmd_ast(args.file)
    if args.cmd == 'check':
        return cmd_check(args.file)
    if args.cmd == 'version':
        print(VERSION); return 0
    parser.print_help(); return 1

if __name__ == '__main__':
    sys.exit(main())
