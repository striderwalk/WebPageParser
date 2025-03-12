import os

from matplotlib import pyplot as plt


class Cli:
    def __init__(self):
        pass

    def clear(self):
        os.system("clear")

    def display_text(self, text):
        print(text)

    def get_filepath(self):
        filepath = None
        while not filepath or not os.path.isfile(filepath):
            filepath = input("Enter the filepath: ")

            if not os.path.isfile(filepath):
                print(f"The file '{filepath}' could not be found.")

        return filepath

    def display_word_length(self, lengths):

        plt.hist(lengths, color="lightgreen", ec="black", bins=15)
        plt.show()

    def display_word_length_groupped(self, groups, bins):
        plt.bar(groups, bins)
        plt.show()
