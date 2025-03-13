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

    def display_bar_chart(self, labels, bins):
        plt.bar(labels, bins)
        plt.show()
