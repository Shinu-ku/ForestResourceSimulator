import pygame

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
