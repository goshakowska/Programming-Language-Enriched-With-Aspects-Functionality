class LexerError:
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"ERR! [{self.line}: {self.column}]: {self.message}"


class TerminateLexerError(LexerError, Exception):
    pass


class ContinueLexerError(LexerError):
    pass
