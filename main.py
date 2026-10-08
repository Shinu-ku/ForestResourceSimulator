import pygame
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
