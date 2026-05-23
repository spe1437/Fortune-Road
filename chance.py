import random

class Chance:
    def __init__(self, filename: str):
        self.filename = filename
        self.cards = self.load_cards()

    def load_cards(self) -> list[list[card]]:
        cards = []
        file = open(self.filename, "r")
        for line in file:
            card = line.strip().split(",")
            cards.append(card)
        file.close()
        return cards

    def trigger(self, player, board) -> str:
        card = random.choice(self.cards)
        event_type = card[0]
        value = int(card[1])
        message = card[2]
        print(message)

        if event_type == 'money':
            if value >= 0:
                player.earn_money(value)
            else:
                player.spend_money(-value)
                
        elif event_type == 'move':
            passed_start = player.move(value, len(board.path))
            if passed_start:
                player.earn_money(1000)
                print(f"Player {player.symbol} passed Start and received $1000.")
                
            new_tile = board.get_tile(player.position)
            print(f"Player {player.symbol} moved to tile: {new_tile}")
            return new_tile

        elif event_type == 'jail':
            player.skip_turn = True
        
        elif event_type == 'tax':
            player.spend_money(value)
        
        elif event_type == 'bonus':
            player.earn_money(value)
        
        elif event_type == 'start':
            player.position = 0
            print(f"Player {player.symbol} moved to Start.")

        elif event_type == 'skip':
            player.skip_tun = True
        
        elif event_type == 'double_rent':
            player.double_rent = True
        
        elif event_type == 'free_upgrade':
            if len(player.properties) == 0:
                print("You do not own any properties.")
            else:
                property = random.choice(player.properties)
                property.level += 1
                property.rent += 50
                print("One of your properties was upgraded for free.")

        
        return None





