from dataclasses import dataclass
from typing import Any


@dataclass
class MenuOption:

    display_name: str
    value: Any


class Menu:

    def __init__(self, options, highlight_last_choice=False):

        self._options = options
        self._last_choice = 0

        self.raise_if_invalid_choice = False
        self.highlight_last_choice = highlight_last_choice

    def display(self):

        print("\nSelect an option:")
        for i, option in enumerate(self._options):
            if self.highlight_last_choice and i == self._last_choice:
                print(f"\u001b[33m\t{i + 1}. {option.display_name}\u001b[0m")
            else:
                print(f"\t{i + 1}. {option.display_name}")

        print("")

    def get_choice(self):
        while True:
            choice = input(f"Enter your choice 1 to {len(self._options)}: ")
            try:
                choice = int(choice)
            except ValueError:
                error_description = "Selected choice was not a number."
                if self.raise_if_invalid_choice:
                    raise ValueError(error_description)
                else:
                    print(error_description)
                continue

            if choice < 1 or choice > len(self._options):
                range_error_description = "Selected choice was not one of the options."
                if self.raise_if_invalid_choice:

                    raise ValueError(range_error_description)
                else:
                    print(range_error_description)

                continue
            self._last_choice = choice - 1
            return self._options[choice - 1].value
