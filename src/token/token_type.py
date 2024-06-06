from enum import Enum, auto


class TokenType(Enum):
    ETX = auto()  # end of text
    IDENTIFIER = auto()  #

    PLUS = auto()  # +
    MINUS = auto()  # -
    MULTIPLICATION = auto()  # *
    DIVISION = auto()  # /

    OPENING_SQUARE_BRACKET = auto()  # [
    CLOSING_SQUARE_BRACKET = auto()  # ]
    OPENING_BRACKET = auto()  # (
    CLOSING_BRACKET = auto()  # )
    OPENING_CURLY_BRACKET = auto()  # {
    CLOSING_CURLY_BRACKET = auto()  # }
    SEMICOLON = auto()  # ;
    COLON = auto()  # :

    ASSIGN = auto()  # =
    NOT = auto()  # !
    LESS_THAN_OPERATOR = auto()  # <
    GREATER_THAN_OPERATOR = auto()  # >

    EQUAL = auto()  # ==
    NOT_EQUAL = auto()  # !=
    LESS_THAN_OR_EQUAL_OPERATOR = auto()  # <=
    GREATER_THAN_OR_EQUAL_OPERATOR = auto()  # >=

    DOT = auto()  # .
    COMMA = auto()  # ,
    AND = auto()  # &&
    OR = auto()  # ||

    IF = auto()  # if
    ELSE = auto()  # else
    WHILE = auto()  # while
    FOR = auto()  # for
    IN = auto()  # in

    TYPE_BOOL = auto()  # bool
    BOOL = auto()  # true, false
    TYPE_INT = auto()  # int
    INT = auto()  # 1
    TYPE_FLOAT = auto()  # float
    FLOAT = auto()  # 1.1
    TYPE_STR = auto()  # str
    STR = auto()  # "my str"
    NULL = auto()  # null, return type of function
    COMMENT = auto()

    TYPE_FUNCTION = auto()  # func  # FUNCTION TODO
    RETURN = auto()  # return

    TYPE_ASPECT = auto()  # aspect  # ASPECT TODO
    ASPECT_ON_START = auto()  # start
    ASPECT_ON_END = auto()  # end
    ASPECT_ON_CALL = auto()  # call
    ON = auto()  # on
    LIKE = auto()  # like
    AS = auto()  # type conversion function
