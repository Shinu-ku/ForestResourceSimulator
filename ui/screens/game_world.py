import pygame
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
