from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class FunctionCall:
    def __init__(self, position, name, arguments) -> None:
        self.position = position
        self.name = name
        self.arguments = arguments
        self.type = AstType.FUNCTION_CALL

    def __repr__(self):
        return f"FunctionCall({self.position}, {self.name}, {self.arguments})"

    def accept(self, visitor: Visitor):
        return visitor.visit_function_call(self)
