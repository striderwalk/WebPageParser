import argparse
import os

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
                self.display_frequencys()

            if choice == 2:
                self.display_plot()

                input()

            if choice == 3:
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

    def display_plot(self):
        frequencys = self.parser.get_frequencys()
        frequencys = sorted(frequencys, key=lambda x: x[1], reverse=True)
        self.app_ui.display_plot(frequencys)


if __name__ == "__main__":
    App()
