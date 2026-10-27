import pygame
from core.config import COLORS
from ui.widgets.asset_loader import AssetLoader

class Button:
    def __init__(self, rect, text="", style="wood", icon=None, on_click=None, font_size=20, payload=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.style = style  # "wood", "green", "blue", "danger", "tab_active", "tab_inactive", "hud"
        self.icon = icon
        self.on_click = on_click
        self.font_size = font_size
        self.payload = payload
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    if self.payload is not None:
                        self.on_click(self.payload)
                    else:
                        self.on_click()
                return True
        return False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Style colors
        if self.style == "green":
            bg = COLORS["btn_green_hover"] if self.is_hovered else COLORS["btn_green"]
            border = COLORS["btn_green_border"]
            text_color = COLORS["text_light"]
        elif self.style == "blue":
            bg = COLORS["btn_blue_hover"] if self.is_hovered else COLORS["btn_blue"]
            border = (30, 80, 140)
            text_color = COLORS["text_light"]
        elif self.style == "danger":
            bg = COLORS["btn_danger_hover"] if self.is_hovered else COLORS["btn_danger"]
            border = (120, 30, 30)
            text_color = COLORS["text_light"]
        elif self.style == "tab_active":
            bg = COLORS["btn_green"]
            border = COLORS["gold_border"]
            text_color = COLORS["text_light"]
        elif self.style == "tab_inactive":
            bg = COLORS["parchment_dark"] if self.is_hovered else COLORS["parchment_mid"]
            border = COLORS["wood_dark"]
            text_color = COLORS["text_dark"]
        elif self.style == "hud":
            bg = (45, 60, 72) if self.is_hovered else (32, 42, 50)
            border = COLORS["gold_border"] if self.is_hovered else COLORS["hud_border"]
            text_color = COLORS["text_gold"] if self.is_hovered else COLORS["text_light"]
        else:  # wood
            bg = COLORS["btn_wood_hover"] if self.is_hovered else COLORS["btn_wood"]
            border = COLORS["gold_border"] if self.is_hovered else COLORS["wood_dark"]
            text_color = COLORS["text_light"]

        # Draw rounded button
        pygame.draw.rect(screen, bg, self.rect, border_radius=6)
        pygame.draw.rect(screen, border, self.rect, width=2, border_radius=6)

        loader = AssetLoader.get()
        font = loader.get_font(self.font_size, bold=True)
        
        # Calculate content layout (icon + text)
        content_width = 0
        icon_surf = None
        if self.icon:
            if isinstance(self.icon, str):
                icon_surf = loader.get_image(self.icon, size=(self.font_size + 2, self.font_size + 2))
            else:
                icon_surf = self.icon
            content_width += icon_surf.get_width() + 6

        text_surf = None
        if self.text:
            text_surf = font.render(self.text, True, text_color)
            content_width += text_surf.get_width()

        start_x = self.rect.centerx - content_width // 2

        if icon_surf:
            icon_y = self.rect.centery - icon_surf.get_height() // 2
            screen.blit(icon_surf, (start_x, icon_y))
            start_x += icon_surf.get_width() + 6

        if text_surf:
            text_y = self.rect.centery - text_surf.get_height() // 2
            screen.blit(text_surf, (start_x, text_y))
