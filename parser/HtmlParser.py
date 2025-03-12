from collections import Counter
import re
import string


class HtmlParser:
    def __init__(self, text):
        self.text = text

        self.parse_file()

    def parse_file(self):
        # Select only the body
        # self.body = self.text[self.text.find("<body>") + 6 : self.text.find("</body>")]
        self.body = "".join(
            re.findall("<.*body.*>.*<.*/.*body.*>", self.text, flags=re.DOTALL)
        )
        # Remove all HTML tags using regular expressions
        patterns = [
            r"<script[^<>]*?>[^<>]*?<[^<>]*?\/[^<>]*?script[^<>]*?>",
            r"<svg[^<>]*?>[^<>]*?<[^<>]*?\/[^<>]*?svg[^<>]*?>",
            r"<img[^<>]*?\/>",
            r"<style[^<>]*?>[^<>]*?<[^<>]*?\/[^<>]*?style[^<>]*?>",
            r"<.*?>",
        ]
        for pattern in patterns:
            self.body = re.sub(pattern, " ", self.body, flags=re.DOTALL)

        # Remove extra newlines
        self.body = re.sub(r"\n\s*\n", "\n", self.body, flags=re.DOTALL)

        # Remove punctuation
        transtable = str.maketrans("", "", string.punctuation)
        transtable[ord("-")] = ord("-")
        transtable[ord("'")] = ord("'")

        self.body = self.body.translate(transtable)

        with open("output/body.txt", "w", encoding="utf-8") as file:

            file.write(self.body)

    def get_words(self):
        # Returns a generator for each word
        yield from [word for word in self.body.replace("\n", "").split(" ") if word]

    def get_frequencys(self):
        word_freq = {}
        for word in self.get_words():
            if word.lower() not in word_freq:
                word_freq[word.lower()] = [word]
            else:
                word_freq[word.lower()] = word_freq[word.lower()] + [word]

        word_freq_common_case = []
        for word_list in sorted(word_freq.values(), key=lambda x: x[0].lower()):
            data = Counter(word_list)
            word_freq_common_case.append((data.most_common(1)[0][0], len(word_list)))

        return word_freq_common_case

    def __repr__(self):
        return f"HTMLparser('{self.file_path}')"
