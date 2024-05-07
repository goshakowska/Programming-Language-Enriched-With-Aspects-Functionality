class Item:
    def __init__(self, position, identifier_or_call, index=None) -> None:
        self.position = position
        self.identifier_or_call = identifier_or_call
        self.index = index

    def accept(self, visitor: Visitor):
        return visitor.visit_item(self)

    def __repr__(self):
        return f"Item({self.identifier_or_call}, {self.index})"

    def __eq__(self, other):
        return self.identifier_or_call == other.identifier_or_call
    