import argparse
import os

import numpy as np

import parser
import ui


class App:
    def __init__(self):

        self.app_ui = ui.UI()

        self.app_ui.clear()
        # If the file isn't specified in the command line promt user
        if not (filepath := self.check_args()):
            filepath = self.app_ui.get_filepath()

        with open(filepath, "r") as file:

            text = file.read()

        self.parser = parser.HTMLparser(text)

        self.run()

    def check_args(self):
        arg_parser = argparse.ArgumentParser(description="HTML parser")
        arg_parser.add_argument("-f", "--filepath", type=str, help="The file to parse")

        args = arg_parser.parse_args()
        if args.filepath is None:
            return False
        if not os.path.isfile(args.filepath):
            print(f"The file '{args.filepath}' could not be found.")
            exit()
        return args.filepath

    def run(self):
        while True:
            self.app_ui.clear()

            choice = self.app_ui.user_options()

            if choice == 1:
                # Display words by frequency
                self.display_frequencys()

            if choice == 2:
                # Display plot word length distribution
                self.display_word_length()

            if choice == 3:
                # Display plot words  length distribution grouped

                self.display_word_length_grouped()
            if choice == 4:
                exit()

    def display_frequencys(self):
        self.app_ui.clear()

        frequencys = self.parser.get_frequencys()

        reorder_choice = self.app_ui.reorder_options()
        while True:
            self.app_ui.clear()

            if reorder_choice == 1:
                frequencys = sorted(frequencys, key=lambda x: x[1], reverse=True)

            if reorder_choice == 2:
                frequencys = sorted(frequencys, key=lambda x: x[1])

            if reorder_choice == 3:
                frequencys = sorted(frequencys, key=lambda x: x[0])

            if reorder_choice == 4:
                frequencys = sorted(frequencys, key=lambda x: x[0], reverse=True)

            if reorder_choice == 5:
                return

            for word, frequency in frequencys:

                self.app_ui.display_text(f"{word: <20}\t{frequency: > 5}")

            reorder_choice = self.app_ui.reorder_options()

    def display_word_length(self):
        words = self.parser.get_words()
        lengths = [len(word) for word in words]

        self.app_ui.display_word_length(lengths)

    def display_word_length_grouped(self):
        words = self.parser.get_words()
        lengths = np.array([len(word) for word in words])
        groups = ["1-3", "4-6", "7-10", "10+"]
        bins = [
            len(lengths[lengths <= 3]),
            len(lengths[lengths <= 6][lengths[lengths <= 6] >= 4]),
            len(lengths[lengths <= 10][lengths[lengths <= 10] >= 7]),
            len(lengths[lengths > 10]),
        ]

        self.app_ui.display_word_length_groupped(groups, bins)


if __name__ == "__main__":
    App()
