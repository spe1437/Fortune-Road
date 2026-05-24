def get_choice(prompt: str, valid_choices: list[str]) -> str:
    '''
    Repeatedly asks the user for input until
    a valid choice is entered.

    Returns the validated user choice.
    '''
    while True:
        choice = input(prompt)
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")
