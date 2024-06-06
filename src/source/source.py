class Source:
    def __init__(self, source_stream):
        self.source_stream = source_stream
        self.line = 1
        self.column = 0
        self.character = 'STX'
        self.next_character()

    def get_character(self):
        return self.character

    def get_line(self):
        return self.line

    def get_column(self):
        return self.column

    def get_position(self):
        return self.line, self.column

    def next_character(self):
        if self.character == "":
            return
        if self.character == '\n':
            self.line += 1
            self.column = 0
        # if self.character == '\\':
        #     return
        new_character = self.source_stream.read(1)  # FIXME!
        if new_character == '\r':
            position = self.source_stream.tell()
            new_character = self.source_stream.read(1)
            if new_character != '\n':
                self.source_stream.seek(position)
                new_character = '\r'
        self.character = new_character
        self.column += 1
































































































#############################################################
        # self.character = new_character
        # while self.character == " ":
        #     self.character = self.source_stream.read(1)
        #         self.character = self.source_stream.read(1)
        # if self.character == '\n' or self.character != '\r' or self.character != '\r\n':
        #     self.line += 1
        #     self.column = 0
        # else:
        #     self.column += 1
        # return self.character
        #
        #
        # self.character = self.source_stream.read(1)
        # if self.character == '/*':
        #     while self.character != '*/':  # czy ignorować wszystko po */ ale w tej samej linii?
        #         if self.character == '\n' or self.character == '\r' or self.character == '\r\n':
        #             self.line += 1
        #             self.column = 0
        #         self.column += 1
        #     self.character = self.source_stream.read(1)
        # if self.character == '#':
        #     while self.character != '\n' or self.character != '\r' or self.character != '\r\n':
        #         self.character = self.source_stream.read(1)
        # if self.character == '\n' or self.character != '\r' or self.character != '\r\n':
        #     self.line += 1
        #     self.column = 0
        # else:
        #     self.column += 1
        # return self.character
