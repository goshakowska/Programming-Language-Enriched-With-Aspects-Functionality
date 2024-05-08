from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class WhileStatement:
    def __init__(self, position, condition, execution_block) -> None:
        self.position = position
        self.condition = condition
        self.execution_block = execution_block
        self.type = AstType.WHILE_STATEMENT

    def __repr__(self):
        return f"WhileStatement({self.position}, {self.condition},\
              {self.execution_block})"

    def __eq__(self, other):
        return (isinstance(other, WhileStatement) and
                other.condition == self.condition and
                other.execution_block == self.execution_block)

    def accept(self, visitor: Visitor):
        return visitor.visit_while_statement(self)
