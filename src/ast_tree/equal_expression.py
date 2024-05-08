from visitor import Visitor
from ast_type import AstType


class EqualExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.EQUAL

    def __repr__(self):
        return f"EqualExpression({self.position}, {self.left_term},\
              {self.right_term})"

    def accept(self, visitor: Visitor):
        return visitor.visit_equal_expression(self)
