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
            self.app_ui.get_filepath()

        self.fileparser = parser.HTMLparser(filepath)

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
            choice = self.app_ui.user_options()

            if choice == 1:
                self.app_ui.clear()
                self.app_ui.display_text(self.fileparser.get_frequencys())
                input()

            if choice == 2:
                self.app_ui.clear()
                self.app_ui.display_text("PLOT")
                input()

            if choice == 3:
                exit()


if __name__ == "__main__":
    App()
