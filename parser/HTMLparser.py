from collections import Counter
import re
import string


class HTMLparser:
    def __init__(self, text):

        self.text = text

        self.parse_file()

    def parse_file(self):
        # Select only the body
        self.body = self.text[self.text.find("<body>") + 6 : self.text.find("</body>")]
        # Remove padding
        self.body = self.body.strip()

        # Remove all HTML tags using regular expressions
        self.body = re.sub(r"<.*?>", "", self.body, flags=re.DOTALL)

        # Remove extra newlines
        self.body = re.sub(r"\n\s*\n", "\n", self.body, flags=re.DOTALL)

        # Remove punctuation
        transtable = str.maketrans("", "", string.punctuation)
        transtable[ord("'")] = ord("'")

        self.body = self.body.translate(transtable)

        self.lines = [line for line in self.body.split("\n") if line]

        # Preseve relative indentation
        # while all(str.isspace(line) or line[0] == " " for line in self.lines):

        #     self.lines = [line[1:] for line in self.lines if line]
        #     self.lines = [line for line in self.lines if line]

        # Remove leading/trailing whitespace
        self.lines = [line.strip() for line in self.lines]

    def get_lines(self):
        # Returns a generator for each line
        yield from self.lines

    def get_words(self):
        # Returns a generator for each word
        yield from [word for word in self.body.replace("\n", "").split(" ") if word]

    def get_frequencys(self):
        word_freq = {}
        for word in self.getwords():
            if word.lower() not in word_freq:
                word_freq[word.lower()] = [word]
            else:
                word_freq[word.lower()] = word_freq[word.lower()] + [word]

        word_freq_common_case = []
        for word_list in sorted(word_freq.values(), key=lambda x: x[0].lower()):

            data = Counter(word_list)
            # print(data.most_common(1))
            word_freq_common_case.append((data.most_common(1)[0][0], len(word_list)))
            # print(word_freq_common_case[-1])
        return word_freq_common_case

    def __repr__(self):
        return f"HTMLparser('{self.file_path}')"
