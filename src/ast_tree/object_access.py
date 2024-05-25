from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class ObjectAccess(Node):
    def __init__(self, position, item, dot_item) -> None:
        self.position = position
        self.item = item
        self.dot_item = dot_item
        self.type = AstType.OBJECT_ACCESS

    def __repr__(self):
        return f"ObjectAccess({self.position}, {self.item}, {self.dot_item})"

    def __eq__(self, other):
        return (isinstance(other, ObjectAccess) and
                other.item == self.item and
                other.dot_item == self.dot_item)

    def accept(self, visitor: Visitor):
        return visitor.visit_object_access(self)
