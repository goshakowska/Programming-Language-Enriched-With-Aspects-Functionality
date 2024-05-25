from enum import Enum, auto


class AstType(Enum):
    PROGRAM = auto()
    IDENITIFIER = auto()

    PLUS = auto()
    MINUS = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()

    LESS_THAN = auto()
    GREATER_THAN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN_OR_EQUAL = auto()
    GREATER_THAN_OR_EQUAL = auto()

    OR = auto()
    AND = auto()

    TYPE_BOOL = auto()
    TYPE_FLOAT = auto()
    TYPE_INT = auto()
    TYPE_STR = auto()

    BOOL = auto()
    FLOAT = auto()
    INT = auto()
    STR = auto()

    TYPE_FUNCTION = auto()

    TYPE_ASPECT = auto()
    ASPECT_ON_START = auto()  # start
    ASPECT_ON_END = auto()  # end
    ASPECT_ON_CALL = auto()  # call

    CONDITIONAL_STATEMENT = auto()
    ASSIGNMENT_STATEMENT = auto()
    OBJECT_ACCESS = auto()
    INDEXED_ITEM = auto()
    FUNCTION_CALL = auto()
    FOR_STATEMENT = auto()
    WHILE_STATEMENT = auto()
    RETURN_STATEMENT = auto()
    UNARY_TERM = auto()
    CASTED_TERM = auto()
