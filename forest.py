class Forest:
    def __init__(self, name, wood_type, base_yield, price):
        self.name = name
        self.wood_type = wood_type
        self.base_yield = base_yield
        self.price = price

    def cut(self, player):
        if player.stamina <= 0:
            return False, "You are exhausted. End the day to recover."

        quantity = self.base_yield * player.power
        player.add_wood(self.wood_type, quantity)
        player.stamina -= 1

        return True, (
            f"You chopped a tree in {self.name}. "
            f"+{quantity} {self.wood_type}. "
            f"Stamina: {player.stamina}/{player.max_stamina}"
        )
