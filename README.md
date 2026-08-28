# OpenBSB — Starter implementation (Phase 1)

This repository contains a minimal, testable Phase-1 implementation of the OpenBSB compiler front-end.

What is included (Phase 1):
- Lexer
- Parser
- AST definitions
- Minimal interpreter to run the Hello World example
- CLI with `run`, `ast`, `check`, `version` commands
- Tests for lexer, parser and interpreter
- examples/hello.bsb

Quick start (requires Python 3.8+):

# run the example
python -m openbsb.cli.openbsb run examples/hello.bsb

# show AST
python -m openbsb.cli.openbsb ast examples/hello.bsb

# run tests
python -m unittest

Project layout follows the requested structure for later expansion.
