import random
from property import Property

class Board:
    def __init__(self, size: int, board_type: str):
        self.board_type = board_type
        self.properties = {}

        #1: random; 2: file
        if self.board_type == '1':
            self.size = size
            self.board = self.create_empty_board()
            self.path = self.create_path()
            self.generate_random_tiles()
        elif self.board_type == '2':
            self.board = self.load_board_from_file('data/board.txt')
            self.size = len(self.board)
            self.path = self.create_path()
        else:
            raise ValueError('Invalid board type.')

    def create_empty_board(self) -> list[list[str]]:
        board = []
        for row in range(self.size):
            board.append([])
            for col in range(self.size):
                board[row].append(" ")

        return board
    
    #show the board
    def display_board(self, players=None) -> None:
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):

                player_symbols = ''

                #show each player currently at this position
                if players is not None:
                    for player in players:
                        if not player.bankrupt:
                            player_row, player_col = self.path[player.position]
                            if player_row == row_index and player_col == col_index:
                                player_symbols += player.symbol

                if player_symbols != '':
                    display = f'{cell}[{player_symbols}]'
                    #print(f"[{player_symbols}]".center(5), end = '')
                else:
                    display = cell
                    #print(f"{cell:^5}", end = '')
                print(f"{display:<8}", end = '')

            print()

    #show player's property map
    def display_property_map(self, player) -> None:
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                symbol = ''
                if (row_index, col_index) in self.path:
                    symbol = '·'
                    for position in self.properties:
                        property_row, property_col = self.path[position]
                        if property_row == row_index and property_col == col_index:
                            property = self.properties[position]
                            if property.owner == player:
                                symbol = f"L{property.level}"
                print(f"{symbol:^5}", end = '')
            print()



    #create the movement path around the outer edge of the board
    def create_path(self) -> list[tuple]:
        path = []

        #create the top row
        for col in range(self.size):
            path.append((0, col))
        #create the right column
        for row in range(1, self.size):
            path.append((row, self.size - 1))
        #create the bottom row
        for col in range(self.size - 2, -1, -1):
            path.append((self.size - 1, col))
        #create the left column
        for row in range(self.size - 2, 0, -1):
            path.append((row, 0))

        return path

    #create the tile list, including every type of tiles
    def create_tiles(self) -> list[str]:
        path_length = len(self.path)

        land_count = path_length * 50 // 100            # 50%
        chance_count = path_length * 20 // 100          # 20%
        tax_count = path_length * 10 // 100             # 10%
        jail_count = path_length * 10 // 100            # 10%

        #1: start tile
        bonus_count = path_length - 1 - land_count - chance_count - tax_count - jail_count

        tiles = []
        for i in range(land_count):
            tiles.append("L")
        for i in range(chance_count):
            tiles.append("?")
        for i in range(tax_count):
            tiles.append("T")
        for i in range(jail_count):
            tiles.append("J")
        for i in range(bonus_count):
            tiles.append("B")

        return tiles
    
    #shuffle the tiles to create a random board layout
    def generate_random_tiles(self) -> None:
        tiles = self.create_tiles()
        random.shuffle(tiles)

        row, col = self.path[0]
        self.board[row][col] = 'S'

        for i in range(1, len(self.path)):
            row, col = self.path[i]
            self.board[row][col] = tiles[i - 1]
            if tiles[i - 1] == 'L':
                self.properties[i] = Property() 

    #return the tile type at a given path position
    def get_tile(self, position: int) -> str:
        row, col = self.path[position]
        return self.board[row][col]
    
    #convert the position into coordinates
    def get_position_coordinates(self, position: int) -> tuple:
        return self.path[position]

    #load file
    def load_board_from_file(self, filename: str) -> list[list[str]]:
        board = []

        file = open(filename, "r")
        for line in file:
            row = line.strip().split(",")
            board.append(row)
        file.close()

        return board
  

