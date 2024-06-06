from src.visitor.visitor import Visitor
from src.ast_tree.node import Node


class StatementsBlock(Node):
    def __init__(self, position, statements) -> None:
        self.position = position
        self.statements = statements

    def __repr__(self):
        return f"StatementsBlock({self.position}, {self.statements})"

    def __eq__(self, other):
        return (isinstance(other, StatementsBlock) and
                other.statements == self.statements)

    def accept(self, visitor: Visitor):
        visitor.visit_statements_block(self)
