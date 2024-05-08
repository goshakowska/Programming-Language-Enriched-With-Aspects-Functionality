class UnexpectedTokenTypeError(Exception):
    def __init__(self, position, required_types, received_type) -> None:
        self.position = position
        self.required_types = required_types
        self.received_type = received_type

    def __str__(self):
        return f"ERR! [{self.position}]: Unexpected type, required {self.required_types}, got {self.received_type} instead."


class FunctionRedefinitionError(Exception):
    def __init__(self, position, function_name) -> None:
        self.position = position
        self.function_name = function_name

    def __str__(self):
        return f"ERR! [{self.position}]: Function {self.function_name} already defined."


class StatementRedefinitionError(Exception):
    def __init__(self, position, statement_name) -> None:
        self.position = position
        self.statement_name = statement_name

    def __str__(self):
        return f"ERR! [{self.position}]: Statement {self.statement_name} already defined."


class AspectRedefinitionError(Exception):
    def __init__(self, position, aspect_name) -> None:
        self.position = position
        self.aspect_name = aspect_name

    def __str__(self):
        return f"ERR! [{self.position}]: Aspect {self.aspect_name} already defined."


class MissingOpeningParenthesisError(Exception):
    def __init__(self, position, statement_name) -> None:
        self.position = position
        self.statement_name = statement_name
        # self.token = token

    def __str__(self):
        return f"ERR! [{self.position}]: Missing opening parenthesis in statement {self.statement}."


class MissingClosingParenthesisError(Exception):
    def __init__(self, position, statement_name) -> None:
        self.position = position
        self.statement_name = statement_name
        # self.token = token

    def __str__(self):
        return f"ERR! [{self.position}]: Missing closing parenthesis in statement {self.statement} declaration."


class MissingSemicolonError(Exception):
    def __init__(self, position) -> None:
        self.position = position
        # self.token = token

    def __str__(self):
        return f"ERR! [{self.position}]: Missing semicolon."


class NoReturnTypeError(Exception):
    def __init__(self, position, function_name) -> None:
        self.position = position
        self.function_name = function_name

    def __str__(self):
        return f"ERR! [{self.position}]: No return type provided in function definition {self.function_name}."


class NoExecutionBlockError(Exception):
    def __init__(self, position, statement_name) -> None:
        self.position = position
        self.statement_name = statement_name

    def __str__(self):
        return f"ERR! [{self.position}]: No execution block provided in '{self.statement_name}' statement."


class NoConditionBlockError(Exception):
    def __init__(self, position, statement_name) -> None:
        self.position = position
        self.statement_name = statement_name

    def __str__(self):
        return f"ERR! [{self.position}]: No condition block provided in '{self.statement_name}' statement."


class NoAssignmentExpressionError(Exception):
    def __init__(self, position) -> None:
        self.position = position

    def __str__(self):
        return f"ERR! [{self.position}]: No assignment expression provided in assignment statement."


class NoIndexExpressionError(Exception):
    def __init__(self, position, name) -> None:
        self.position = position
        self.name = name

    def __str__(self):
        return f"ERR! [{self.position}]: No index expression provided in indexed expression {self.name}."
    

class NoIteratorError(Exception):
    def __init__(self, position) -> None:
        self.position = position

    def __str__(self):
        return f"ERR! [{self.position}]: No iterator provided in 'for' statement."
    

class NoIterableError(Exception):
    def __init__(self, position, iterator) -> None:
        self.position = position
        self.iterator = iterator

    def __str__(self):
        return f"ERR! [{self.position}]: No iterable provided for iterator {self.iterator} in 'for' statement."
    

class InvalidExpressionError(Exception):
    def __init__(self, position) -> None:
        self.position = position

    def __str__(self):
        return f"ERR! [{self.position}]: Invalid expression."


