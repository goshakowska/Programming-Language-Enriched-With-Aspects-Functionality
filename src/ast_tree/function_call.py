from src.visitor.visitor import Visitor
# from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class FunctionCall(Node):
    def __init__(self, position, name, arguments, parent) -> None:
        self.position = position
        self.name = name
        self.arguments = arguments
        self.parent = parent
        # self.type = AstType.FUNCTION_CALL

    def __repr__(self):
        return f"FunctionCall({self.position}, {self.name}, {self.arguments})"

    def __eq__(self, other):
        return (isinstance(other, FunctionCall) and
                other.name == self.name
                and other.arguments == self.arguments
                and other.parent == self.parent)

    def accept(self, visitor: Visitor):
        visitor.visit_object_access(self)
