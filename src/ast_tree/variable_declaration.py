from visitor import Visitor


class VariableDeclaration:  # position, ast_type, name
    def __init__(self, position, name, type) -> None:
        self.position = position
        self.name = name
        self.type = type

    def __repr__(self):
        return f"VariableDeclaration({self.position}, {self.name},\
              {self.type})"

    def __eq__(self, other):
        return (isinstance(other, VariableDeclaration) and
                other.name == self.name)

    def accept(self, visitor: Visitor):
        return visitor.visit_variable_declaration(self)
