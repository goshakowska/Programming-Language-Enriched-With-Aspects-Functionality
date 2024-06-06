from src.visitor.visitor import Visitor
# from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class FloatLiteral(Node):
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term
        # self.type = AstType.FLOAT

    def __repr__(self):
        return f"Literal({self.position}, {self.term})"

    def __eq__(self, other):
        return (isinstance(other, FloatLiteral) and
                other.term == self.term)

    def accept(self, visitor: Visitor):
        visitor.visit_float_literal(self)
