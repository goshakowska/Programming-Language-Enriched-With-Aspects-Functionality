from visitor import Visitor


class FunctionCall:
    def __init__(self, position, name, parameters) -> None:
        self.position = position
        self.name = name
        self.parameters = parameters

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.parameters})"

    def accept(self, visitor: Visitor):
        return visitor.visit_function_call(self)
