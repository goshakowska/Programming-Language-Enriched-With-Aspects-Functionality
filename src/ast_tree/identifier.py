from visitor import Visitor
from ast_type import AstType


class Identifier:
    def __init__(self, position, name) -> None:
        self.position = position
        self.name = name
        self.type = AstType.IDENITIFIER

    def __repr__(self):
        return f"Identifier({self.position}, {self.name})"

    def __eq__(self, other):
        return (isinstance(other, Identifier) and
                other.name == self.name)

    def accept(self, visitor: Visitor):
        return visitor.visit_identifier(self)
