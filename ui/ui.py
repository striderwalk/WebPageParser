import os
import matplotlib.pyplot as plt


class UI:
    def __init__(self):
        pass

    def display_text(self, text):
        print(text)

    def clear(self):
        os.system("clear")

    def get_filepath(self):

        filepath = None
        while not filepath or not os.path.isfile(filepath):
            filepath = input("Enter the filepath: ")

            if not os.path.isfile(filepath):
                print(f"The file '{filepath}' could not be found.")

        return filepath

    def user_options(self):
        options = [
            "Display words by frequency",
            "Display word length plot",
            "Display word length occurrences",
            "Exit",
        ]
        print("\nSelect an option:")
        for i, option in enumerate(options):

            print(f"\t{i+1}. {option}")

        choice = 0
        while choice < 1 or choice > len(options):
            choice = input(f"Enter your choice (1-{len(options)}): ").strip()

            if not choice.isdecimal():
                print("Invalid choice, Please enter a number.")
                choice = 0
                continue

            choice = int(choice)
            if choice < 1 or choice > len(options):

                print("Invalid choice, Please try again.")
        return int(choice)

    def reorder_options(self, current):
        options = [
            "Frequency order",
            "Reverse frequency order",
            "Alphabetical order",
            "Reverse alphabetical order",
            "Save current",
            "Exit",
        ]
        print("\nOrder options:")
        for i, option in enumerate(options):
            if current == i + 1:
                print(f"\t\u001b[33;1m{i+1}. {option}\u001b[0m")
            else:
                print(f"\t{i+1}. {option}")

        choice = 0
        while choice < 1 or choice > len(options):
            choice = input(f"Enter your choice (1-{len(options)}): ").strip()

            if not choice.isdecimal():
                print("Invalid choice, Please enter a number.")
                choice = 0
                continue

            choice = int(choice)
            if choice < 1 or choice > len(options):

                print("Invalid choice, Please try again.")
        return int(choice)

    def display_word_length(self, lengths):

        plt.hist(lengths, color="lightgreen", ec="black", bins=15)
        plt.show()

    def display_word_length_groupped(self, groups, bins):
        plt.bar(groups, bins)
        plt.show()
