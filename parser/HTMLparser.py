class HTMLparser:
    def __init__(self, file_path):

        self.file_path = file_path
        self.read_file()
        self.parse_file()

    def read_file(self):
        with open(self.file_path, "r") as file:
            self.file = file.read()

    def parse_file(self):
        # This will eventually parse the HTML removing all HTML tags
        ...

    def getlines(self):

        yield from self.file.split("\n")

    def __repr__(self):
        return f"HTMLparser('{self.file_path}')"
