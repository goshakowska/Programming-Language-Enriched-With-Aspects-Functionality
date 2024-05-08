from visitor import Visitor
from ast_type import AstType


class GreaterThanExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.GREATER_THAN

    def __repr__(self):
        return f"GreaterThanExpression({self.left_term}, {self.right_term})"

    def accept(self, visitor: Visitor):
        return visitor.visit_greater_than_expression(self)
