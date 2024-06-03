class AdditionExpressionError(Exception):
    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Addition expression not supported for: {self.left_term} + {self.right_term}."


class SubtractionExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Subtraction expression not supported for: {self.left_term} - {self.right_term}."


class DivisionExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Division expression not supported for: {self.left_term} / {self.right_term}."


class MultiplicationExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Multiplication expression not supported for: {self.left_term} * {self.right_term}."


class GreaterThanExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Greater than expression not supported for: {self.left_term} > {self.right_term}."


class GreaterThanOrEqualExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Greater than or equal expression not supported for: {self.left_term} >= {self.right_term}."


class LessThanExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Less than expression not supported for: {self.left_term} < {self.right_term}."


class LessThanOrEqualExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Less than or equal expression not supported for: {self.left_term} <= {self.right_term}."


class OrExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: Or expression not supported for: {self.left_term} or {self.right_term}. Expected boolean value."


class AndExpressionError(Exception):

    def __init__(self, position, left_term, right_term) -> None:
        self.position = position
        self.left_term = left_term
        self.right_term = right_term

    def __str__(self):
        return f"ERR! [{self.position}]: And expression not supported for: {self.left_term} or {self.right_term}. Expected boolean value."


class NegatedTermError(Exception):

    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term

    def __str__(self):
        return f"ERR! [{self.position}]: In {self.term}. Negation is supported for: float, int, bool."


class CastingTypeError(Exception):

    def __init__(self, position, term, previous_type, casted_type) -> None:
        self.position = position
        self.term = term
        self.previous_type = previous_type
        self.casted_type = casted_type

    def __str__(self):
        return f"ERR! [{self.position}]: In {self.term}. Casting from {self.previous_type} to {self.casted_type} is not supported."


class EmbeddedFunctionOverrideError(Exception):

    def __init__(self, name) -> None:
        self.name = name

    def __str__(self):
        return f"ERR! [-]: Embedded function override: {self.name}."


class FunctionNotFoundError(Exception):

    def __init__(self, name) -> None:
        self.name = name

    def __str__(self):
        return f"ERR! [-]: Function with the name: {self.name} not found in the program functions' declarations."


class WrongNumberOfArgumentsError(Exception):

    def __init__(self, position, name, expected, got) -> None:
        self.position = position
        self.function_name = name
        self.expected_number = expected
        self.got_number = got

    def __str__(self):
        return f"ERR! [{self.position}]: In function {self.function_name}: expected {self.expected_number} number of arguments, got {self.got_number}."


class WrongArgumentTypeError(Exception):

    def __init__(self, position, name, argument_name, expected, got) -> None:
        self.position = position
        self.function_name = name
        self.argument_name = argument_name
        self.expected_type = expected
        self.got_type = got

    def __str__(self):
        return f"ERR! [{self.position}]: In function {self.function_name} in argument {self.argument_name}: Expected {self.expected_type} type, got {self.got_type}."


class ReturnOutsideFunctionCallError(Exception):

    def __init__(self, position) -> None:
        self.position = position

    def __str__(self):
        return f"ERR! [{self.position}]: Return statement in global scope and not in function call."


class TypeAssignmentError(Exception):

    def __init__(self, previous_value, current_value, previous_type, current_type) -> None:
        self.previous_value = previous_value
        self.current_value = current_value
        self.previous_type = previous_type
        self.current_type = current_type

    def __str__(self):
        return f"ERR! [-]: In assignment: from {self.previous_value} to {self.current_value}. Assignment from {self.previous_type} to {self.current_type} is not supported."


class DivisionByZeroError(Exception):

    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term

    def __str__(self):
        return f"ERR! [{self.position}]: {self.term} cannot be divided by zero."


class IncorrectReturnTypeError(Exception):

    def __init__(self, position, name, expected, got) -> None:
        self.position = position
        self.function_name = name
        self.expected_type = expected
        self.got_type = got.type  # got is an instance of Value

    def __str__(self):
        return f"ERR! [{self.position}]: In function {self.function_name}: Expected {self.expected_type} type, got {self.got_type} instead."


class UndefinedFunctionError(Exception):

    def __init__(self, position, name) -> None:
        self.position = position
        self.name = name

    def __str__(self):
        return f"ERR! [{self.position}]: Function {self.name} is not defined in the program."


class VariableNameConflictError(Exception):

    def __init__(self, name, value, existing_variable_value) -> None:
        self.name = name
        self.value = value
        self.existing_variable_value = existing_variable_value

    def __str__(self):
        return f"ERR! Cannot assign variable value {self.value} to variable {self.name}. Variable of a name {self.name} already exists with value {self.existing_variable_value}."


class ReturnInAspectDefinitionError(Exception): 

    def __init__(self, statement_position, aspect_name) -> None:
        self.position = statement_position
        self.name = aspect_name

    def __str__(self):
        return f"ERR! [{self.position}]: Return statements are not supported in Aspect type. Aspect: {self.name}."
