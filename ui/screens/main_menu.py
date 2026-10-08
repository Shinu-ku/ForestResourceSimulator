import pygame
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
