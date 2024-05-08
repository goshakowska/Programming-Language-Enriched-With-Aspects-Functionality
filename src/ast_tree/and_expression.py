from src.visitor.visitor import Visitor
from src.visitor.checker_visitor import CheckerVisitor
from src.ast_tree.ast_type import AstType


class AndExpression:
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left = left_term
        self.right = right_term
        self.type = AstType.AND

    def __repr__(self):
        return f"AndExpression({self.position}, {self.left}, {self.right})"

    def __eq__(self, other):
        return (isinstance(other, AndExpression) and
                other.left == self.left and
                other.right == self.right)

    def accept(self, visitor: Visitor):
        return visitor.visit_and_expression(self)

    def accept_checker(self, visitor: CheckerVisitor):
        return visitor.visit_and_expression(self)
