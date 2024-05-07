from visitor import Visitor


class ForStatement:
    def __init__(self, position, iterator, iterable, execution_block) -> None:
        self.position = position
        self.iterator = iterator
        self.iterable = iterable
        self.execution_block = execution_block

    def __repr__(self):
        return f"ForStatement({self.iterator}, {self.iterable}, {self.execution_block})"

    def accept(self, visitor: Visitor):
        return visitor.visit_while_statement(self)
