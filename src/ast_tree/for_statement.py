from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class ForStatement(Node):
    def __init__(self, position, iterator, iterable, execution_block) -> None:
        self.position = position
        self.iterator = iterator
        self.iterable = iterable
        self.execution_block = execution_block
        self.type = AstType.FOR_STATEMENT

    def __repr__(self):
        return f"ForStatement({self.position}, {self.iterator},\
              {self.iterable}, {self.execution_block})"

    def __eq__(self, other):
        return (isinstance(other, ForStatement) and
                other.iterator == self.iterator and
                other.iterable == self.iterable and
                other.execution_block == self.execution_block)

    def accept(self, visitor: Visitor):
        return visitor.visit_for_statement(self)
