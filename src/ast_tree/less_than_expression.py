from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class LessThanExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.LESS_THAN

    def __repr__(self):
        return f"LessThanExpression({self.position}, \
            {self.left_term}, {self.right_term})"

    def accept(self, visitor: Visitor):
        return visitor.visit_less_than_expression(self)
