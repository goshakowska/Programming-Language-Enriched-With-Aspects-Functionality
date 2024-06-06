from enum import Enum, auto


class AstType(Enum):

    TYPE_BOOL = auto()
    TYPE_FLOAT = auto()
    TYPE_INT = auto()
    TYPE_STR = auto()
    NULL = auto()

    BOOL = auto()
    FLOAT = auto()
    INT = auto()
    STR = auto()

    TYPE_FUNCTION = auto()

    TYPE_ASPECT = auto()
    ASPECT_ON_START = auto()  # start
    ASPECT_ON_END = auto()  # end
    ASPECT_ON_CALL = auto()  # call
