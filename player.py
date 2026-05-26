class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.money = 1000
        self.position = 0
        self.properties = []
        self.skip_turn = False
        self.double_rent = False
        self.in_debt = False
        self.bankrupt = False
        
    
    def move(self, steps: int, path_length: int) -> bool:
        old_position = self.position
        self.position = (self.position + steps) % path_length
        passed_start = False
        if steps > 0:
            if old_position + steps >= path_length and self.position != 0:
                passed_start = True
        return passed_start
    
    def earn_money(self, amount: int) -> None:
        self.money += amount

    def spend_money(self, amount: int) -> None:
        self.money -= amount
    
    #unfinished
    def get_total_wealth(self) -> int:
        total = self.money
        for property in self.properties:
            total += property.price
        return total

    def check_debt(self) -> bool:
        if self.money < 0:
            self.in_debt = True
        return self.in_debt
    
    def check_bankruptcy(self) -> bool:
        if self.get_total_wealth() < 0:
            self.bankrupt = True
        return self.bankrupt
        
