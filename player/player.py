from economy.items import get_item_info

class Player:
    def __init__(self, name="Explorer"):
        self.name = name
        self.level = 5
        self.xp = 340
        self.max_xp = 600
        self.money = 2450
        
        self.max_stamina = 100
        self.stamina = 80
        self.power = 2
        
        self.day = 12
        self.time_of_day = "Morning"  # Morning, Afternoon, Evening, Night
        self.current_location = "Village"
        self.equipment = "Basic Axe"
        
        self.max_weight = 100.0
        
        # Initial inventory mirroring the mockup screenshot
        self.inventory = {
            "pine_wood": 12,
            "oak_wood": 8,
            "redwood_wood": 15,
            "stone": 6,
            "iron_ore": 4,
            "berries": 20,
            "mushrooms": 7,
            "herb": 3,
            "flower": 2,
            "fish": 2,
            "leather": 1,
            "crystal": 1,
        }

    def total_weight(self):
        weight = 0.0
        for item_id, count in self.inventory.items():
            info = get_item_info(item_id)
            weight += info.get("weight", 1.0) * count
        return round(weight, 1)

    def add_item(self, item_id, quantity=1):
        if quantity <= 0:
            return False, "Invalid quantity."
        info = get_item_info(item_id)
        added_weight = info.get("weight", 1.0) * quantity
        if self.total_weight() + added_weight > self.max_weight:
            return False, "Inventory is full! Weight limit reached."
            
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity
        return True, f"+{quantity} {info['name']}"

    def remove_item(self, item_id, quantity=1):
        if self.inventory.get(item_id, 0) < quantity:
            return False, "Not enough items."
        self.inventory[item_id] -= quantity
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
        return True, f"-{quantity} {item_id}"

    def add_xp(self, amount):
        self.xp += amount
        leveled_up = False
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp = int(self.max_xp * 1.35)
            self.max_stamina += 10
            self.stamina = self.max_stamina
            if self.level % 2 == 0:
                self.power += 1
            leveled_up = True
        return leveled_up

    def consume_stamina(self, amount):
        if self.stamina < amount:
            return False
        self.stamina -= amount
        return True

    def advance_time(self, steps=1):
        times = ["Morning", "Afternoon", "Evening", "Night"]
        idx = times.index(self.time_of_day) if self.time_of_day in times else 0
        new_idx = idx + steps
        days_passed = new_idx // len(times)
        self.day += days_passed
        self.time_of_day = times[new_idx % len(times)]

    def rest(self):
        """Resting advances to the next morning and restores stamina."""
        self.day += 1
        self.time_of_day = "Morning"
        self.stamina = self.max_stamina
        return f"Day {self.day} began. Stamina restored to {self.max_stamina}!"

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "max_xp": self.max_xp,
            "money": self.money,
            "max_stamina": self.max_stamina,
            "stamina": self.stamina,
            "power": self.power,
            "day": self.day,
            "time_of_day": self.time_of_day,
            "current_location": self.current_location,
            "equipment": self.equipment,
            "inventory": dict(self.inventory)
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data.get("name", "Explorer"))
        p.level = data.get("level", 1)
        p.xp = data.get("xp", 0)
        p.max_xp = data.get("max_xp", 500)
        p.money = data.get("money", 100)
        p.max_stamina = data.get("max_stamina", 100)
        p.stamina = data.get("stamina", 100)
        p.power = data.get("power", 1)
        p.day = data.get("day", 1)
        p.time_of_day = data.get("time_of_day", "Morning")
        p.current_location = data.get("current_location", "Village")
        p.equipment = data.get("equipment", "Basic Axe")
        p.inventory = data.get("inventory", {})
        return p
