class CheckerVisitor:
    def __init__(self) -> None:
        pass

    def visit_and_expression(self, and_expression, other_and_expression) -> bool:
        return and_expression is other_and_expression
    
    def visit_aspect_definition(self, aspect_definition, other_aspect_definition) -> bool:
        return aspect_definition is other_aspect_definition

    def visit_assignment_statement(self, assignment_statement, other_assignment_statement) -> bool:
        return assignment_statement is other_assignment_statement

    def visit_bool_literal(self, bool_literal, other_bool_literal) -> bool:
        return bool_literal is other_bool_literal


    def visit_program(self, program, other_program) -> bool:
        return program is other_program
