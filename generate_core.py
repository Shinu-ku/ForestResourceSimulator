import os
from pathlib import Path

base_dir = Path(r"d:\programming\Projects\ForestResourceSimulator")

files_to_create = {
    "core/config.py": """import pygame

WIDTH = 1280
HEIGHT = 720
FPS = 60

# Colors
COLORS = {
    "bg": (24, 30, 28),
    "panel": (37, 45, 42),
    "text": (230, 230, 230),
    "text_dark": (150, 150, 150),
    "highlight": (60, 120, 80),
    "button": (45, 60, 50),
    "button_hover": (55, 75, 60),
    "forest": (34, 139, 34),
    "village": (205, 133, 63),
    "mountain": (139, 137, 137),
    "water": (70, 130, 180),
    "route": (200, 180, 140),
}
""",
    "core/game_state.py": """class GameState:
    def __init__(self):
        self.player = None
        self.world = None
        self.time_manager = None
        self.running = True
        self.scene_manager = None
""",
    "core/scene_manager.py": """import pygame

class Scene:
    def __init__(self, game_state):
        self.game_state = game_state

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def switch_to(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
""",
    "main.py": """import pygame
from core.config import WIDTH, HEIGHT, FPS
from core.game_state import GameState
from core.scene_manager import SceneManager
from ui.screens.main_menu import MainMenu
from ui.screens.game_world import GameWorld

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Forest Resource Simulator")
    clock = pygame.time.Clock()

    game_state = GameState()
    scene_manager = SceneManager()
    game_state.scene_manager = scene_manager

    scene_manager.add_scene("main_menu", MainMenu(game_state))
    scene_manager.add_scene("game_world", GameWorld(game_state))
    scene_manager.switch_to("main_menu")

    while game_state.running:
        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_state.running = False

        scene_manager.handle_events(events)
        scene_manager.update(dt)
        scene_manager.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
""",
    "ui/screens/main_menu.py": """import pygame
from core.scene_manager import Scene
from core.config import COLORS, WIDTH, HEIGHT

class MainMenu(Scene):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # In a real game, initialize the player and world here
                    self.game_state.scene_manager.switch_to("game_world")
                elif event.key == pygame.K_ESCAPE:
                    self.game_state.running = False

    def draw(self, screen):
        screen.fill(COLORS["bg"])
        
        title = self.font.render("FOREST RESOURCE SIMULATOR", True, COLORS["text"])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        
        start = self.small_font.render("Press ENTER to Start", True, COLORS["highlight"])
        screen.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
        
        exit_text = self.small_font.render("Press ESC to Exit", True, COLORS["text_dark"])
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 50))
""",
    "ui/screens/game_world.py": """import pygame
from core.scene_manager import Scene
from core.config import COLORS, WIDTH, HEIGHT

class GameWorld(Scene):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.font = pygame.font.Font(None, 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state.scene_manager.switch_to("main_menu")

    def draw(self, screen):
        screen.fill(COLORS["bg"])
        
        text = self.font.render("GAME WORLD (Press ESC to return)", True, COLORS["text"])
        screen.blit(text, (20, 20))
""",
    "ui/screens/__init__.py": "",
    "dsa/graphs/graph.py": """class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {}

    def add_edge(self, u, v, weight=1, bidirectional=True):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency_list[u][v] = weight
        if bidirectional:
            self.adjacency_list[v][u] = weight

    def get_neighbors(self, vertex):
        return self.adjacency_list.get(vertex, {})
""",
    "dsa/graphs/dijkstra.py": """import heapq

def dijkstra(graph, start, end):
    distances = {vertex: float('infinity') for vertex in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {vertex: None for vertex in graph.adjacency_list}

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue
            
        if current_vertex == end:
            break

        for neighbor, weight in graph.get_neighbors(current_vertex).items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    path, current = [], end
    while previous_nodes[current] is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    if path:
        path.insert(0, current)
        
    return path, distances[end] if distances[end] != float('infinity') else -1
""",
    "player/player.py": """class Player:
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
""",
    "world/world.py": """from dsa.graphs.graph import Graph

class World:
    def __init__(self):
        self.map_graph = Graph()
        self.locations = {}
        
    def add_location(self, name, loc_data):
        self.locations[name] = loc_data
        self.map_graph.add_vertex(name)
        
    def connect(self, loc1, loc2, cost):
        self.map_graph.add_edge(loc1, loc2, cost)
"""
}

for filepath, content in files_to_create.items():
    path = base_dir / filepath
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Core files created.")
