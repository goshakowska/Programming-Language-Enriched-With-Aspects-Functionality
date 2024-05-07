from visitor import Visitor


class FunctionDefinition:
    def __init__(self, position, name, params, return_type) -> None:
        self.position = position
        self.name = name
        self.params = params
        self.return_type = return_type

    def accept(self, visitor: Visitor):
        return visitor.visit_function_definition(self)
