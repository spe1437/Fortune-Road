class Property:
    def __init__(self):
        self.owner = None
        self.rent = 50
        self.price = 200
        self.level = 1

    def buy(self, player) -> bool:
        if self.owner is None and player.money >= self.price:
            player.spend_money(self.price)
            self.owner = player
            player.properties.append(self)
            return True
        return False

    def pay_rent(self, player) -> None:
        if self.owner is not None and self.owner != player:
            rent = self.rent
            if player.double_rent:
                rent *= 2
                player.double_rent = False
                print("Double rent effect activated!")

            player.spend_money(rent)
            self.owner.earn_money(rent)
    
    def upgrade_property(self, player) -> bool:
        upgrade_cost = self.level * 100
        
        if self.owner == player and player.money >= upgrade_cost:
            player.spend_money(upgrade_cost)
            self.level += 1
            self.rent += 50
            return True
        return False
    
    

