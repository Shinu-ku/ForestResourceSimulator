class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.money = 100
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.power = 10
        self.current_location = "Village"
        self.equipment = "Basic Axe"
        self.inventory = {}
        
    def add_item(self, item, quantity):
        self.inventory[item] = self.inventory.get(item, 0) + quantity
