import argparse
import datetime
import os
from enum import Enum


import parser
import cli


class MainMenuValues(Enum):
    SORT = 0
    SAVE = 1
    EXIT = 2
    FREQUENCY = 3
    LENGTHS = 4
    GROUPED_LENGTHS = 5


class App:
    def __init__(self):
        self.app_cli = cli.Cli()

        self.app_cli.clear()
        # If the file isn't specified in the command line promt user
        if not (filepath := self.check_args()):
            filepath = self.app_cli.get_filepath()

        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()

        self.parser = parser.HtmlParser(text)
        self.frequencys = self.parser.get_frequencys()
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
            self.app_cli.clear()

            user_options = [
                cli.MenuOption("By Frequency", MainMenuValues.FREQUENCY),
                cli.MenuOption("Word length graph", MainMenuValues.LENGTHS),
                cli.MenuOption(
                    "Grouped word length graph", MainMenuValues.GROUPED_LENGTHS
                ),
                cli.MenuOption("Exit", MainMenuValues.EXIT),
            ]
            menu = cli.Menu(user_options)
            menu.display()
            choice = menu.get_choice()

            if choice == MainMenuValues.FREQUENCY:
                self.display_frequency_menu()

            if choice == MainMenuValues.LENGTHS:
                self.display_word_length()

            if choice == MainMenuValues.GROUPED_LENGTHS:
                self.display_word_length(grouped=True)

            if choice == MainMenuValues.EXIT:
                return

    def display_frequency_menu(self):
        self.app_cli.clear()

        self.display_frequencys()

        while True:
            options = [
                cli.MenuOption("Resort", MainMenuValues.SORT),
                cli.MenuOption("Save", MainMenuValues.SAVE),
                cli.MenuOption("Exit", MainMenuValues.EXIT),
            ]

            menu = cli.Menu(options)
            menu.display()

            match menu.get_choice():
                case MainMenuValues.SORT:
                    sort_options = [
                        cli.MenuOption("Frequency order", (lambda x: x[1], True)),
                        cli.MenuOption(
                            "Reverse Frequency order", (lambda x: x[1], False)
                        ),
                        cli.MenuOption("Alphabetical order", (lambda x: x[0], False)),
                        cli.MenuOption(
                            "Reverse alphabetical order", (lambda x: x[0], True)
                        ),
                    ]

                    sort_menu = cli.Menu(sort_options, highlight_last_choice=True)

                    sort_menu.display()

                    sort_option = sort_menu.get_choice()

                    self.frequencys = sorted(
                        self.frequencys, key=sort_option[0], reverse=sort_option[1]
                    )

                    self.display_frequencys()

                case MainMenuValues.SAVE:
                    # Save to output file
                    filename = f"./output/output-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
                    with open(filename, "w", encoding="utf-8") as file:
                        for word, frequency in self.frequencys:
                            file.write(f"{word}\t{frequency}\n")

                    self.app_cli.clear()
                    self.app_cli.display_text(f"Saved to {filename}")

                case MainMenuValues.EXIT:
                    return

    def display_frequencys(self):
        for word, frequency in self.frequencys:
            # Display text
            self.app_cli.display_text(f"{word: <20}\t{frequency: > 5}")

    def display_word_length(self, grouped=False):
        # Display bar chart of word length

        res = self.parser.get_length_counts(grouped)

        self.app_cli.display_bar_chart(res["labels"], res["data"])


if __name__ == "__main__":
    try:
        App()
    except KeyboardInterrupt:
        pass
