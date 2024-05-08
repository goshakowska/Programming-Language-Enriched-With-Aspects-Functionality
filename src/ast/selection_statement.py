from visitor import Visitor
from ast_type import AstType


class SelectionStatement:
    def __init__(self, position, expression, if_block, else_block=None):
        self.position = position
        self.expression = expression
        self.if_block = if_block
        self.else_block = else_block
        self.type = AstType.CONDITIONAL_STATEMENT

    def __repr__(self):
        return f"SelectionStatement(\
            {self.position}, {self.expression}, {self.if_block},\
                  {self.else_block})"

    def accept(self, visitor: Visitor):
        return visitor.visit_selection_statement(self)
