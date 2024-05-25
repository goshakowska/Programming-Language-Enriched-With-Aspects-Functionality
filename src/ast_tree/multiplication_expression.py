from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class MultiplicationExpression(Node):
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.MULTIPLICATION

    def __repr__(self):
        return f"MultiplicationExpression({self.position}, {self.left_term},\
              {self.right_term})"

    def __eq__(self, other):
        return (isinstance(other, MultiplicationExpression) and
                other.left_term == self.left_term and
                other.right_term == self.right_term)

    def accept(self, visitor: Visitor):
        return visitor.visit_multiplication_expression(self)
