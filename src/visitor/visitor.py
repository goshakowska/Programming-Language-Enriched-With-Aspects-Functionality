class Visitor:
    def __init__(self) -> None:
        pass

    def visit_function_definition(self):
        pass

    def visit_aspect_definition(self):
        pass

    def visit_for_statement(self):
        pass

    def visit_while_statement(self):
        pass

    def visit_selection_statement(self):
        pass


# polimorfizm - oddzielamy logikę - wizytator, który printuje na ekran
# wizytator, który printuje do pliku
# na etapie interpretacji