# TODO: ma podać możliwe a co dostał w zamian
class InvalidAspectDefinitionSyntaxError(Exception):
    def __init__(self, position, aspect_name, missing_key_word) -> None:
        self.position = position
        self.aspect_name = aspect_name
        self.missing_key_word = missing_key_word
        # self.token = token

    def __str__(self):
        return f"ERR! [{self.position}]: Aspect {self.aspect_name} missing {self.missing_key_word} keyword."


class InvalidAspectTargetError(Exception):
    def __init__(self, position, aspect_name, expected_aspect_targets) -> None:
        self.position = position
        self.aspect_name = aspect_name
        self.expected_aspect_targets = expected_aspect_targets
        # self.token = token

    def __str__(self):
        return f"ERR! [{self.position}]: Aspect {self.aspect_name} has target not in expected aspect targets {self.expected_aspect_targets}."


class InvalidAspectEventError(Exception):
    def __init__(self, position, aspect_name, expected_aspect_events) -> None:
        self.position = position
        self.aspect_name = aspect_name
        self.expected_aspect_events = expected_aspect_events
        # self.token = token

    def __str__(self):
        return f"ERR! [{self.position}]: Aspect {self.aspect_name} has event not in expected aspect events {self.expected_aspect_events}."


# TODO: refactor
class UncompleteOrExpressionError(Exception):
    def __init__(self, position, left_term) -> None:
        self.position = position
        self.left_term = left_term

    def __str__(self):
        return f"ERR! [{self.position}]: Missing right term in or expression that starts with {self.left_term}."
    

# TODO: refactor
class UncompleteAndExpressionError(Exception):
    def __init__(self, position, left_term) -> None:
        self.position = position
        self.left_term = left_term

    def __str__(self):
        return f"ERR! [{self.position}]: Missing right term in and expression that starts with {self.left_term}."


# TODO: refactor
class UncompleteRelationExpressionError(Exception):
    def __init__(self, position, left_term) -> None:
        self.position = position
        self.left_term = left_term

    def __str__(self):
        return f"ERR! [{self.position}]: Missing right term in relation expression that starts with {self.left_term}."


# TODO: refactor
class UncompleteAdditiveExpressionError(Exception):
    def __init__(self, position, left_term) -> None:
        self.position = position
        self.left_term = left_term

    def __str__(self):
        return f"ERR! [{self.position}]: Missing right term in additive expression that starts with {self.left_term}."


# TODO: refactor
class UncompleteMultiplicativeExpressionError(Exception):
    def __init__(self, position, left_term) -> None:
        self.position = position
        self.left_term = left_term

    def __str__(self):
        return f"ERR! [{self.position}]: Missing right term in multiplicative expression that starts with {self.left_term}."


# TODO: refactor
class UncompleteUnaryExpressionError(Exception):
    def __init__(self, position) -> None:
        self.position = position

    def __str__(self):
        return f"ERR! [{self.position}]: Missing unary term."


# TODO: refactor
class UncompleteCastedExpressionError(Exception):
    def __init__(self, position, term) -> None:
        self.position = position
        self.term = term

    def __str__(self):
        return f"ERR! [{self.position}]: Missing type conversion for term in casted expression: {self.term}."


class InvalidParameterError(Exception):
    def __init__(self, position, parameter_before) -> None:
        self.position = position
        self.previous_parameter = parameter_before

    def __str__(self):
        return f"ERR! [{self.position}]: Invalid parameter occurred after parameter: {self.previous_parameter}."

class InvalidArgumentError(Exception):
    def __init__(self, position, argument_before) -> None:
        self.position = position
        self.previous_argument = argument_before

    def __str__(self):
        return f"ERR! [{self.position}]: Invalid argument occurred after argument: {self.previous_argument}."


class InvalidObjectAccessSyntaxError(Exception):
    def __init__(self, position, accessed_object) -> None:
        self.position = position
        self.accessed_object = accessed_object

    def __str__(self):
        return f"ERR! [{self.position}]: Invalid object access syntax in: {self.accessed_object}."
