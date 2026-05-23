from player import Player
from input_helper import get_choice

def display_title():
    print("=" * 40)
    print(f"{'FORTUNE ROAD':^40}")
    print("=" * 40)
    print(f"{'A Text-Based Monopoly Board Game':^40}")
    print("=" * 40)

def display_main_menu():
    print()
    print("1. Start Game")
    print("2. View Rules")
    print("3. Exit")
    print()

    choice = get_choice("Enter choice(1/2/3): ",['1','2','3'])
    return choice
    

def choose_game_mode():
    print()
    print("Choose Game Mode:")
    print("1. Fixed Round Mode")
    print("2. Endless Mode")
    print()

    game_mode = get_choice("Enter choice(1/2): ", ['1','2'])
    return game_mode

def choose_board_type():
    print()
    print("Choose Board Type:")
    print("1. Random Board")
    print("2. Load Board From File")
    
    print()

    board_type = get_choice("Enter choice(1/2): ",['1','2'])
    return board_type

def choose_board_size():
    while True:
        print()
        print("Choose Board Size:")
        print("1. Small  (5x5)")
        print("2. Medium (7x7)")
        print("3. Large  (9x9)")
        print()

        command = get_choice("Enter choice (1/2/3): ", ['1','2','3'])

        if command == "1":
            return 5
        elif command == "2":
            return 7
        elif command == "3":
            return 9
        #else:
            #print("Please enter a valid number.")

def get_players() -> list[Player]:
    players = []

    while True:
        try:
            number = int(input("Enter number of players (2-4): "))

            if number < 2 or number > 4:
                print("Please enter a number between 2 and 4.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    symbols = ["A", "B", "C", "D"]

    for i in range(number):
        player = Player(symbols[i])
        players.append(player)

    return players
