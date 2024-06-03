from src.visitor.visitor import Visitor
from src.ast_tree.node import Node
from src.ast_tree.ast_type import AstType


class PrintFunction(Node):
    def __init__(self, content_to_print) -> None:
        self.name = "print"
        self.arguments = content_to_print
        self.return_type = AstType.NULL

    def accept(self, visitor: Visitor):
        visitor.visit_print_function(self)


