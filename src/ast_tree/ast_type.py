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

    BOOL_TYPE = auto()
    FLOAT_TYPE = auto()
    INT_TYPE = auto()
    STR_TYPE = auto()

    BOOL = auto()
    FLOAT = auto()
    INT = auto()
    STR = auto()

    FUNCTION = auto()

    ASPECT = auto()
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
