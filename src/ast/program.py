from visitor import Visitor


class Program:
    def __init__(self, name: str, functions: set, aspects: set, 
                 statements: list) -> None:
        self.name = name
        self.functions = functions
        self.aspects = aspects
        self.statements = statements

    def __repr__(self):
        return f"Program({self.name}, {self.functions}, {self.aspects}, {self.statements})"

    def accept(self, visitor: Visitor):
        return visitor.visit_program(self)
