import re


class HTMLparser:
    def __init__(self, file_path):

        self.file_path = file_path
        self.read_file()
        self.parse_file()

    def read_file(self):
        with open(self.file_path, "r") as file:
            self.file = file.read()

    def parse_file(self):
        # Select only the body
        self.body = self.file[self.file.find("<body>") + 6 : self.file.find("</body>")]
        # Remove padding
        self.body = self.body.strip()

        self.body = re.sub(r"<.*?>", "", self.body, flags=re.DOTALL)

        while re.search(r"\n\s*\n", self.body, flags=re.DOTALL):

            self.body = re.sub(r"\n\s*\n", "\n", self.body, flags=re.DOTALL)

        self.lines = [line for line in self.body.split("\n") if line]

        # Preseve relative indentation
        # while all(str.isspace(line) or line[0] == " " for line in self.lines):

        #     self.lines = [line[1:] for line in self.lines if line]
        #     self.lines = [line for line in self.lines if line]

        # Remove leading/trailing whitespace
        self.lines = [line.strip() for line in self.lines]

    def getlines(self):

        yield from self.lines

    def __repr__(self):
        return f"HTMLparser('{self.file_path}')"
