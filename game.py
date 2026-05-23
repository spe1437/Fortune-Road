from board import Board
from chance import Chance
from input_helper import get_choice
import random

class Game:

    def __init__(self, players, board_size, game_mode, board_type):

        self.players = players
        self.board_size = board_size
        self.game_mode = game_mode
        self.board_type = board_type
        self.board = Board(board_size, board_type)
        self.chance = Chance("data/chance_cards.txt")
        self.max_rounds = 20

    def display_game_start_info(self):
        print("=" * 40)
        print(f"{'GAME STARTING':^40}")
        print("=" * 40)
        print()
        print(f"Board Size : {self.board.size}x{self.board.size}")
        print("Players    :", end=" ")
        for player in self.players:
            print(player.symbol, end=" ")
        print()
        print(f"Game Mode  : {self.game_mode}")
        print(f"Board Type : {self.board_type}")
        self.board.display_board(self.players)
        input("\nPress Enter to begin...")

    def play_fixed_round_mode(self) -> None:
        current_round = 1
        end_flag = False

        while current_round <= self.max_rounds:
            print()
            print("=" * 40)
            print(f"Round {current_round}")
            print("=" * 40)

            for player in self.players:
                if not self.take_turn(player):
                    end_flag = True
                    break

            if end_flag:
                break

            self.show_round_summary()
            self.board.display_board(self.players)
            current_round += 1
        
        self.show_winner()
    
    def play_endless_mode(self) -> None:
        current_round = 1
        end_flag = False

        while True:
            print()
            print("=" * 40)
            print(f"Round {current_round}")
            print("=" * 40)

            for player in self.players:
                if not self.take_turn(player):
                    end_flag = True
                    break

            if end_flag:
                break

            self.show_round_summary()
            self.board.display_board(self.players)
            current_round += 1
            
        self.show_winner()

    def start(self) -> None:
        self.display_game_start_info()
        self.board.display_board()

        if self.game_mode == '1':
            self.play_fixed_round_mode()
        elif self.game_mode == '2':
            self.play_endless_mode()


    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def take_turn(self, player) -> bool:
        if player.bankrupt:
            return True
        
        if player.skip_turn:
            print(f"Player {player.symbol} skips this turn.")
            player.skip_turn = False
            return True

        while True:
            print()
            print(f"Player {player.symbol}'s turn")
            print("1. Roll Dice")
            print("2. Show My Information")
            print("3. Propse Ending Game")
            choice = get_choice("Choose an action(1/2/3): ", ['1','2','3'])

            if choice == '1':
                dice = self.roll_dice()
                print(f"Player {player.symbol} rolled {dice}.")

                passed_start = player.move(dice, len(self.board.path))
                if passed_start:
                    player.earn_money(1000)
                    print(f"Player {player.symbol} passed Start and received $1000.")

                tile = self.board.get_tile(player.position)
                print(f"Player {player.symbol} landed on tile: {tile}")
                self.handle_tile(player, tile)
                self.check_player_status(player)
                if player.in_debt:
                    self.handle_debt(player)
                if self.only_one_player_left():
                    return False
                return True

            elif choice == '2':
                self.show_information(player)

            elif choice == '3':
                print(f"Player {player.symbol} proposed to end the game.")
                if self.ask_end_game(player):
                    return False
            else:
                print("Invalid choice.")

    def ask_end_game(self, player) -> bool:
        for p in self.players:
            if p == player:
                continue
            if p.bankrupt:
                continue
            choice = get_choice(f"Player {p.symbol}, do you agree to end the game? (y/n) ", ['y','n'])
            if choice.lower() == 'n':
                print(f"Player {p.symbol} rejected the proposal. The game continues.")
                return False
        return True
                
    def handle_tile(self, player, tile) -> None:
        if tile == 'S':
            print("You are in the Start tile.")

        elif tile == 'L':
            print("Land tile.")
            property = self.board.properties[player.position]

            if property.owner is None:
                choice = get_choice("Buy this property? (y/n) ", ['y','n'])
                if choice.lower() == 'y':
                    if property.buy(player):
                        print("Property purchased!")
                    else:
                        print("Sorry, you don't have enough money.")

            elif property.owner != player:
                print(f"This land belongs to Player {property.owner.symbol}.")
                print(f"Rent is ${property.rent}.")
                property.pay_rent(player)
                print(f"Player {player.symbol} paid rent.")

                choice = get_choice("Do you want to offer to buy this property? (y/n) ",['y','n'])
                if choice.lower() == 'y':
                    self.offer_to_buy_property(player, property)

                print(f"Player {player.symbol}'s current money: ${player.money}")
                
            elif property.owner == player:
                print("This is your own land.")
                choice = get_choice("Do you want to upgrade your land? (y/n) ", ['y','n'])
                if choice.lower() == 'y':
                    if property.upgrade_property(player):
                        print("Successful upgrade.")
                    else:
                        print("Sorry, you don't have enough money.")

        elif tile == 'T':
            print("Tax tile.")
            player.spend_money(100)
            print(f"Player {player.symbol} paid $100 tax.")

        elif tile == 'B':
            print("Bonus tile.")
            player.earn_money(100)
            print(f"Player {player.symbol} received $100 bonus.")

        elif tile == 'J':
            print("Jile tile.")
            player.skip_turn = True
            print(f"Player {player.symbol} will skip the next turn.")

        elif tile == '?':
            print("Chance tile.")
            new_tile = self.chance.trigger(player, self.board)
            if new_tile is not None:
                self.handle_tile(player, new_tile)

        
    def check_player_status(self, player) -> None:
        if player.check_bankruptcy():
            print(f"Player {player.symbol} is bankrupt.")
        elif player.check_debt():
            print(f"Player {player.symbol} is in debt.")

    def show_winner(self) -> None:
        print()
        print("=" * 40)
        print("The game is over.")
        print("=" * 40)

        winner = None
        highest_wealth = -1

        for player in self.players:
            if not player.bankrupt:
                wealth = player.get_total_wealth()
                print(f"Player {player.symbol}: ${wealth}")
                if wealth > highest_wealth:
                    highest_wealth = wealth
                    winner = player
        
        print()
        print(f"Winner: Player {winner.symbol}. Congratulation!")
    
    def show_round_summary(self) -> None:
        print()
        print("-" * 40)
        print(f"{'CASH SUMMARY':^40}")
        print("-" * 40)

        for player in self.players:
            if player.bankrupt:
                print(f"{f'Player {player.symbol}':<20}: Bankrupt")
            else:
                print(f"{f'Player {player.symbol}':<20}: ${player.money}")
        print("-" * 40)

    def show_information(self, player) -> None:
        print("-" * 40)
        print(f"Player {player.symbol}'s Information")
        print("-" * 40)

        print(f"{'Player':<15}: {player.symbol}")
        print(f"{'Money':<15}: ${player.money}")
        print(f"{'Position':<15}: {player.position}")

        #current_tile = self.board.get_tile(player.position)
        #print(f"{'Current Tile':<15}: {current_tile}")

        print(f"{'Properties Owned':<15}: {len(player.properties)}")
        if len(player.properties) != 0:
            print("Property Map:")
            self.board.display_property_map(player)

        print(f"{'Total Wealth':<15}: ${player.get_total_wealth()}")

        print("-" * 40)

    def sell_property(self, player) -> bool:
        if len(player.properties) == 0:
            print("You don't have any properties to sell.")
            return False
        
        print()
        print("Your properties:")

        for i, property in enumerate(player.properties, start = 1):
            print(f"{i}. Level {property.level}  Sell Value: ${(property.price // 2) + ((property.level - 1) * 50)}")

        choice = input("Choose a property to sell: ")

        try:
            index = int(choice) - 1
            if index < 0 or index >= len(player.properties):
                print("Invalid property number.")
                return False
            property  = player.properties[index]
            sell_value = (property.price // 2) + ((property.level - 1) * 50)
            player.earn_money(sell_value)

            property.owner = None
            property.level = 1
            property.rent = 50
            player.properties.pop(index)

            print(f"Property sold for ${sell_value}.")
            print(f"Player {player.symbol} now has ${player.money}.")
            return True

        except ValueError:
            print("Please enter a valid number.")
            return False
    
    def handle_debt(self, player) -> None:
        while player.money < 0 and not player.bankrupt:
            print()
            print("=" * 40)
            print(f"Player {player.symbol} is in debt.")
            print(f"Current money: ${player.money}")
            print("=" * 40)

            '''
            if len(player.properties) == 0:
                print("No properties left to sell.")
                print(f"Player {player.symbol} is bankrupt.")
                player.bankrupt = True
                return
            '''

            print("1. Sell Property")
            print("2. Declare Bankruptcy")

            choice = get_choice("Choose an option(1/2): ", ['1','2'])

            if choice == '1':
                self.sell_property(player)
            elif choice == '2':
                for property in player.properties:
                    property.owner = None
                    property.level = 1
                    property.rent = 50

                player.properties.clear()

                player.bankrupt = True
                print(f"Player {player.symbol} declared bankruptcy.")
                return

    def offer_to_buy_property(self, buyer, property) -> None:
        seller = property.owner
        price = property.price + (property.level - 1) * 100
        if buyer.money < price:
            print("You don't have enough money to buy this property.")
            return
        
        choice = get_choice(f"Player {seller.symbol}, sell this property to Player {buyer.symbol} for ${price}? (y/n) ", ['y','n'])

        if choice.lower() == 'y':
            buyer.spend_money(price)
            seller.earn_money(price)
            seller.properties.remove(property)
            buyer.properties.append(property)
            property.owner = buyer

            print("Property trade completed.")
        else:
            print("The owner rejected the trade.")

    # if only one player left, game over and the winner is the last active player
    def only_one_player_left(self) -> bool:
        active_count = 0
        for player in self.players:
            if not player.bankrupt:
                active_count += 1
        if active_count == 1:
            return True
        return False




        
            
    

    


