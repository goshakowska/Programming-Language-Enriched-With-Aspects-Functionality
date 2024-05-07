from visitor import Visitor
from ast.ast_type import AstType


class AndExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left = left_term
        self.right = right_term
        self.type = AstType.AND

    def __repr__(self):
        return f"AndExpression({self.left}, {self.right})"

    def accept(self, visitor: Visitor):
        return visitor.visit_and_expression(self)
