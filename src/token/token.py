from src.token.token_type import TokenType


class Token:
    def __init__(self, token_type=TokenType.IDENTIFIER, value=None, line=None, column=None):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def get_column(self):
        return self.column

    def get_line(self):
        return self.line

    def get_position(self):
        return self.line, self.column

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def __repr__(self):
        return f"Token of type: {self.type}, with value: {self.value}, at line: {self.value}, column: {self.line}."

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value and self.line == other.line and self.column == other.column