def input_required(message):
    while True:
        output = input(message).strip()
        if output != "":
            return output
        print("O campo é obrigatório!")
        wait_input()


def input_in_range(message, validation_range, exit_character):
    while True:
        user_input = input(message).strip()

        if user_input.lower() == exit_character.lower():
            return exit_character

        user_input = int(user_input)
        if user_input in validation_range:
            return user_input

        print("O valor deve estar entre " + str(list(validation_range)[0]) + " e " + str(list(validation_range)[-1]))
        wait_input()


def wait_input():
    input("Pressione Enter para continuar\n")
