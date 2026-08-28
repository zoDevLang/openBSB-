from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    blocks: List[Any]

@dataclass
class Block(ASTNode):
    name: Optional[str]
    args: Optional[List[Any]]
    body: List[Any]
    assign: Optional[Any] = None

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class NumberLiteral(ASTNode):
    value: int
