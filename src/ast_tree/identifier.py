from src.visitor.visitor import Visitor
# from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class Identifier(Node):
    def __init__(self, position, name, parent) -> None:
        self.position = position
        self.name = name
        self.parent = parent
        # self.type = AstType.IDENITIFIER

    def __repr__(self):
        return f"Identifier({self.position}, {self.name})"

    def __eq__(self, other):
        return (isinstance(other, Identifier) and
                other.name == self.name and
                other.parent == self.parent)

    def accept(self, visitor: Visitor):
        visitor.visit_object_access(self)
