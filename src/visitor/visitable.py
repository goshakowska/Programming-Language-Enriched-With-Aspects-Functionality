import typing
if typing.TYPE_CHECKING:
    from src.visitor.interpreter import Interpreter
from src.ast_tree.node import Node
from src.ast_tree.ast_type import AstType


class PrintFunction(Node):
    def __init__(self, params=None) -> None:
        self.arguments = params
        self.return_type = AstType.NULL

    def set_arguments(self, params):
        self.arguments = params

    def accept(self, visitor: "Interpreter"):
        visitor.visit_print_function(self)
