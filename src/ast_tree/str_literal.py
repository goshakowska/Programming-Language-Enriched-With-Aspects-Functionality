from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType


class StrLiteral:
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term  # czy lepiej value?
        self.type = AstType.STR

    def __repr__(self):
        return f"Literal({self.position}, {self.term}, {self.type})"

    def accept(self, visitor: Visitor):
        return visitor.visit_str_literal(self)
