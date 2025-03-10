class UI:
    def __init__(self, parser):
        self.parser = parser

        self.display_results()

    def display_results(self):
        for line in self.parser.getlines():
            print(line)

    def run(self):
        pass
