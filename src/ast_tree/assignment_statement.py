from src.visitor.visitor import Visitor
from src.visitor.checker_visitor import CheckerVisitor
from src.ast_tree.ast_type import AstType


class AssignmentStatement:
    def __init__(self, position, expression, object_access) -> None:
        self.position = position
        self.object_access = object_access
        self.expression = expression
        self.type = AstType.ASSIGNMENT_STATEMENT

    def __repr__(self):
        return f"AssignmentStatement({self.position}, {self.object_access},\
              {self.expression})"

    def __eq__(self, other):
        return (isinstance(other, AssignmentStatement) and
                other.object_access == self.object_access and
                other.expression == self.expression)

    def accept(self, visitor: Visitor):
        return visitor.visit_assignment_statement(self)

    def accept_checker(self, visitor: CheckerVisitor):
        return visitor.visit_assignment_statement(self)
