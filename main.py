import menu
import rules
from game import Game


def start_game() -> None:
    game_mode = menu.choose_game_mode()
    board_type = menu.choose_board_type()
    if board_type == '2':
        board_size = 0
    elif board_type == '1':
        board_size = menu.choose_board_size()
    players = menu.get_players()

    print(board_size,board_type)
    game = Game(players, board_size, game_mode, board_type)
    game.start()

def main():

    menu.display_title()

    while True:
        choice = menu.display_main_menu()

        if choice == "1":
            start_game()

        elif choice == "2":
            rules.show_rules()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
	main()
