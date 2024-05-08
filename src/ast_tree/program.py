from visitor import Visitor
from ast_type import AstType


class Program:
    def __init__(self, name: str, functions: set, aspects: set,
                 statements: list) -> None:
        self.name = name
        self.functions = functions
        self.aspects = aspects
        self.statements = statements
        self.type = AstType.PROGRAM

    def __repr__(self):
        return f"Program({self.name}, {self.functions}, {self.aspects},\
              {self.statements})"

    def accept(self, visitor: Visitor):
        return visitor.visit_program(self)
