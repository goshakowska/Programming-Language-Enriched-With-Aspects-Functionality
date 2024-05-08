from visitor import Visitor


class AspectDefinition:
    def __init__(self, position, name, target, event, regular_expression):
        self.position = position
        self.name = name
        self.target = target
        self.event = event
        self.regular_expression = regular_expression

    def __repr__(self):
        return f"AspectDefinition({self.name}, {self.target}, {self.event}, {self.regular_expression})"

    def __eq__(self, other):
        return (isinstance(other, AspectDefinition) and
                other.name == self.name)

    def accept(self, visitor: Visitor):
        return visitor.visit_aspect_definition(self)

# aspect target, aspect trigger, aspect