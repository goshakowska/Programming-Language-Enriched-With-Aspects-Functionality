from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class PlusExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        self.type = AstType.PLUS

    def __repr__(self):
        return f"PlusExpression({self.position}, {self.left_term},\
              {self.right_term})"

    def __eq__(self, other):
        return (isinstance(other, PlusExpression) and
                other.left_term == self.left_term and
                other.right_term == self.right_term)

    def accept(self, visitor: Visitor):
        return visitor.visit_plus_expression(self)
