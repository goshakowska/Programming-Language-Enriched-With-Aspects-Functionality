from visitor import Visitor


class AssignmentStatement:
    def __init__(self, position, declaration, expression) -> None:
        self.position = position
        self.declaration = declaration
        self.expression = expression

    def __repr__(self):
        return f"AssignmentStatement({self.declaration}, {self.expression})"

    def __eq__(self, other):
        return (isinstance(other, AssignmentStatement) and
                other.declaration == self.declaration and
                other.expression == self.expression)

    def accept(self, visitor: Visitor):
        return visitor.visit_assignment_statement(self)
