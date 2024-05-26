from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class GreaterThanOrEqualExpression(Node):
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.GREATER_THAN_OR_EQUAL

    def __repr__(self):
        return f"GreaterThanOrEqualExpression(\
            {self.position}, {self.left_term}, {self.right_term})"

    def __eq__(self, other):
        return (isinstance(other, GreaterThanOrEqualExpression) and
                other.left_term == self.left_term and
                other.right_term == self.right_term)

    def accept(self, visitor: Visitor):
        visitor.visit_greater_than_or_equal_expression(self)
