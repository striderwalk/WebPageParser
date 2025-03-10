import os


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
        print("\nSelect an option:")
        print("\t1. Display words by frequency")
        print("\t2. Display plot")
        print("\t3. Exit")

        choice = None
        while choice not in ["1", "2", "3"]:
            choice = input("Enter your choice (1-3): ").strip()

            if choice not in ["1", "2", "3"]:
                print("Invalid choice. Please try again.")

        return int(choice)

    def reorder_options(self):
        print("\nOrder options:")
        print("\t1. Frequency order")
        print("\t2. Reverse frequency order")
        print("\t3. Alphabetical order")
        print("\t4. Reverse alphabetical order")
        print("\t5. Exit")

        choice = None
        while choice not in ["1", "2", "3", "4", "5"]:
            choice = input("Enter your choice (1-5): ").strip()

            if choice not in ["1", "2", "3", "4", "5"]:
                print("Invalid choice. Please try again.")

        return int(choice)
