from visitor import Visitor
from ast_type import AstType


class MultiplicationExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.MULTIPLICATION

    def __repr__(self):
        return f"MultiplicationExpression({self.left_term}, {self.right_term})"

    def accept(self, visitor: Visitor):
        return visitor.visit_multiplication_expression(self)
