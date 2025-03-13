from collections import Counter
import re
import string

import numpy as np


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

    def get_words(self, remove_numbers=True):
        # Returns a generator for each word
        words = [
            word
            for word in self.body.replace("\n", "").split(" ")
            if word and (remove_numbers and word.isalpha())
        ]

        return words

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

    def get_length_counts(self, grouped=False):

        lengths = []

        for word in self.get_words():

            lengths += [len(word)]

        word_lengths = np.array(lengths)
        length_counts = Counter(word_lengths)

        length_counts = sorted(length_counts.items(), key=lambda x: x[0])

        if not grouped:

            return {
                "labels": [int(i[0]) for i in length_counts],
                "data": [int(i[1]) for i in length_counts],
            }
        else:
            groups = ["1-3", "4-6", "7-10", "10+"]
            word_lengths = np.array(word_lengths)
            bins = [
                len(word_lengths[word_lengths <= 3]),
                len(
                    word_lengths[word_lengths <= 6][
                        word_lengths[word_lengths <= 6] >= 4
                    ]
                ),
                len(
                    word_lengths[word_lengths <= 10][
                        word_lengths[word_lengths <= 10] >= 7
                    ]
                ),
                len(word_lengths[word_lengths > 10]),
            ]

            return {
                "labels": groups,
                "data": bins,
            }

    def __repr__(self):
        return f"HTMLparser('{self.file_path}')"
