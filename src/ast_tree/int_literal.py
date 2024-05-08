from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class IntLiteral:
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term
        self.type = AstType.INT

    def __repr__(self):
        return f"Literal({self.position}, {self.term}, {self.type})"

    def __eq__(self, other):
        return (isinstance(other, IntLiteral) and
                other.term == self.term)

    def accept(self, visitor: Visitor):
        return visitor.visit_int_literal(self)
