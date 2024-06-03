from src.visitor.visitor import Visitor
from src.visitor.checker_visitor import CheckerVisitor
# from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class AndExpression(Node):
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term
        # self.type = AstType.AND

    def __repr__(self):
        return f"AndExpression({self.position}, {self.left_term}, {self.right_term})"

    def __eq__(self, other):
        return (isinstance(other, AndExpression) and
                other.left_term == self.left_term and
                other.right_term == self.right_term)

    def accept(self, visitor: Visitor):
        visitor.visit_and_expression(self)

    def accept_checker(self, visitor: CheckerVisitor):
        visitor.visit_and_expression(self)
