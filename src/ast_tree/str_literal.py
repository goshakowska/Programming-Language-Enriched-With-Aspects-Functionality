from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class StrLiteral(Node):
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term  # czy lepiej value?
        self.type = AstType.STR

    def __repr__(self):
        return f"Literal({self.position}, {self.term}, {self.type})"

    def __eq__(self, other):
        return (isinstance(other, StrLiteral) and
                other.term == self.term)

    def accept(self, visitor: Visitor):
        visitor.visit_str_literal(self)
