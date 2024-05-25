from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class GreaterThanExpression(Node):
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.GREATER_THAN

    def __repr__(self):
        return f"GreaterThanExpression({self.position}, {self.left_term},\
              {self.right_term})"

    def __eq__(self, other):
        return (isinstance(other, GreaterThanExpression) and
                other.left_term == self.left_term and
                other.right_term == self.right_term)

    def accept(self, visitor: Visitor):
        return visitor.visit_greater_than_expression(self)
