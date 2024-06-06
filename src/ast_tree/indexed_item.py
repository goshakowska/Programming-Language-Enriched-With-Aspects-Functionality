# from src.visitor.visitor import Visitor
# # from src.ast_tree.ast_type import AstType
# from src.ast_tree.node import Node


# class IndexedItem(Node):
#     def __init__(self, position, item, index) -> None:
#         self.position = position
#         self.item = item
#         self.index = index
#         # self.type = AstType.INDEXED_ITEM

#     def __repr__(self):
#         return f"IndexedItem({self.position}, {self.item}, {self.index})"

#     def __eq__(self, other):
#         return (isinstance(other, IndexedItem) and
#                 other.item == self.item and
#                 other.index == self.index)

#     def accept(self, visitor: Visitor):
#         visitor.visit_indexed_item(self)
