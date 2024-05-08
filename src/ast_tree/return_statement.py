from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class ReturnStatement:
    def __init__(self, position, expression):
        self.position = position
        self.expression = expression
        self.type = AstType.RETURN_STATEMENT

    def __repr__(self):
        return f"ReturnStatement({self.position}, {self.expression})"

    def accept(self, visitor: Visitor):
        return visitor.visit_return_statement(self)
