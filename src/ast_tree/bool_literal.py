from src.visitor.visitor import Visitor
from src.visitor.checker_visitor import CheckerVisitor
from src.ast_tree.ast_type import AstType


class BoolLiteral:
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term
        self.type = AstType.BOOL

    def __repr__(self):
        return f"Literal({self.position}, {self.term}, {self.type})"

    def __eq__(self, other):
        return (isinstance(other, BoolLiteral) and
                other.term == self.term)

    def accept(self, visitor: Visitor):
        return visitor.visit_bool_literal(self)

    def accept_checker(self, visitor: CheckerVisitor):
        return visitor.visit_bool_literal(self)
