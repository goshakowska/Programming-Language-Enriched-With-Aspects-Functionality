from visitor import Visitor


class SelectionStatement:
    pass

    def accept(self, visitor: Visitor):
        return visitor.visit_selection_statement(self)
