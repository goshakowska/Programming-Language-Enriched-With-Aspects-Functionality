from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class CastedTerm:
    def __init__(self, position, term, casted_type) -> None:
        self.position = position
        self.term = term
        self.casted_type = casted_type
        self.type = AstType.CASTED_TERM

    def __repr__(self):
        return f"CastedTerm({self.position}, {self.term}, {self.casted_type})"

    def accept(self, visitor: Visitor):
        return visitor.visit_casted_term(self)
