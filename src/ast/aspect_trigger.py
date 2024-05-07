from visitor import Visitor


class AspectTriger:
    def __init__(self, position, target, events) -> None:
        self.position = position
        self.target = target
        self.events = events

    def __repr__(self):
        return f"AspectTriger({self.target}, {self.events})"

    def accept(self, visitor: Visitor):
        return visitor.visit_aspect_trigger(self)
