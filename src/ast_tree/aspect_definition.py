from src.visitor.visitor import Visitor
from src.ast_tree.ast_type import AstType
from src.ast_tree.node import Node


class AspectDefinition(Node):
    def __init__(self, position, name, target, event, regular_expression,
                 block):
        self.position = position
        self.name = name
        self.target = target
        self.event = event
        self.regular_expression = regular_expression
        self.block = block
        self.type = AstType.TYPE_ASPECT
        self.enabled = True

    def __repr__(self):
        return f"AspectDefinition({self.position}, {self.name}, {self.target},\
              {self.event}, {self.regular_expression}, {self.block})"

    def __eq__(self, other):
        return (isinstance(other, AspectDefinition) and
                other.name == self.name)

    def accept(self, visitor: Visitor):
        visitor.visit_aspect_definition(self)

    def __hash__(self) -> int:
        return hash(str(self))
