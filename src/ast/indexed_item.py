from visitor import Visitor
from ast_type import AstType


class IndexedItem:
    def __init__(self, position, item, index) -> None:
        self.position = position
        self.item = item
        self.index = index
        self.type = AstType.INDEXED_ITEM

    def __repr__(self):
        return f"IndexedItem({self.position}, {self.item}, {self.index})"

    def accept(self, visitor: Visitor):
        return visitor.visit_indexed_item(self)
