from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class FunctionDefinition:
    def __init__(self, position, name, params, block, return_type) -> None:
        self.position = position
        self.name = name
        self.params = params
        self.block = block
        self.return_type = return_type
        self.type = AstType.FUNCTION

    def __repr__(self):
        return f"FunctionDefinition({self.position}, {self.name},\
              {self.params}, {self.return_type}, {self.block})"

    def __eq__(self, other):
        return (isinstance(other, FunctionDefinition) and
                other.name == self.name)

    def accept(self, visitor: Visitor):
        return visitor.visit_function_definition(self)
