def get_choice(prompt: str, valid_choice: list[str]) -> str:
    while True:
        choice = input(prompt)
        if choice in valid_choice:
            return choice
        print("Invalid choice. Please try again.")
