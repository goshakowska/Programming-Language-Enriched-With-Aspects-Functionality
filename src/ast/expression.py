from visitor import Visitor


class Expression:
    def __init__(self, position, left_term, right_term, operation=None) -> None:
        self.left_term = left_term
        self.operation = operation
        self.right_term = right_term

    def __eq__(self, other):
        return self.left_term == other.left_term and \
               self.operation == other.operation and \
               self.right_term == other.right_term

    def __repr__(self):
        return f"Expression({self.left_term}, {self.operation}, {self.right_term})"

    def accept(self, visitor: Visitor):
        return visitor.visit_expression(self)
