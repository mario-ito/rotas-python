class Presenter:

    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    RESET = "\u001b[0m"

    def __print_styled(self, text, color):
        print(color + text + self.RESET)

    def print_title(self, text):
        self.__print_styled(text, self.CYAN)

    def print_success(self, text):
        self.__print_styled(text, self.GREEN)

    def print_error(self, text):
        self.__print_styled(text, self.RED)
