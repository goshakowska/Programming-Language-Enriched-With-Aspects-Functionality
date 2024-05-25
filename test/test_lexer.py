import io
from src.lexer.lexer import Lexer
from src.source.source import Source
from src.token.token_type import TokenType
# from src.token.token import Token


def create_lexer_with_given_source(string):
    return Lexer(Source(io.StringIO(string)))


def test_lexer_with_single_token():
    lexer = create_lexer_with_given_source("myString")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IDENTIFIER
    assert token.get_value() == "myString"
    assert token.get_position() == (1, 1)


def test_lexer_with_single_token_with_space():
    lexer = create_lexer_with_given_source(" myString")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IDENTIFIER
    assert token.get_value() == "myString"
    assert token.get_position() == (1, 2)


def test_lexer_build_multiple_tokens_of_different_type():
    lexer = create_lexer_with_given_source("int myInt = 6")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_INT
    assert token.get_value() is None
    assert token.get_position() == (1, 1)
  
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IDENTIFIER
    assert token.get_value() == "myInt"
    assert token.get_position() == (1, 5)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ASSIGN
    assert token.get_value() is None
    assert token.get_position() == (1, 11)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.INT
    assert token.get_value() == 6
    assert token.get_position() == (1, 13)


def test_lexer_build_multiple_tokens_of_different_type_2():
    lexer = create_lexer_with_given_source(" 6 + 4 ")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.INT
    assert token.get_value() == 6
    assert token.get_position() == (1, 2)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.PLUS
    assert token.get_value() is None
    assert token.get_position() == (1, 4)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.INT
    assert token.get_value() == 4
    assert token.get_position() == (1, 6)


def test_lexer_with_multiple_tokens_of_different_type_with_spaces():
    lexer = create_lexer_with_given_source('str        myString         "Ala ma kota."')
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_STR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IDENTIFIER
    assert token.get_value() == 'myString'
    assert token.get_position() == (1, 12)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.STR
    assert token.get_value() == "Ala ma kota."
    assert token.get_position() == (1, 29)


def test_lexer_build_token_type_etx():
    lexer = create_lexer_with_given_source("")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ETX
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_identifier():
    lexer = create_lexer_with_given_source("myOtherString")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IDENTIFIER
    assert token.get_value() == "myOtherString"
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_plus():
    lexer = create_lexer_with_given_source("+")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.PLUS
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_minus():
    lexer = create_lexer_with_given_source("-")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.MINUS
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_multiplication():
    lexer = create_lexer_with_given_source("*")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.MULTIPLICATION
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_division():
    lexer = create_lexer_with_given_source("/")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.DIVISION
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_opening_square_bracket():
    lexer = create_lexer_with_given_source("[")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.OPENING_SQUARE_BRACKET
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_closing_square_bracket():
    lexer = create_lexer_with_given_source("]")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.CLOSING_SQUARE_BRACKET
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_opening_bracket():
    lexer = create_lexer_with_given_source("(")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.OPENING_BRACKET
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_closing_bracket():
    lexer = create_lexer_with_given_source(")")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.CLOSING_BRACKET
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_opening_curly_bracket():
    lexer = create_lexer_with_given_source("{")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.OPENING_CURLY_BRACKET
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_closing_curly_bracket():
    lexer = create_lexer_with_given_source("}")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.CLOSING_CURLY_BRACKET
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_semicolon():
    lexer = create_lexer_with_given_source(";")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.SEMICOLON
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_colon():
    lexer = create_lexer_with_given_source(":")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.COLON
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_assign():
    lexer = create_lexer_with_given_source("=")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ASSIGN
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_ambitious_assign():
    lexer = create_lexer_with_given_source("<==")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.LESS_THAN_OR_EQUAL_OPERATOR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ASSIGN
    assert token.get_value() is None
    assert token.get_position() == (1, 3)

    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ETX
    assert token.get_value() is None
    assert token.get_position() == (1, 4)


def test_lexer_build_token_type_not():
    lexer = create_lexer_with_given_source("!")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.NOT
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_less_than_operator():
    lexer = create_lexer_with_given_source("<")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.LESS_THAN_OPERATOR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_greater_than_operator():
    lexer = create_lexer_with_given_source(">")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.GREATER_THAN_OPERATOR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_equal():
    lexer = create_lexer_with_given_source("==")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.EQUAL
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_not_equal():
    lexer = create_lexer_with_given_source("!=")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.NOT_EQUAL
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_less_than_or_equal_operator():
    lexer = create_lexer_with_given_source("<=")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.LESS_THAN_OR_EQUAL_OPERATOR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_greater_than_or_equal_operator():
    lexer = create_lexer_with_given_source(">=")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.GREATER_THAN_OR_EQUAL_OPERATOR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_dot():
    lexer = create_lexer_with_given_source(".")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.DOT
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_comma():
    lexer = create_lexer_with_given_source(",")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.COMMA
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_and():
    lexer = create_lexer_with_given_source("&&")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.AND
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


