class Player:
    def __init__(self, name):
        self.name = name
        self.day = 1
        self.money = 100
        self.level = 1
        self.stamina = 10
        self.max_stamina = 10
        self.power = 1
        self.inventory = {}

    def reset_stamina(self):
        self.stamina = self.max_stamina

    def add_wood(self, wood_type, quantity):
        self.inventory[wood_type] = self.inventory.get(wood_type, 0) + quantity

    def remove_wood(self, wood_type, quantity):
        if self.inventory.get(wood_type, 0) < quantity:
            return False
        self.inventory[wood_type] -= quantity
        if self.inventory[wood_type] == 0:
            del self.inventory[wood_type]
        return True

    def total_wood(self):
        return sum(self.inventory.values())
