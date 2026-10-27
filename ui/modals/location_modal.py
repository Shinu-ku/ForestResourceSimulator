import pygame
from core.config import COLORS, WIDTH, HEIGHT
from ui.widgets.modal_frame import ModalFrame
from ui.widgets.button import Button
from ui.widgets.asset_loader import AssetLoader
from world.locations import LOCATIONS
from economy.items import get_item_info

class LocationModal:
    def __init__(self, game_state, location_name):
        self.game_state = game_state
        self.location_name = location_name
        self.loc_data = LOCATIONS.get(location_name, {})
        
        modal_w, modal_h = 420, 440
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGHT - modal_h) // 2 + 20
        self.frame = ModalFrame((modal_x, modal_y, modal_w, modal_h), location_name, on_close=self.close)
        
        self.buttons = []
        btn_y = modal_y + modal_h - 110
        btn_w = 180
        btn_h = 36

        # Set Route Button
        self.buttons.append(
            Button((modal_x + 20, btn_y + 46, btn_w, btn_h), "Set as Route Dest", style="blue", font_size=13, on_click=self.set_destination)
        )
        
        # If at this location:
        p = game_state.player
        if p.current_location == location_name:
            # Gather / Work action
            if self.loc_data.get("gather_resources"):
                first_res = self.loc_data["gather_resources"][0]
                info = get_item_info(first_res)
                label = f"Chop {info['name']}" if "wood" in first_res else f"Gather {info['name']}"
                self.buttons.append(
                    Button((modal_x + 20, btn_y, btn_w, btn_h), label, style="green", font_size=13, on_click=self.gather_resource, payload=first_res)
                )

            # Inn / Rest
            if self.loc_data.get("has_inn"):
                self.buttons.append(
                    Button((modal_x + 215, btn_y, btn_w, btn_h), "Rest (Restore Stamina)", style="wood", font_size=13, on_click=self.rest_at_inn)
                )

            # Market
            if self.loc_data.get("has_market"):
                self.buttons.append(
                    Button((modal_x + 215, btn_y + 46, btn_w, btn_h), "Visit Market", style="green", font_size=13, on_click=self.open_market)
                )
        else:
            # Check if neighbor to travel directly
            neighbors = game_state.world.get_neighbors(p.current_location)
            if location_name in neighbors:
                cost = neighbors[location_name]
                self.buttons.append(
                    Button((modal_x + 215, btn_y + 46, btn_w, btn_h), f"Travel Here (-{cost} St)", style="green", font_size=13, on_click=self.direct_travel, payload=cost)
                )

    def close(self):
        self.game_state.active_modal = None

    def set_destination(self):
        self.game_state.to_location = self.location_name
        self.game_state.from_location = self.game_state.player.current_location
        self.game_state.update_route()
        self.game_state.active_modal = "route_finder"
        self.game_state.set_toast(f"Route set to {self.location_name}.")

    def direct_travel(self, cost):
        p = self.game_state.player
        if p.stamina < cost:
            self.game_state.set_toast(f"Need {cost} Stamina to travel!")
            return
        p.consume_stamina(cost)
        p.current_location = self.location_name
        p.advance_time(1)
        p.add_xp(cost * 5)
        self.game_state.active_modal = None
        self.game_state.set_toast(f"Traveled to {self.location_name}! (-{cost} Stamina, +{cost*5} XP)")

    def gather_resource(self, res_id):
        p = self.game_state.player
        stamina_cost = 2
        if p.stamina < stamina_cost:
            self.game_state.set_toast("Exhausted! Rest to restore stamina.")
            return

        info = get_item_info(res_id)
        qty = 2 * p.power if "wood" in res_id else 1
        success, msg = p.add_item(res_id, qty)
        if success:
            p.consume_stamina(stamina_cost)
            p.add_xp(15)
            self.game_state.set_toast(f"Harvested {qty}x {info['name']}! (+15 XP)")
        else:
            self.game_state.set_toast(msg)

    def rest_at_inn(self):
        msg = self.game_state.player.rest()
        self.game_state.set_toast(msg)

    def open_market(self):
        self.game_state.active_modal = "shop"

    def handle_events(self, events):
        for event in events:
            if self.frame.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN and self.frame.close_btn_rect.collidepoint(event.pos):
                    return True
            for btn in self.buttons:
                if btn.handle_event(event):
                    return True
        return False

    def draw(self, screen):
        loader = AssetLoader.get()
        p = self.game_state.player

        # Backdrop
        backdrop = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 140))
        screen.blit(backdrop, (0, 0))

        # Modal
        self.frame.draw(screen)

        font_cat = loader.get_font(13, bold=True)
        font_body = loader.get_font(14)
        font_bold = loader.get_font(15, bold=True)

        # Category badge
        cat_surf = font_cat.render(self.loc_data.get("category", "Landmark"), True, COLORS["gold"])
        screen.blit(cat_surf, (self.frame.rect.x + 20, self.frame.rect.y + 46))

        # Status: Are you here?
        status_text = "You are currently here" if p.current_location == self.location_name else f"Your Location: {p.current_location}"
        status_surf = font_cat.render(status_text, True, (60, 140, 70) if p.current_location == self.location_name else COLORS["text_mid"])
        screen.blit(status_surf, (self.frame.rect.right - status_surf.get_width() - 20, self.frame.rect.y + 46))

        # Divider
        pygame.draw.line(screen, COLORS["wood_dark"], 
                         (self.frame.rect.x + 20, self.frame.rect.y + 68), 
                         (self.frame.rect.right - 20, self.frame.rect.y + 68), 1)

        # Lore description (wrapped text)
        desc = self.loc_data.get("desc", "")
        desc_words = desc.split()
        lines = []
        cur_line = []
        for word in desc_words:
            test_line = " ".join(cur_line + [word])
            if font_body.size(test_line)[0] < (self.frame.rect.width - 40):
                cur_line.append(word)
            else:
                lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))

        line_y = self.frame.rect.y + 80
        for line in lines:
            screen.blit(font_body.render(line, True, COLORS["text_dark"]), (self.frame.rect.x + 20, line_y))
            line_y += 20

        # Resources Available Box
        box_rect = pygame.Rect(self.frame.rect.x + 20, line_y + 10, self.frame.rect.width - 40, 110)
        pygame.draw.rect(screen, (244, 234, 212), box_rect, border_radius=6)
        pygame.draw.rect(screen, COLORS["gold_border"], box_rect, width=1, border_radius=6)

        screen.blit(font_bold.render("Local Resources & Features:", True, COLORS["text_dark"]), (box_rect.x + 10, box_rect.y + 8))

        res_list = self.loc_data.get("gather_resources", [])
        if res_list:
            rx = box_rect.x + 12
            for res_id in res_list:
                info = get_item_info(res_id)
                icon_surf = loader.get_image(f"items/{info['icon']}", size=(34, 34))
                screen.blit(icon_surf, (rx, box_rect.y + 36))
                name_surf = font_cat.render(info["name"], True, COLORS["text_dark"])
                screen.blit(name_surf, (rx + 40, box_rect.y + 44))
                rx += 125
        else:
            features = []
            if self.loc_data.get("has_market"):
                features.append("Trading Market")
            if self.loc_data.get("has_inn"):
                features.append("Resting Tavern")
            feature_str = ", ".join(features) if features else "Tranquil Crossroads"
            screen.blit(font_body.render(feature_str, True, COLORS["text_mid"]), (box_rect.x + 12, box_rect.y + 44))

        # Buttons
        for btn in self.buttons:
            btn.draw(screen)
