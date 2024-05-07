from token.token import Token


class InvalidSyntaxError(Exception):
    def __init__(self, token: Token) -> None:
        # self.message = message
        self.line = token.get_line()
        self.column = token.get_column()
        self.value = token.get_value()

        def __str__(self):
            return f"ERR! [{self.line}: {self.column}]: {self.message}"