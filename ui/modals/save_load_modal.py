import pygame
from core.config import COLORS, WIDTH, HEIGHT
from ui.widgets.modal_frame import ModalFrame
from ui.widgets.button import Button
from ui.widgets.asset_loader import AssetLoader

class SaveLoadModal:
    def __init__(self, game_state):
        self.game_state = game_state
        modal_w, modal_h = 440, 480
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGHT - modal_h) // 2 + 20
        self.frame = ModalFrame((modal_x, modal_y, modal_w, modal_h), "Save / Load", on_close=self.close)
        
        self.mode = "Save"  # "Save" or "Load"
        self.save_tab_btn = Button((modal_x + 16, modal_y + 44, 195, 30), "Save Game", style="tab_active", on_click=self.set_mode, payload="Save")
        self.load_tab_btn = Button((modal_x + 225, modal_y + 44, 195, 30), "Load Game", style="tab_inactive", on_click=self.set_mode, payload="Load")

    def close(self):
        self.game_state.active_modal = None

    def set_mode(self, mode):
        self.mode = mode

    def handle_events(self, events):
        for event in events:
            if self.frame.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN and self.frame.close_btn_rect.collidepoint(event.pos):
                    return True
            if self.save_tab_btn.handle_event(event):
                return True
            if self.load_tab_btn.handle_event(event):
                return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                start_y = self.frame.rect.y + 88
                slot_h = 110
                for slot_num in range(1, 4):
                    btn_rect = pygame.Rect(self.frame.rect.right - 95, start_y + (slot_num - 1) * (slot_h + 10) + 38, 75, 32)
                    if btn_rect.collidepoint(mouse_pos):
                        if self.mode == "Save":
                            self.game_state.save_manager.save_slot(slot_num, self.game_state.player)
                            self.game_state.set_toast(f"Game saved to Slot {slot_num}!")
                        else:
                            loaded_player = self.game_state.save_manager.load_slot(slot_num)
                            if loaded_player:
                                self.game_state.player = loaded_player
                                self.game_state.from_location = loaded_player.current_location
                                self.game_state.update_route()
                                self.game_state.active_modal = None
                                self.game_state.set_toast(f"Slot {slot_num} loaded successfully!")
                            else:
                                self.game_state.set_toast("Slot is empty.")
                        return True
        return False

    def draw(self, screen):
        loader = AssetLoader.get()
        sm = self.game_state.save_manager

        # Dim background
        backdrop = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 140))
        screen.blit(backdrop, (0, 0))

        # Modal frame
        self.frame.draw(screen)

        # Tabs
        self.save_tab_btn.style = "tab_active" if self.mode == "Save" else "tab_inactive"
        self.load_tab_btn.style = "tab_active" if self.mode == "Load" else "tab_inactive"
        self.save_tab_btn.draw(screen)
        self.load_tab_btn.draw(screen)

        # 3 Save Slots
        start_y = self.frame.rect.y + 88
        slot_h = 110
        mouse_pos = pygame.mouse.get_pos()

        font_title = loader.get_font(15, bold=True)
        font_sub = loader.get_font(13)
        font_xs = loader.get_font(11)

        for slot_num in range(1, 4):
            slot_y = start_y + (slot_num - 1) * (slot_h + 10)
            slot_rect = pygame.Rect(self.frame.rect.x + 14, slot_y, self.frame.rect.width - 28, slot_h)
            
            is_hover = slot_rect.collidepoint(mouse_pos)
            bg = (248, 238, 218) if not is_hover else (255, 248, 230)
            pygame.draw.rect(screen, bg, slot_rect, border_radius=6)
            pygame.draw.rect(screen, COLORS["wood_dark"], slot_rect, width=1, border_radius=6)

            info = sm.get_slot_info(slot_num)

            # Thumbnail
            thumb_rect = pygame.Rect(slot_rect.x + 8, slot_rect.y + 8, 95, 94)
            thumb_img = loader.get_image("ui/main_menu_bg.jpg", size=(95, 94))
            screen.blit(thumb_img, thumb_rect.topleft)
            pygame.draw.rect(screen, COLORS["gold_border"], thumb_rect, width=1, border_radius=4)

            # Metadata
            text_x = slot_rect.x + 112
            if info and "player" in info:
                p_data = info["player"]
                title_surf = font_title.render(f"Save {slot_num}", True, COLORS["text_dark"])
                screen.blit(title_surf, (text_x, slot_rect.y + 10))

                sub1_surf = font_sub.render(f"Day {p_data.get('day', 1)} | Lv. {p_data.get('level', 1)}", True, COLORS["text_mid"])
                screen.blit(sub1_surf, (text_x, slot_rect.y + 32))

                sub2_surf = font_sub.render(f"Location: {p_data.get('current_location', 'Village')}", True, COLORS["text_dark"])
                screen.blit(sub2_surf, (text_x, slot_rect.y + 52))

                sub3_surf = font_sub.render(f"Money: {p_data.get('money', 0):,} gold", True, COLORS["gold"])
                screen.blit(sub3_surf, (text_x, slot_rect.y + 70))

                time_surf = font_xs.render(info.get("timestamp", ""), True, COLORS["text_dim"])
                screen.blit(time_surf, (text_x, slot_rect.y + 90))

                btn_label = "Save" if self.mode == "Save" else "Load"
                btn_color = COLORS["btn_green"]
            else:
                title_surf = font_title.render(f"Save {slot_num}", True, COLORS["text_dark"])
                screen.blit(title_surf, (text_x, slot_rect.y + 20))
                empty_surf = font_sub.render("Empty Slot", True, COLORS["text_dim"])
                screen.blit(empty_surf, (text_x, slot_rect.y + 45))

                btn_label = "Save Here" if self.mode == "Save" else "Empty"
                btn_color = COLORS["btn_blue"] if self.mode == "Save" else (120, 120, 120)

            # Action Button
            action_btn_rect = pygame.Rect(slot_rect.right - 88, slot_rect.y + 38, 78, 32)
            btn_hover = action_btn_rect.collidepoint(mouse_pos)
            btn_bg = COLORS["btn_green_hover"] if (btn_hover and btn_label != "Empty") else btn_color
            pygame.draw.rect(screen, btn_bg, action_btn_rect, border_radius=4)
            pygame.draw.rect(screen, COLORS["gold_border"], action_btn_rect, width=1, border_radius=4)

            btn_surf = font_title.render(btn_label, True, COLORS["text_light"])
            screen.blit(btn_surf, (action_btn_rect.centerx - btn_surf.get_width()//2, 
                                   action_btn_rect.centery - btn_surf.get_height()//2))
