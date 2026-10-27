import pygame
from core.config import WIDTH, COLORS
from ui.widgets.asset_loader import AssetLoader
from ui.widgets.button import Button

class HUD:
    def __init__(self, game_state):
        self.game_state = game_state
        self.height = 54
        self.rect = pygame.Rect(0, 0, WIDTH, self.height)
        
        # Action Buttons on right
        btn_y = 10
        btn_h = 34
        self.buttons = [
            Button((WIDTH - 590, btn_y, 85, btn_h), "Map", style="hud", on_click=self.on_map_click),
            Button((WIDTH - 495, btn_y, 95, btn_h), "Inventory", style="hud", on_click=self.on_inventory_click),
            Button((WIDTH - 390, btn_y, 80, btn_h), "Shop", style="hud", on_click=self.on_shop_click),
            Button((WIDTH - 300, btn_y, 90, btn_h), "Route", style="hud", on_click=self.on_route_click),
            Button((WIDTH - 200, btn_y, 95, btn_h), "Save/Load", style="hud", on_click=self.on_save_click),
            Button((WIDTH - 95, btn_y, 85, btn_h), "Menu", style="hud", on_click=self.on_menu_click),
        ]

    def on_map_click(self):
        self.game_state.active_modal = None

    def on_inventory_click(self):
        if self.game_state.active_modal == "inventory":
            self.game_state.active_modal = None
        else:
            self.game_state.active_modal = "inventory"

    def on_shop_click(self):
        if self.game_state.active_modal == "shop":
            self.game_state.active_modal = None
        else:
            self.game_state.active_modal = "shop"

    def on_route_click(self):
        if self.game_state.active_modal == "route_finder":
            self.game_state.active_modal = None
        else:
            self.game_state.active_modal = "route_finder"

    def on_save_click(self):
        if self.game_state.active_modal == "save_load":
            self.game_state.active_modal = None
        else:
            self.game_state.active_modal = "save_load"

    def on_menu_click(self):
        self.game_state.scene_manager.switch_to("main_menu")

    def handle_events(self, events):
        for event in events:
            for btn in self.buttons:
                if btn.handle_event(event):
                    return True
        return False

    def draw(self, screen):
        loader = AssetLoader.get()
        p = self.game_state.player

        # Background bar
        pygame.draw.rect(screen, COLORS["hud_bg"], self.rect)
        pygame.draw.line(screen, COLORS["gold_border"], (0, self.height), (WIDTH, self.height), 2)
        pygame.draw.line(screen, COLORS["hud_border"], (0, self.height + 1), (WIDTH, self.height + 1), 1)

        # 1. Avatar Portrait
        avatar_img = loader.get_image("ui/avatar.png", size=(40, 40))
        avatar_rect = pygame.Rect(10, 7, 40, 40)
        pygame.draw.rect(screen, COLORS["gold_border"], avatar_rect.inflate(4, 4), border_radius=6)
        screen.blit(avatar_img, avatar_rect.topleft)

        # 2. Level & XP
        font_sm = loader.get_font(16, bold=True)
        font_xs = loader.get_font(13, bold=True)
        
        lvl_text = font_sm.render(f"Lv. {p.level}", True, COLORS["text_gold"])
        screen.blit(lvl_text, (62, 10))

        # XP Bar
        xp_rect = pygame.Rect(62, 28, 90, 14)
        pygame.draw.rect(screen, (30, 40, 32), xp_rect, border_radius=3)
        xp_pct = min(1.0, max(0.0, p.xp / max(1, p.max_xp)))
        if xp_pct > 0:
            fill_w = int(xp_rect.width * xp_pct)
            pygame.draw.rect(screen, COLORS["xp_green"], (xp_rect.x, xp_rect.y, fill_w, xp_rect.height), border_radius=3)
        pygame.draw.rect(screen, (70, 90, 75), xp_rect, width=1, border_radius=3)
        
        xp_str = font_xs.render(f"{p.xp}/{p.max_xp}", True, COLORS["text_light"])
        screen.blit(xp_str, (xp_rect.centerx - xp_str.get_width()//2, xp_rect.centery - xp_str.get_height()//2 - 1))

        # 3. Stamina
        stam_label = font_xs.render("Stamina", True, COLORS["stamina_cyan"])
        screen.blit(stam_label, (168, 10))
        
        stam_rect = pygame.Rect(168, 28, 100, 14)
        pygame.draw.rect(screen, (24, 40, 50), stam_rect, border_radius=3)
        stam_pct = min(1.0, max(0.0, p.stamina / max(1, p.max_stamina)))
        if stam_pct > 0:
            fill_w = int(stam_rect.width * stam_pct)
            pygame.draw.rect(screen, COLORS["stamina_cyan"], (stam_rect.x, stam_rect.y, fill_w, stam_rect.height), border_radius=3)
        pygame.draw.rect(screen, (50, 85, 110), stam_rect, width=1, border_radius=3)

        stam_str = font_xs.render(f"{p.stamina}/{p.max_stamina}", True, COLORS["text_light"])
        screen.blit(stam_str, (stam_rect.centerx - stam_str.get_width()//2, stam_rect.centery - stam_str.get_height()//2 - 1))

        # 4. Money / Coins
        coin_icon = loader.get_image("ui/coin.png", size=(20, 20))
        screen.blit(coin_icon, (285, 17))
        money_text = font_sm.render(f"{p.money:,}", True, COLORS["gold"])
        screen.blit(money_text, (312, 18))

        # 5. Day & Time
        day_text = font_sm.render(f"Day {p.day}", True, COLORS["text_light"])
        screen.blit(day_text, (390, 18))

        time_color = COLORS["text_gold"] if p.time_of_day == "Morning" else (220, 150, 80)
        time_text = font_sm.render(f"({p.time_of_day})", True, time_color)
        screen.blit(time_text, (445, 18))

        # 6. Action Buttons
        for btn in self.buttons:
            # Highlight button if corresponding modal is open
            if ((btn.text == "Inventory" and self.game_state.active_modal == "inventory") or
                (btn.text == "Shop" and self.game_state.active_modal == "shop") or
                (btn.text == "Route" and self.game_state.active_modal == "route_finder") or
                (btn.text == "Save/Load" and self.game_state.active_modal == "save_load")):
                btn.style = "tab_active"
            else:
                btn.style = "hud"
            btn.draw(screen)