# def test_lexer_build_token_type_and_with_users_typo():
#     lexer = create_lexer_with_given_source("&7")
#     token = lexer.try_to_build_next_token()
#     assert token.get_type() == TokenType.AND
#     assert token.get_value() is None
#     assert token.get_position() == (1, 1)


def test_lexer_build_token_type_or():
    lexer = create_lexer_with_given_source("||")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.OR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


# def test_lexer_build_token_type_or_with_users_typo():
#     lexer = create_lexer_with_given_source("|'")
#     token = lexer.try_to_build_next_token()
#     assert token.get_type() == TokenType.OR
#     assert token.get_value() is None
#     assert token.get_position() == (1, 1)


def test_lexer_build_token_type_if():
    lexer = create_lexer_with_given_source("if")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IF
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_else():
    lexer = create_lexer_with_given_source("else")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ELSE
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_while():
    lexer = create_lexer_with_given_source("while")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.WHILE
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_for():
    lexer = create_lexer_with_given_source("for")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.FOR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_in():
    lexer = create_lexer_with_given_source("in")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.IN
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_bool_type():
    lexer = create_lexer_with_given_source("bool")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_BOOL
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_int_type():
    lexer = create_lexer_with_given_source("int")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_INT
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_int():
    lexer = create_lexer_with_given_source("6")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.INT
    assert token.get_value() == 6
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_float_type():
    lexer = create_lexer_with_given_source("float")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_FLOAT
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_float():
    lexer = create_lexer_with_given_source("6.5")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.FLOAT
    assert token.get_value() == 6.5
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_long_float():
    lexer = create_lexer_with_given_source("666666.5")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.FLOAT
    assert token.get_value() == 666666.5
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_long_float_():
    lexer = create_lexer_with_given_source("666666.54321")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.FLOAT
    assert token.get_value() == 666666.54321
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_str_type():
    lexer = create_lexer_with_given_source("str")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_STR
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_str():
    lexer = create_lexer_with_given_source('"str"')
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.STR
    assert token.get_value() == 'str'
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_str_escaped_escape_char():
    lexer = create_lexer_with_given_source('"escaped\\ str"')  # FIXME!
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.STR
    assert token.get_value() == "escaped\\ str"
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_str_escaped_n_char():
    lexer = create_lexer_with_given_source('"escaped\n str"')
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.STR
    assert token.get_value() == "escaped\n str"
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_str_escaped_t_char():
    lexer = create_lexer_with_given_source('"escaped\t str"')
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.STR
    assert token.get_value() == "escaped\t str"
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_str_escaped_apostrophe_char():
    lexer = create_lexer_with_given_source('"escaped\' str"')
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.STR
    assert token.get_value() == "escaped\' str"
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_null():
    lexer = create_lexer_with_given_source("null")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.NULL
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_comment():
    lexer = create_lexer_with_given_source("#ab\n kolejne")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.COMMENT
    assert token.get_value() == "#ab"
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_function_type():
    lexer = create_lexer_with_given_source("func")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_FUNCTION
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_return():
    lexer = create_lexer_with_given_source("return")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.RETURN
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_aspect_type():
    lexer = create_lexer_with_given_source("aspect")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.TYPE_ASPECT
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_aspect_on_start():
    lexer = create_lexer_with_given_source("start")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ASPECT_ON_START
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_aspect_on_end():
    lexer = create_lexer_with_given_source("end")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ASPECT_ON_END
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_aspect_on_call():
    lexer = create_lexer_with_given_source("call")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ASPECT_ON_CALL
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_on():
    lexer = create_lexer_with_given_source("on")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.ON
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_like():
    lexer = create_lexer_with_given_source("like")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.LIKE
    assert token.get_value() is None
    assert token.get_position() == (1, 1)


def test_lexer_build_token_type_as():
    lexer = create_lexer_with_given_source("as")
    token = lexer.try_to_build_next_token()
    assert token.get_type() == TokenType.AS
    assert token.get_value() is None
    assert token.get_position() == (1, 1)
