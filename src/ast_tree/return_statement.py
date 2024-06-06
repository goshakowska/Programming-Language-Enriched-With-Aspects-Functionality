from src.visitor.visitor import Visitor
# from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class ReturnStatement(Node):
    def __init__(self, position, expression):
        self.position = position
        self.expression = expression
        # self.type = AstType.RETURN_STATEMENT

    def __repr__(self):
        return f"ReturnStatement({self.position}, {self.expression})"

    def __eq__(self, other):
        return (isinstance(other, ReturnStatement) and
                other.expression == self.expression)

    def accept(self, visitor: Visitor):
        visitor.visit_return_statement(self)
