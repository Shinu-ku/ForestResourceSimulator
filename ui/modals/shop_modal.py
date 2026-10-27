import pygame
from core.config import COLORS, WIDTH, HEIGHT
from ui.widgets.modal_frame import ModalFrame
from ui.widgets.button import Button
from ui.widgets.asset_loader import AssetLoader
from economy.items import ITEMS_DATABASE, get_item_info

class ShopModal:
    def __init__(self, game_state):
        self.game_state = game_state
        modal_w, modal_h = 420, 500
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGHT - modal_h) // 2 + 20
        self.frame = ModalFrame((modal_x, modal_y, modal_w, modal_h), "Shop - Market", on_close=self.close)
        
        # Mode: Buy or Sell
        self.mode = "Buy"
        self.category = "All"
        
        # Top Mode Buttons
        self.buy_btn = Button((modal_x + 16, modal_y + 44, 80, 28), "Buy", style="tab_active", on_click=self.set_mode, payload="Buy")
        self.sell_btn = Button((modal_x + 100, modal_y + 44, 80, 28), "Sell", style="tab_inactive", on_click=self.set_mode, payload="Sell")
        
        # Sub-category tabs
        self.sub_tabs = ["All", "Tools", "Materials", "Resources"]
        self.cat_buttons = []
        cx = modal_x + 190
        for cat in self.sub_tabs:
            self.cat_buttons.append(
                Button((cx, modal_y + 46, 50, 24), cat, style="tab_inactive", font_size=11, on_click=self.set_category, payload=cat)
            )
            cx += 54

    def close(self):
        self.game_state.active_modal = None

    def set_mode(self, mode):
        self.mode = mode

    def set_category(self, cat):
        self.category = cat

    def handle_events(self, events):
        for event in events:
            if self.frame.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN and self.frame.close_btn_rect.collidepoint(event.pos):
                    return True
            if self.buy_btn.handle_event(event):
                return True
            if self.sell_btn.handle_event(event):
                return True
            for btn in self.cat_buttons:
                if btn.handle_event(event):
                    return True
                    
            # Item row action clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                row_items = self.get_display_items()
                start_y = self.frame.rect.y + 86
                row_h = 52
                for i, (item_id, info) in enumerate(row_items):
                    btn_rect = pygame.Rect(self.frame.rect.right - 90, start_y + i * row_h + 10, 72, 30)
                    if btn_rect.collidepoint(mouse_pos):
                        if self.mode == "Buy":
                            self.execute_buy(item_id, info)
                        else:
                            self.execute_sell(item_id, info)
                        return True
        return False

    def execute_buy(self, item_id, info):
        p = self.game_state.player
        price = info.get("buy_price", 10)
        if p.money < price:
            self.game_state.set_toast("Not enough gold!")
            return
        success, msg = p.add_item(item_id, 1)
        if success:
            p.money -= price
            self.game_state.set_toast(f"Purchased {info['name']} for {price} gold.")
        else:
            self.game_state.set_toast(msg)

    def execute_sell(self, item_id, info):
        p = self.game_state.player
        price = info.get("sell_price", 5)
        success, msg = p.remove_item(item_id, 1)
        if success:
            p.money += price
            self.game_state.set_toast(f"Sold 1 {info['name']} for +{price} gold.")
        else:
            self.game_state.set_toast("You don't have this item to sell.")

    def get_display_items(self):
        p = self.game_state.player
        items = []
        if self.mode == "Buy":
            catalog = [
                "pine_wood", "oak_wood", "redwood_wood", "stone", "iron_ore", 
                "berries", "mushrooms", "herb", "basic_axe", "sturdy_axe", "pickaxe", "fishing_rod"
            ]
            for i_id in catalog:
                info = get_item_info(i_id)
                if self.category == "All" or info.get("category") == self.category:
                    items.append((i_id, info))
        else:
            # Sell mode: only show items player owns
            for i_id in p.inventory:
                info = get_item_info(i_id)
                if self.category == "All" or info.get("category") == self.category:
                    items.append((i_id, info))
        return items

    def draw(self, screen):
        loader = AssetLoader.get()
        p = self.game_state.player

        # Dim background
        backdrop = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 140))
        screen.blit(backdrop, (0, 0))

        # Modal frame
        self.frame.draw(screen)

        # Money counter in header
        coin_icon = loader.get_image("ui/coin.png", size=(18, 18))
        screen.blit(coin_icon, (self.frame.rect.right - 145, self.frame.rect.y + 11))
        font_sm = loader.get_font(15, bold=True)
        money_surf = font_sm.render(f"{p.money:,}", True, COLORS["gold"])
        screen.blit(money_surf, (self.frame.rect.right - 124, self.frame.rect.y + 12))

        # Mode Buttons
        self.buy_btn.style = "tab_active" if self.mode == "Buy" else "tab_inactive"
        self.sell_btn.style = "tab_active" if self.mode == "Sell" else "tab_inactive"
        self.buy_btn.draw(screen)
        self.sell_btn.draw(screen)

        # Category Buttons
        for btn in self.cat_buttons:
            btn.style = "tab_active" if btn.payload == self.category else "tab_inactive"
            btn.draw(screen)

        # Item Rows
        row_items = self.get_display_items()
        start_y = self.frame.rect.y + 86
        row_h = 52
        mouse_pos = pygame.mouse.get_pos()

        font_name = loader.get_font(15, bold=True)
        font_sub = loader.get_font(12)

        for i, (item_id, info) in enumerate(row_items[:7]):
            row_y = start_y + i * row_h
            row_rect = pygame.Rect(self.frame.rect.x + 14, row_y, self.frame.rect.width - 28, row_h - 4)
            
            is_hover = row_rect.collidepoint(mouse_pos)
            bg = (248, 238, 218) if not is_hover else (255, 248, 230)
            pygame.draw.rect(screen, bg, row_rect, border_radius=6)
            pygame.draw.rect(screen, COLORS["wood_dark"], row_rect, width=1, border_radius=6)

            # Icon
            icon_surf = loader.get_image(f"items/{info['icon']}", size=(38, 38))
            screen.blit(icon_surf, (row_rect.x + 6, row_rect.y + 5))

            # Name & Category
            name_surf = font_name.render(info["name"], True, COLORS["text_dark"])
            screen.blit(name_surf, (row_rect.x + 50, row_rect.y + 8))

            owned_count = p.inventory.get(item_id, 0)
            count_str = f"Owned: {owned_count}" if self.mode == "Sell" else info["category"]
            sub_surf = font_sub.render(count_str, True, COLORS["text_mid"])
            screen.blit(sub_surf, (row_rect.x + 50, row_rect.y + 26))

            # Price
            price = info["buy_price"] if self.mode == "Buy" else info["sell_price"]
            screen.blit(coin_icon, (row_rect.right - 155, row_rect.y + 16))
            price_surf = font_sm.render(str(price), True, COLORS["text_dark"])
            screen.blit(price_surf, (row_rect.right - 132, row_rect.y + 17))

            # Action Button [Buy] or [Sell]
            btn_rect = pygame.Rect(row_rect.right - 76, row_rect.y + 8, 68, 30)
            btn_hover = btn_rect.collidepoint(mouse_pos)
            action_btn_bg = COLORS["btn_green_hover"] if btn_hover else COLORS["btn_green"]
            pygame.draw.rect(screen, action_btn_bg, btn_rect, border_radius=4)
            pygame.draw.rect(screen, COLORS["btn_green_border"], btn_rect, width=1, border_radius=4)
            
            action_label = "Buy" if self.mode == "Buy" else "Sell"
            action_surf = font_sm.render(action_label, True, COLORS["text_light"])
            screen.blit(action_surf, (btn_rect.centerx - action_surf.get_width()//2, 
                                      btn_rect.centery - action_surf.get_height()//2))

        if not row_items:
            empty_font = loader.get_font(16)
            empty_surf = empty_font.render("No items available.", True, COLORS["text_mid"])
            screen.blit(empty_surf, (self.frame.rect.centerx - empty_surf.get_width()//2, self.frame.rect.y + 180))
