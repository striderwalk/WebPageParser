import argparse
import datetime
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

        self.parser = parser.HtmlParser(text)

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

        reorder_choice = 1
        while True:
            self.app_ui.clear()

            if reorder_choice == 1:
                # Frequency order
                frequencys = sorted(frequencys, key=lambda x: x[1], reverse=True)

            if reorder_choice == 2:
                # Reverse frequency order
                frequencys = sorted(frequencys, key=lambda x: x[1])

            if reorder_choice == 3:
                # Alphabetical order
                frequencys = sorted(frequencys, key=lambda x: x[0])

            if reorder_choice == 4:
                # Reverse alphabetical order
                frequencys = sorted(frequencys, key=lambda x: x[0], reverse=True)

            for word, frequency in frequencys:
                # Display text
                self.app_ui.display_text(f"{word: <20}\t{frequency: > 5}")

            if reorder_choice == 5:
                # Save to output file
                filename = f"./output/output-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
                with open(filename, "w") as file:
                    for word, frequency in frequencys:
                        file.write(f"{word}\t{frequency}\n")

                self.app_ui.clear()
                self.app_ui.display_text(f"Saved to {filename}")
                reorder_choice = last_choice

            if reorder_choice == 6:
                # Exit Menu
                return

            last_choice = reorder_choice
            reorder_choice = self.app_ui.reorder_options(reorder_choice)

    def display_word_length(self):
        # Display bar chart of word length
        words = self.parser.get_words()
        lengths = [len(word) for word in words]

        self.app_ui.display_word_length(lengths)

    def display_word_length_grouped(self):
        # Display groupped bar chart of word length
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
    try:
        App()
    except KeyboardInterrupt:
        pass
