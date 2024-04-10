from src.token.token import Token
from src.source.source import Source
from src.token.token_type import TokenType
from src.lexer.lexer_error import ContinueLexerError, TerminateLexerError


class Lexer:
    def __init__(self, source: Source, max_string_length=10000):

        self.source = source
        self.token = Token()
        self.max_string_length = max_string_length
        self._character = source.get_character()
        self._token_line = 0
        self._token_column = 0

        self.key_words = {

            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "for": TokenType.FOR,
            "in": TokenType.IN,

            "bool": TokenType.BOOL_TYPE,
            "int": TokenType.INT_TYPE,
            "float": TokenType.FLOAT_TYPE,
            "str": TokenType.STR_TYPE,
            "null": TokenType.NULL,

            "func": TokenType.FUNCTION_TYPE,
            "return": TokenType.RETURN,

            "aspect": TokenType.ASPECT_TYPE,
            "start": TokenType.ASPECT_ON_START,
            "end": TokenType.ASPECT_ON_END,
            "call": TokenType.ASPECT_ON_CALL,
            "on": TokenType.ON,
            "like": TokenType.LIKE,

            "as": TokenType.AS,

        }

        self.one_char_symbols = {

            "[": TokenType.OPENING_SQUARE_BRACKET,
            "]": TokenType.CLOSING_SQUARE_BRACKET,
            "(": TokenType.OPENING_BRACKET,
            ")": TokenType.CLOSING_BRACKET,
            "{": TokenType.OPENING_CURLY_BRACKET,
            "}": TokenType.CLOSING_CURLY_BRACKET,
            ";": TokenType.SEMICOLON,
            ":": TokenType.COLON,
            ".": TokenType.DOT,
            ",": TokenType.COMMA,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.MULTIPLICATION,
            "/": TokenType.DIVISION,

        }

        self.extendable_one_char_symbols = {

            "!": lambda: self.try_build_two_sign_operator("=", TokenType.NOT,
                                                          TokenType.NOT_EQUAL),
            "=": lambda: self.try_build_two_sign_operator("=", TokenType.ASSIGN,
                                                          TokenType.EQUAL),
            "<": lambda: self.try_build_two_sign_operator("=", TokenType.LESS_THAN_OPERATOR,
                                                          TokenType.LESS_THAN_OR_EQUAL_OPERATOR),
            ">": lambda: self.try_build_two_sign_operator("=",
                                                          TokenType.GREATER_THAN_OPERATOR,
                                                          TokenType.GREATER_THAN_OR_EQUAL_OPERATOR),
            "&": lambda: self.try_build_and_or_operator("&",
                                                        TokenType.AND,
                                                        "wrong syntax: symbol \
                                                         matched and replaced \
                                                            to && operator"),
            "|": lambda: self.try_build_and_or_operator("|",
                                                        TokenType.OR,
                                                        "wrong syntax: \
                                                         symbol matched \
                                                         and replaced to \
                                                         || operator"),

        }

    def _next_char(self):

        self.source.next_character()
        self._character = self.source.get_character()

    def get_token(self):

        return self.token

    def omit_whitespaces(self):

        while self._character.isspace():
            self._next_char()

    def build_etx(self):

        if self.source.get_character() == "":
            return Token(TokenType.ETX, line=self._token_line,
                         column=self._token_column)

    def handle_escape_char(self):
        if self._character != "\\":
            return self._character
        self._next_char()
        escaped_char_buffer = [self._character]
        self._next_char()
        if self._character in ("n", "t", "\"", "\\"):
            escaped_char_buffer.append(self._character)
            return escaped_char_buffer
        else:
            raise TerminateLexerError("wrong syntax: unexpected\
                                       symbol in string body",
                                      self.source.get_line(),
                                      self.source.get_column())

    def build_string(self):

        if self._character != '"':
            return None
        string_to_build = []
        self._next_char()
        while self._character != '"':
            if self._character == "":
                raise TerminateLexerError("wrong syntax: unfinished string",
                                          self._token_line, self._token_column)
            if len(string_to_build) == self.max_string_length:
                raise TerminateLexerError("exceeded max string length",
                                          self._token_line,
                                          self._token_column)
            string_to_build.append(self.handle_escape_char())
            self._next_char()
        string_to_build = "".join(string_to_build)
        return Token(TokenType.STR, value=string_to_build,
                     line=self._token_line, column=self._token_column)

    def build_one_char_token(self):

        if character_type := self.one_char_symbols.get(self._character):
            return Token(character_type, line=self._token_line,
                         column=self._token_column)
        return None

    def try_build_two_sign_operator(self, second_char, token_type_single_sign,
                                    token_type_multi_sign):

        self._next_char()
        if self._character == second_char:
            self._next_char()
            return token_type_multi_sign
        else:
            return token_type_single_sign

    def try_build_and_or_operator(self, second_char,
                                  token_type,
                                  error_message):

        self._next_char()
        if self._character == second_char:
            self._next_char()
            return token_type
        else:
            self._report_error(ContinueLexerError(error_message,
                                                  self._token_line,
                                                  self._token_column))
            return token_type

    def build_extendable_tokens(self):

        if fun := self.extendable_one_char_symbols.get(self._character):
            return Token(fun(), line=self._token_line,
                         column=self._token_column)
        return None

    def build_keywords_or_identifier(self):

        buffer = []
        while self._character.isalpha():
            if len(buffer) == self.max_string_length:
                TerminateLexerError("buffer overflow: \
                                    exceeded number of chars",
                                    self._token_line, self._token_column)
            buffer.append(self._character)
            self._next_char()
        ret_buffer = "".join(buffer)
        if ret_buffer == "":
            return None
        elif token_type := self.key_words.get(ret_buffer):
            return Token(token_type, line=self._token_line,
                         column=self._token_column)
        else:
            return Token(TokenType.IDENTIFIER, value=ret_buffer,
                         line=self._token_line, column=self._token_column)

    def build_number(self):

        while self._character.isdecimal():
            is_float = False
            number_buffer = [self._character]
            self._next_char()
            if self._character == ".":
                is_float = True
                number_buffer.append(self._character)
                self._next_char()
            while self._character.isdecimal():
                number_buffer.append(self._character)
                self._next_char()
            number_buffer = "".join(number_buffer)
            if is_float:
                return Token(TokenType.FLOAT, value=number_buffer,
                             line=self._token_line, column=self._token_column)
            else:
                return Token(TokenType.INT, value=number_buffer,
                             line=self._token_line, column=self._token_column)

        else:
            return None

    def build_comment(self):

        if self._character == "#":
            comment_buffer = [self._character]
            self._next_char()
            while self._character != "\n" and self._character != "":
                comment_buffer.append(self._character)
                self._next_char()
            self._next_char()
            comment_buffer = "".join(comment_buffer)
            return Token(TokenType.COMMENT, value=comment_buffer,
                         line=self._token_line, column=self._token_column)
        else:
            return None

    def try_to_build_next_token(self):
        self.omit_whitespaces()
        self._token_line, self._token_column = self.source.get_position()
        token = self.build_comment()\
            or self.build_etx()\
            or self.build_number()\
            or self.build_string()\
            or self.build_one_char_token()\
            or self.build_extendable_tokens()\
            or self.build_keywords_or_identifier()
        # nie podmieniam tokena lekserowego - trzeba dodać self.token = token
        if token:
            self.token = token
            return token
        raise TerminateLexerError("unidentified token", self._token_line,
                                  self._token_column)
