import pygame
from core.config import COLORS, WIDTH, HEIGHT
from ui.widgets.modal_frame import ModalFrame
from ui.widgets.button import Button
from ui.widgets.asset_loader import AssetLoader
from world.locations import LOCATIONS

class RouteFinderModal:
    def __init__(self, game_state):
        self.game_state = game_state
        modal_w, modal_h = 440, 520
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGHT - modal_h) // 2 + 20
        self.frame = ModalFrame((modal_x, modal_y, modal_w, modal_h), "Route Finder", on_close=self.close)
        
        # Location List
        self.location_names = list(LOCATIONS.keys())
        
        # Algorithm selection buttons
        btn_y = modal_y + 130
        self.algo_buttons = [
            Button((modal_x + 16, btn_y, 130, 30), "Shortest (Dijkstra)", style="blue", font_size=12, on_click=self.set_algo, payload="dijkstra"),
            Button((modal_x + 152, btn_y, 120, 30), "BFS (Nearest)", style="tab_inactive", font_size=12, on_click=self.set_algo, payload="bfs"),
            Button((modal_x + 278, btn_y, 120, 30), "DFS (Explore)", style="tab_inactive", font_size=12, on_click=self.set_algo, payload="dfs"),
        ]
        
        # Bottom Action Buttons
        self.show_map_btn = Button((modal_x + 20, modal_y + modal_h - 48, 185, 34), "Show on Map", style="green", font_size=14, on_click=self.show_on_map)
        self.travel_btn = Button((modal_x + 225, modal_y + modal_h - 48, 185, 34), "Travel Route", style="blue", font_size=14, on_click=self.travel_route)

        # Dropdown selection state
        self.selecting_from = False
        self.selecting_to = False

    def close(self):
        self.game_state.active_modal = None

    def set_algo(self, algo):
        self.game_state.selected_algo = algo
        self.game_state.update_route()

    def show_on_map(self):
        self.game_state.show_route_on_map = True
        self.game_state.active_modal = None
        self.game_state.set_toast(f"Route highlighted on map ({self.game_state.selected_algo.upper()}).")

    def travel_route(self):
        route = self.game_state.current_route
        p = self.game_state.player
        if not route or not route["path"]:
            self.game_state.set_toast("No route available to travel.")
            return

        cost = route["total_cost"]
        if p.stamina < cost:
            self.game_state.set_toast(f"Not enough stamina! Need {cost}, have {p.stamina}.")
            return

        destination = route["path"][-1]
        p.consume_stamina(cost)
        p.current_location = destination
        p.advance_time(max(1, len(route["path"]) // 2))
        p.add_xp(cost * 5)
        
        self.game_state.from_location = destination
        self.game_state.update_route()
        self.game_state.active_modal = None
        self.game_state.set_toast(f"Arrived at {destination}! (-{cost} Stamina, +{cost*5} XP)")

    def handle_events(self, events):
        for event in events:
            if self.frame.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN and self.frame.close_btn_rect.collidepoint(event.pos):
                    return True

            for btn in self.algo_buttons:
                if btn.handle_event(event):
                    return True

            if self.show_map_btn.handle_event(event):
                return True
            if self.travel_btn.handle_event(event):
                return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                from_rect = pygame.Rect(self.frame.rect.x + 80, self.frame.rect.y + 50, 200, 30)
                to_rect = pygame.Rect(self.frame.rect.x + 80, self.frame.rect.y + 88, 200, 30)

                # Cycle from locations on click
                if from_rect.collidepoint(pos):
                    idx = (self.location_names.index(self.game_state.from_location) + 1) % len(self.location_names)
                    self.game_state.from_location = self.location_names[idx]
                    self.game_state.update_route()
                    return True

                # Cycle to locations on click
                if to_rect.collidepoint(pos):
                    idx = (self.location_names.index(self.game_state.to_location) + 1) % len(self.location_names)
                    self.game_state.to_location = self.location_names[idx]
                    self.game_state.update_route()
                    return True

        return False

    def draw(self, screen):
        loader = AssetLoader.get()
        gs = self.game_state

        # Dim background
        backdrop = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 140))
        screen.blit(backdrop, (0, 0))

        # Modal frame
        self.frame.draw(screen)

        font_label = loader.get_font(15, bold=True)
        font_value = loader.get_font(14)
        font_sm = loader.get_font(13)

        # 1. From: Field
        screen.blit(font_label.render("From:", True, COLORS["text_dark"]), (self.frame.rect.x + 20, self.frame.rect.y + 56))
        from_rect = pygame.Rect(self.frame.rect.x + 80, self.frame.rect.y + 50, self.frame.rect.width - 105, 30)
        pygame.draw.rect(screen, COLORS["parchment_mid"], from_rect, border_radius=4)
        pygame.draw.rect(screen, COLORS["wood_dark"], from_rect, width=1, border_radius=4)
        from_text = font_value.render(f"{gs.from_location} (Click to change)", True, COLORS["text_dark"])
        screen.blit(from_text, (from_rect.x + 10, from_rect.y + 6))

        # 2. To: Field
        screen.blit(font_label.render("To:", True, COLORS["text_dark"]), (self.frame.rect.x + 20, self.frame.rect.y + 94))
        to_rect = pygame.Rect(self.frame.rect.x + 80, self.frame.rect.y + 88, self.frame.rect.width - 105, 30)
        pygame.draw.rect(screen, COLORS["parchment_mid"], to_rect, border_radius=4)
        pygame.draw.rect(screen, COLORS["wood_dark"], to_rect, width=1, border_radius=4)
        to_text = font_value.render(f"{gs.to_location} (Click to change)", True, COLORS["text_dark"])
        screen.blit(to_text, (to_rect.x + 10, to_rect.y + 6))

        # 3. Algorithm Label & Buttons
        for btn in self.algo_buttons:
            btn.style = "blue" if btn.payload == gs.selected_algo else "tab_inactive"
            btn.draw(screen)

        # 4. Route Result Box (Dark card)
        card_rect = pygame.Rect(self.frame.rect.x + 16, self.frame.rect.y + 172, self.frame.rect.width - 32, 230)
        pygame.draw.rect(screen, (32, 38, 44), card_rect, border_radius=8)
        pygame.draw.rect(screen, COLORS["gold_border"], card_rect, width=1, border_radius=8)

        route = gs.current_route
        if route and route["path"]:
            cost_str = f"Route:  Total Cost: {route['total_cost']}    Distance: {route['distance']} nodes"
            cost_surf = font_label.render(cost_str, True, COLORS["text_gold"])
            screen.blit(cost_surf, (card_rect.x + 14, card_rect.y + 12))

            # Step-by-step path list
            step_y = card_rect.y + 40
            for i, step_name in enumerate(route["path"][:6]):
                # Number circle badge
                num_rect = pygame.Rect(card_rect.x + 16, step_y + 1, 20, 20)
                pygame.draw.rect(screen, (48, 120, 70), num_rect, border_radius=10)
                num_surf = font_sm.render(str(i + 1), True, COLORS["text_light"])
                screen.blit(num_surf, (num_rect.centerx - num_surf.get_width()//2, num_rect.centery - num_surf.get_height()//2))

                # Step location name
                step_surf = font_value.render(step_name, True, COLORS["text_light"])
                screen.blit(step_surf, (card_rect.x + 46, step_y + 2))
                
                step_y += 28

            if len(route["path"]) > 6:
                more_surf = font_sm.render(f"... + {len(route['path']) - 6} more stops", True, COLORS["text_dim"])
                screen.blit(more_surf, (card_rect.x + 46, step_y + 2))
        else:
            no_route = font_label.render("No valid route found.", True, (220, 100, 100))
            screen.blit(no_route, (card_rect.centerx - no_route.get_width()//2, card_rect.centery - 10))

        # Bottom Buttons
        self.show_map_btn.draw(screen)
        self.travel_btn.draw(screen)
