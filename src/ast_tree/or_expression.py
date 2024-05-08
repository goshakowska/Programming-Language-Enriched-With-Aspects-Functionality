from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class OrExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left = left_term
        self.right = right_term
        self.type = AstType.OR

    def __repr__(self):
        return f"OrExpression({self.left}, {self.right})"

    def __eq__(self, other):
        return (isinstance(other, OrExpression) and
                other.left == self.left and
                other.right == self.right)

    def accept(self, visitor: Visitor):
        return visitor.visit_or_expression(self)
