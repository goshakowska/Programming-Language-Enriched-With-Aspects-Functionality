from src.visitor.visitor import Visitor
from src.ast_tree.node import Node


class Program(Node):
    def __init__(self, name: str, functions: dict, aspects: dict,
                 statements: list) -> None:
        self.name = name
        self.functions = functions
        self.aspects = aspects
        self.statements = statements
        # self.type = AstType.PROGRAM

    def __repr__(self):
        return f"Program({self.name}, {self.functions}, {self.aspects},\
              {self.statements})"

    def __eq__(self, other):
        return (isinstance(other, Program) and
                other.name == self.name and
                other.functions == self.functions and
                other.aspects == self.aspects and
                other.statements == self.statements)

    def accept(self, visitor: Visitor):
        visitor.visit_program(self)
