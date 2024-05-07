from visitor import Visitor


class WhileStatement:
    def __init__(self, position, condition, execution_block) -> None:
        self.position = position
        self.condition = condition
        self.execution_block = execution_block

    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.execution_block})"

    def __eq__(self, other):
        pass

    def accept(self, visitor: Visitor):
        return visitor.visit_while_statement(self)
