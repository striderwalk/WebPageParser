import argparse
import os

import parser
import ui


def get_filepath():
    arg_parser = argparse.ArgumentParser(description="HTML parser")
    arg_parser.add_argument("filepath", type=str, help="The file to parse")

    args = arg_parser.parse_args()

    if not os.path.isfile(args.filepath):
        print(f"The file '{args.filepath}' could not be found.")
        exit()
    return args.filepath


def main():
    filepath = get_filepath()
    fileparser = parser.HTMLparser(filepath)

    app_ui = ui.UI(fileparser)
    app_ui.run()


if __name__ == "__main__":
    main()
