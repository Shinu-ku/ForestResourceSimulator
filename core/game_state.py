from player.player import Player
from world.world import World
from core.save_manager import SaveManager

class GameState:
    def __init__(self):
        self.player = Player("Explorer")
        self.world = World()
        self.save_manager = SaveManager()
        self.running = True
        self.scene_manager = None
        
        # Modal and UI State
        self.active_modal = None  # "inventory", "shop", "route_finder", "save_load", "location", "how_to_play", "credits"
        self.active_tab = {}      # Modal specific subtab
        
        # Route Finder State
        self.from_location = "Village"
        self.to_location = "Redwood Forest"
        self.selected_algo = "dijkstra"
        self.current_route = None
        self.show_route_on_map = True
        self.route_anim_timer = 0.0
        
        # Location Selection / Interaction
        self.selected_location_name = None
        
        # Notification Toast
        self.toast_message = ""
        self.toast_timer = 0.0
        
        # Precompute initial route
        self.update_route()

    def update_route(self):
        self.current_route = self.world.find_route(
            self.from_location, 
            self.to_location, 
            self.selected_algo
        )

    def set_toast(self, message, duration=3.0):
        self.toast_message = message
        self.toast_timer = duration

    def update(self, dt):
        if self.toast_timer > 0:
            self.toast_timer -= dt
            if self.toast_timer <= 0:
                self.toast_message = ""
                
        self.route_anim_timer = (self.route_anim_timer + dt * 2.0) % 1.0

    def start_new_game(self, name="Explorer"):
        self.player = Player(name)
        self.player.level = 1
        self.player.xp = 0
        self.player.max_xp = 200
        self.player.money = 150
        self.player.day = 1
        self.player.stamina = self.player.max_stamina
        self.player.inventory = {
            "pine_wood": 5,
            "berries": 10
        }
        self.from_location = "Village"
        self.to_location = "Oak Forest"
        self.active_modal = None
        self.update_route()
        self.set_toast(f"Welcome, {name}! Adventure begins.")
