import pygame
from core.config import COLORS, WIDTH, HEIGHT
from ui.widgets.modal_frame import ModalFrame
from ui.widgets.button import Button
from ui.widgets.asset_loader import AssetLoader
from economy.items import get_item_info

class InventoryModal:
    def __init__(self, game_state):
        self.game_state = game_state
        # Center modal on screen
        modal_w, modal_h = 360, 480
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGHT - modal_h) // 2 + 20
        self.frame = ModalFrame((modal_x, modal_y, modal_w, modal_h), "Inventory", on_close=self.close)
        
        # Tabs
        self.current_tab = "All"
        self.tabs = ["All", "Resources", "Tools", "Materials", "Others"]
        self.tab_buttons = []
        tab_x = modal_x + 12
        tab_y = modal_y + 44
        tab_w = 64
        for tab in self.tabs:
            self.tab_buttons.append(
                Button((tab_x, tab_y, tab_w, 24), tab, style="tab_inactive", font_size=12, on_click=self.set_tab, payload=tab)
            )
            tab_x += tab_w + 4

        self.hovered_item = None

    def close(self):
        self.game_state.active_modal = None

    def set_tab(self, tab):
        self.current_tab = tab

    def handle_events(self, events):
        for event in events:
            if self.frame.handle_event(event):
                # Check if click was on close button
                if event.type == pygame.MOUSEBUTTONDOWN and self.frame.close_btn_rect.collidepoint(event.pos):
                    return True
            for btn in self.tab_buttons:
                if btn.handle_event(event):
                    return True
        return False

    def draw(self, screen):
        loader = AssetLoader.get()
        p = self.game_state.player

        # Dim background
        backdrop = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 140))
        screen.blit(backdrop, (0, 0))

        # Modal frame
        self.frame.draw(screen)

        # Tab buttons
        for btn in self.tab_buttons:
            btn.style = "tab_active" if btn.text == self.current_tab else "tab_inactive"
            btn.draw(screen)

        # Filter items according to tab
        items_to_show = []
        for item_id, count in p.inventory.items():
            info = get_item_info(item_id)
            if self.current_tab == "All" or info.get("category") == self.current_tab:
                items_to_show.append((item_id, count, info))

        # Item Grid (4 cols, 4 rows)
        grid_start_x = self.frame.rect.x + 18
        grid_start_y = self.frame.rect.y + 78
        slot_size = 72
        slot_spacing = 8
        cols = 4

        mouse_pos = pygame.mouse.get_pos()
        self.hovered_item = None

        font_sm = loader.get_font(13, bold=True)

        for i in range(16):
            col = i % cols
            row = i // cols
            x = grid_start_x + col * (slot_size + slot_spacing)
            y = grid_start_y + row * (slot_size + slot_spacing)
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)

            is_slot_hover = slot_rect.collidepoint(mouse_pos)

            # Slot Background
            slot_bg = COLORS["parchment_mid"] if not is_slot_hover else (250, 240, 220)
            pygame.draw.rect(screen, slot_bg, slot_rect, border_radius=6)
            pygame.draw.rect(screen, COLORS["wood_dark"], slot_rect, width=1, border_radius=6)

            if i < len(items_to_show):
                item_id, count, info = items_to_show[i]
                if is_slot_hover:
                    self.hovered_item = (item_id, count, info, mouse_pos)

                # Icon
                icon_surf = loader.get_image(f"items/{info['icon']}", size=(44, 44))
                screen.blit(icon_surf, (x + (slot_size - 44)//2, y + 8))

                # Quantity badge (bottom right)
                badge_text = font_sm.render(str(count), True, COLORS["text_dark"])
                badge_bg_rect = pygame.Rect(x + slot_size - badge_text.get_width() - 8, 
                                            y + slot_size - badge_text.get_height() - 4, 
                                            badge_text.get_width() + 6, badge_text.get_height() + 2)
                pygame.draw.rect(screen, COLORS["parchment_dark"], badge_bg_rect, border_radius=3)
                pygame.draw.rect(screen, COLORS["gold_border"], badge_bg_rect, width=1, border_radius=3)
                screen.blit(badge_text, (badge_bg_rect.x + 3, badge_bg_rect.y + 1))

        # Weight Bar in Footer
        footer_y = self.frame.rect.bottom - 42
        weight_font = loader.get_font(15, bold=True)
        cur_weight = p.total_weight()
        max_weight = p.max_weight
        weight_str = f"Weight: {cur_weight} / {max_weight}"
        weight_text = weight_font.render(weight_str, True, COLORS["text_dark"])
        screen.blit(weight_text, (self.frame.rect.x + 18, footer_y))

        # Weight progress bar
        bar_rect = pygame.Rect(self.frame.rect.x + 18, footer_y + 20, self.frame.rect.width - 36, 10)
        pygame.draw.rect(screen, (200, 185, 160), bar_rect, border_radius=4)
        pct = min(1.0, cur_weight / max_weight)
        bar_color = (80, 180, 70) if pct < 0.8 else (200, 70, 60)
        pygame.draw.rect(screen, bar_color, (bar_rect.x, bar_rect.y, int(bar_rect.width * pct), bar_rect.height), border_radius=4)
        pygame.draw.rect(screen, COLORS["wood_dark"], bar_rect, width=1, border_radius=4)

        # Hover Tooltip
        if self.hovered_item:
            _, count, info, pos = self.hovered_item
            tt_font = loader.get_font(13)
            tt_title_font = loader.get_font(14, bold=True)
            
            name_surf = tt_title_font.render(info["name"], True, COLORS["gold"])
            desc_surf = tt_font.render(info["description"], True, COLORS["text_light"])
            info_surf = tt_font.render(f"Category: {info['category']} | Price: {info['sell_price']}g | Wt: {info['weight']}", True, COLORS["stamina_cyan"])
            
            tt_w = max(name_surf.get_width(), desc_surf.get_width(), info_surf.get_width()) + 20
            tt_h = 70
            tt_x = min(pos[0] + 15, WIDTH - tt_w - 10)
            tt_y = min(pos[1] + 15, HEIGHT - tt_h - 10)
            
            tt_rect = pygame.Rect(tt_x, tt_y, tt_w, tt_h)
            pygame.draw.rect(screen, (30, 36, 42), tt_rect, border_radius=6)
            pygame.draw.rect(screen, COLORS["gold_border"], tt_rect, width=1, border_radius=6)
            
            screen.blit(name_surf, (tt_x + 10, tt_y + 6))
            screen.blit(info_surf, (tt_x + 10, tt_y + 26))
            screen.blit(desc_surf, (tt_x + 10, tt_y + 46))
