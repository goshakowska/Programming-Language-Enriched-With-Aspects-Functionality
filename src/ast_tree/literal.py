# from visitor import Visitor
# from ast_type import AstType

# class Literal:
#     def __init__(self, position, value, type) -> None:
#         self.position = position
#         self.value = value
#         self.type = AstType.LITERAL

#     def __repr__(self):
#         return f"Literal({self.position}, {self.value}, {self.type})"

#     def accept(self, visitor: Visitor):
#         return visitor.visit_literal(self)
