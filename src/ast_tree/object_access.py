from visitor import Visitor
from ast_type import AstType


class ObjectAccess:
    def __init__(self, position, item, dot_item) -> None:
        self.position = position
        self.item = item
        self.dot_item = dot_item
        self.type = AstType.OBJECT_ACCESS

    def __repr__(self):
        return f"ObjectAccess({self.position}, {self.item}, {self.dot_item})"

    def accept(self, visitor: Visitor):
        return visitor.visit_object_access(self)
