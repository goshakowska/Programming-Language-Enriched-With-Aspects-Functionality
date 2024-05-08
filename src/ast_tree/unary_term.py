from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class UnaryTerm:
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term
        self.type = AstType.UNARY_TERM

    def __repr__(self):
        return f"UnaryTerm({self.position}, {self.term})"

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_term(self)
