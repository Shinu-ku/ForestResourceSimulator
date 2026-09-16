from player import Player
from forest import Forest
from dsa.graph import Graph
from dsa.queue import Queue


class Game:
    """Game rules and state, kept independent from the Pygame interface."""

    def __init__(self):
        self.player = None
        self.forests = [
            Forest("Pine Forest", "Pine Wood", 2, 8),
            Forest("Oak Forest", "Oak Wood", 3, 12),
            Forest("Redwood Forest", "Redwood", 4, 20),
        ]
        self.forest_map = Graph()
        self.forest_map.add_edge("Pine Forest", "Oak Forest")
        self.forest_map.add_edge("Oak Forest", "Redwood Forest")
        self.activity_log = Queue()

    def new_game(self, name):
        self.player = Player(name)
        self.log_activity(f"{name} arrived at the forest camp.")

    def log_activity(self, message):
        """Keep a short FIFO history for the GUI activity panel."""
        self.activity_log.enqueue(message)
        if self.activity_log.size() > 5:
            self.activity_log.dequeue()

    def recent_activities(self):
        return self.activity_log.items()

    def reachable_forests(self):
        """Return forests in BFS order from the starting forest."""
        return self.forest_map.bfs("Pine Forest")

    def cut_wood(self, forest_index):
        if self.player is None:
            return False, "Start a game first."

        if not 0 <= forest_index < len(self.forests):
            return False, "Invalid forest."

        success, message = self.forests[forest_index].cut(self.player)
        self.log_activity(message)
        return success, message

    def sell_wood(self, forest_index, quantity):
        if self.player is None:
            return False, "Start a game first."

        forest = self.forests[forest_index]
        available = self.player.inventory.get(forest.wood_type, 0)

        if quantity <= 0 or quantity > available:
            return False, f"Enter a quantity from 1 to {available}."

        self.player.remove_wood(forest.wood_type, quantity)
        earnings = quantity * forest.price
        self.player.money += earnings
        message = f"Sold {quantity} {forest.wood_type} for ${earnings}."
        self.log_activity(message)
        return True, message

    def end_day(self):
        self.player.day += 1
        self.player.reset_stamina()
        message = f"Day {self.player.day} started. Stamina restored."
        self.log_activity(message)
        return message

    def run_gui(self):
        from gui.app import run
        run(self)
