from visitor import Visitor
from ast_type import AstType


class BoolLiteral:
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term
        self.type = AstType.BOOL

    def __repr__(self):
        return f"Literal({self.position}, {self.term}, {self.type})"

    def accept(self, visitor: Visitor):
        return visitor.visit_bool_literal(self)
