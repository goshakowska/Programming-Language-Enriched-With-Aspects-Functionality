from visitor import Visitor
from ast_type import AstType


class FloatLiteral:
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term
        self.type = AstType.FLOAT

    def __repr__(self):
        return f"Literal({self.position}, {self.term}, {self.type})"

    def accept(self, visitor: Visitor):
        return visitor.visit_float_literal(self)
