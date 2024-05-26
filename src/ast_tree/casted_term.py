from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class CastedTerm(Node):
    def __init__(self, position, term, casted_type) -> None:
        self.position = position
        self.term = term
        self.casted_type = casted_type
        self.type = AstType.CASTED_TERM

    def __repr__(self):
        return f"CastedTerm({self.position}, {self.term}, {self.casted_type})"

    def __eq__(self, other):
        return (isinstance(other, CastedTerm) and
                other.term == self.term and
                other.casted_type == self.casted_type)

    def accept(self, visitor: Visitor):
        visitor.visit_casted_term(self)
