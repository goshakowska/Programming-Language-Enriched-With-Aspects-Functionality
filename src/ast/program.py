from visitor import Visitor


class Program:
    def __init__(self, functions: set, aspects: set, statements: list) -> None:
        self.functions = functions
        self.aspects = aspects
        self.statements = statements

    def accept(self, visitor: Visitor):
        return visitor.visit_program(self)

    def __repr__(self):
        return f"Program({self.functions}, {self.aspects}, {self.statements})"
