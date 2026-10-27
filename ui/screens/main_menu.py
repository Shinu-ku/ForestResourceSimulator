import pygame
from core.scene_manager import Scene
from core.config import WIDTH, HEIGHT, COLORS
from ui.widgets.button import Button
from ui.widgets.asset_loader import AssetLoader
from ui.widgets.modal_frame import ModalFrame

class MainMenu(Scene):
    def __init__(self, game_state):
        super().__init__(game_state)
        loader = AssetLoader.get()
        self.bg_img = loader.get_image("ui/title_bg_1280.jpg", size=(WIDTH, HEIGHT))
        self.logo_img = loader.get_image("ui/logo.png", size=(340, 170))

        # Buttons position (on left side like in Image 2)
        start_x = 90
        start_y = 240
        btn_w = 230
        btn_h = 44
        gap = 14

        self.buttons = [
            Button((start_x, start_y, btn_w, btn_h), "New Game", style="green", font_size=18, on_click=self.on_new_game),
            Button((start_x, start_y + (btn_h + gap), btn_w, btn_h), "Continue", style="wood", font_size=18, on_click=self.on_continue),
            Button((start_x, start_y + (btn_h + gap) * 2, btn_w, btn_h), "Load Game", style="wood", font_size=18, on_click=self.on_load_game),
            Button((start_x, start_y + (btn_h + gap) * 3, btn_w, btn_h), "Settings", style="wood", font_size=18, on_click=self.on_settings),
            Button((start_x, start_y + (btn_h + gap) * 4, btn_w, btn_h), "How to Play", style="wood", font_size=18, on_click=self.on_how_to_play),
            Button((start_x, start_y + (btn_h + gap) * 5, btn_w, btn_h), "Credits", style="wood", font_size=18, on_click=self.on_credits),
        ]

        self.overlay_modal = None

    def on_new_game(self):
        self.game_state.start_new_game("Explorer")
        self.game_state.scene_manager.switch_to("game_world")

    def on_continue(self):
        loaded = self.game_state.save_manager.load_slot(1)
        if loaded:
            self.game_state.player = loaded
            self.game_state.from_location = loaded.current_location
            self.game_state.update_route()
            self.game_state.set_toast("Game resumed from Slot 1!")
        self.game_state.scene_manager.switch_to("game_world")

    def on_load_game(self):
        self.game_state.active_modal = "save_load"
        self.game_state.scene_manager.switch_to("game_world")

    def on_settings(self):
        self.overlay_modal = "settings"

    def on_how_to_play(self):
        self.overlay_modal = "how_to_play"

    def on_credits(self):
        self.overlay_modal = "credits"

    def handle_events(self, events):
        for event in events:
            if self.overlay_modal:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Click outside or on close to dismiss
                    self.overlay_modal = None
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.overlay_modal = None
                    return
                continue

            for btn in self.buttons:
                if btn.handle_event(event):
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.on_new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state.running = False

    def draw(self, screen):
        loader = AssetLoader.get()

        # 1. Background image
        screen.blit(self.bg_img, (0, 0))

        # Subtle dark vignette over left menu area for readability
        vignette = pygame.Surface((440, HEIGHT), pygame.SRCALPHA)
        vignette.fill((10, 16, 12, 100))
        screen.blit(vignette, (0, 0))

        # 2. Wooden Logo Signboard
        screen.blit(self.logo_img, (35, 45))

        # 3. Menu Buttons
        for btn in self.buttons:
            btn.draw(screen)

        # 4. Version indicator
        font_xs = loader.get_font(14)
        ver_text = font_xs.render("v0.1  |  DSA-II PBL individual project", True, (240, 240, 230))
        screen.blit(ver_text, (20, HEIGHT - 30))

        # 5. Overlay modal (How to Play / Credits / Settings)
        if self.overlay_modal:
            self.draw_overlay_modal(screen)

    def draw_overlay_modal(self, screen):
        loader = AssetLoader.get()
        backdrop = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 160))
        screen.blit(backdrop, (0, 0))

        modal_w, modal_h = 560, 420
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGHT - modal_h) // 2
        frame = ModalFrame((modal_x, modal_y, modal_w, modal_h), self.overlay_modal.replace("_", " ").title())
        frame.draw(screen)

        font_body = loader.get_font(15)
        font_bold = loader.get_font(16, bold=True)
        line_y = modal_y + 55

        if self.overlay_modal == "how_to_play":
            lines = [
                ("1. World Exploration:", "Click any location on the map to inspect its resources or travel directly."),
                ("2. DSA Route Finder:", "Use Dijkstra, BFS, or DFS to calculate optimal stamina paths between forests."),
                ("3. Resource Gathering:", "Chop Pine, Oak, and Redwood trees; mine ores and collect herbs."),
                ("4. Economy & Trading:", "Visit the Village Market to trade gathered lumber and ores for gold."),
                ("5. Stamina & Rest:", "Rest at Inns or Hunter Camp to recover stamina and begin a new day."),
                ("6. Shortcuts:", "[I] Inventory  |  [M] Market / Shop  |  [R] Route Finder  |  [ESC] Close")
            ]
            for header, text in lines:
                h_surf = font_bold.render(header, True, COLORS["gold"])
                screen.blit(h_surf, (modal_x + 24, line_y))
                t_surf = font_body.render(text, True, COLORS["text_dark"])
                screen.blit(t_surf, (modal_x + 24, line_y + 22))
                line_y += 50

        elif self.overlay_modal == "credits":
            lines = [
                ("Project:", "Forest Resource Simulator"),
                ("Course:", "Data Structures & Algorithms - II (CCSE0301)"),
                ("Topics Implemented:", "Graph Theory, Dijkstra, BFS, DFS, Heaps, Priority Queues"),
                ("Framework:", "Python 3 + Pygame 2.6"),
                ("Art & Assets:", "Custom Fantasy World Map & Wood-carved UI"),
            ]
            for header, text in lines:
                h_surf = font_bold.render(header, True, COLORS["gold"])
                screen.blit(h_surf, (modal_x + 24, line_y))
                t_surf = font_body.render(text, True, COLORS["text_dark"])
                screen.blit(t_surf, (modal_x + 24, line_y + 22))
                line_y += 50

        elif self.overlay_modal == "settings":
            s_surf = font_bold.render("Display & Audio Settings", True, COLORS["gold"])
            screen.blit(s_surf, (modal_x + 24, line_y))
            line_y += 35
            opts = [
                "Resolution: 1280 x 720 (Standard HD)",
                "Framerate: 60 FPS VSync",
                "UI Theme: Fantasy Wood & Parchment",
                "Sound Effects: Enabled",
                "Music Volume: 80%"
            ]
            for opt in opts:
                o_surf = font_body.render(opt, True, COLORS["text_dark"])
                screen.blit(o_surf, (modal_x + 24, line_y))
                line_y += 32
