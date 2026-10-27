import pygame
from core.config import COLORS
from ui.widgets.asset_loader import AssetLoader

class ModalFrame:
    def __init__(self, rect, title="Window", on_close=None):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.on_close = on_close
        self.close_btn_rect = pygame.Rect(self.rect.right - 34, self.rect.y + 8, 24, 24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_btn_rect.collidepoint(event.pos):
                if self.on_close:
                    self.on_close()
                return True
            # Consume clicks inside modal so they don't propagate to map underneath
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        loader = AssetLoader.get()
        
        # Soft Drop Shadow
        shadow_rect = self.rect.move(4, 4)
        shadow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 80))
        screen.blit(shadow_surf, shadow_rect.topleft)

        # Parchment Body
        pygame.draw.rect(screen, COLORS["parchment_light"], self.rect, border_radius=10)
        
        # Outer Wood Frame & Gold Inset
        pygame.draw.rect(screen, COLORS["wood_dark"], self.rect, width=3, border_radius=10)
        inset_rect = self.rect.inflate(-6, -6)
        pygame.draw.rect(screen, COLORS["gold_border"], inset_rect, width=1, border_radius=8)

        # Header Bar Background
        header_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.rect.width - 8, 34)
        pygame.draw.rect(screen, COLORS["wood_frame"], header_rect, border_top_left_radius=7, border_top_right_radius=7)
        pygame.draw.rect(screen, COLORS["gold_border"], header_rect, width=1, border_top_left_radius=7, border_top_right_radius=7)

        # Title Text
        title_font = loader.get_font(20, bold=True)
        title_surf = title_font.render(self.title, True, COLORS["text_light"])
        screen.blit(title_surf, (self.rect.x + 14, self.rect.y + 11))

        # Close [X] Button
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.close_btn_rect.collidepoint(mouse_pos)
        close_bg = COLORS["btn_danger_hover"] if is_hover else COLORS["btn_danger"]
        pygame.draw.rect(screen, close_bg, self.close_btn_rect, border_radius=4)
        pygame.draw.rect(screen, (220, 200, 180), self.close_btn_rect, width=1, border_radius=4)

        x_font = loader.get_font(18, bold=True)
        x_surf = x_font.render("X", True, COLORS["text_light"])
        screen.blit(x_surf, (self.close_btn_rect.centerx - x_surf.get_width()//2, 
                             self.close_btn_rect.centery - x_surf.get_height()//2))
