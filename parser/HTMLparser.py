import re


class HTMLparser:
    def __init__(self, file_path):

        self.file_path = file_path
        self.read_file()
        self.parse_file()
        # self.save_file()

    # def save_file(self):

    def read_file(self):
        with open(self.file_path, "r", encoding="UTF-8") as file:
            self.file = file.read()

    def parse_file(self):
        # Select only the body
        self.body = self.file[self.file.find("<body>") + 6 : self.file.find("</body>")]
        # Remove padding
        self.body = self.body.strip()

        # Remove all HTML tags using regular expressions
        self.body = re.sub(r"<.*?>", "", self.body, flags=re.DOTALL)

        # Remove extra newlines
        self.body = re.sub(r"\n\s*\n", "\n", self.body, flags=re.DOTALL)

        self.lines = [line for line in self.body.split("\n") if line]

        # Preseve relative indentation
        while all(str.isspace(line) or line[0] == " " for line in self.lines):

            self.lines = [line[1:] for line in self.lines if line]
            self.lines = [line for line in self.lines if line]

        # Remove leading/trailing whitespace
        # self.lines = [line.strip() for line in self.lines]

    def getlines(self):
        # Returns a generator for each line
        yield from self.lines

    def getwords(self):
        # Returns a generator for each word
        yield from [word for word in self.body.replace("\n", "").split(" ") if word]

    def get_frequencys(self):
        word_freq = {}
        for word in self.getwords():
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] = word_freq[word] + 1

        return word_freq

    def __repr__(self):
        return f"HTMLparser('{self.file_path}')"
