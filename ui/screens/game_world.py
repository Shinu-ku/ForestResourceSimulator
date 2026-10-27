import pygame
import math
from core.scene_manager import Scene
from core.config import WIDTH, HEIGHT, COLORS, MAP_ORIGINAL_WIDTH, MAP_ORIGINAL_HEIGHT
from ui.components.hud import HUD
from ui.widgets.asset_loader import AssetLoader
from world.locations import LOCATIONS, EDGES
from ui.modals.inventory_modal import InventoryModal
from ui.modals.shop_modal import ShopModal
from ui.modals.route_finder_modal import RouteFinderModal
from ui.modals.save_load_modal import SaveLoadModal
from ui.modals.location_modal import LocationModal

class GameWorld(Scene):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.hud = HUD(game_state)
        
        # Modals
        self.modals = {
            "inventory": InventoryModal(game_state),
            "shop": ShopModal(game_state),
            "route_finder": RouteFinderModal(game_state),
            "save_load": SaveLoadModal(game_state),
        }
        self.location_modal = None
        
        # Map Display Area
        self.map_y_offset = self.hud.height
        self.map_view_h = HEIGHT - self.map_y_offset
        self.map_view_w = WIDTH
        
        # Scaling factors from 1024x682 to 1280x666
        self.scale_x = self.map_view_w / MAP_ORIGINAL_WIDTH
        self.scale_y = self.map_view_h / MAP_ORIGINAL_HEIGHT
        
        # Pre-scale map image
        loader = AssetLoader.get()
        raw_map = loader.get_image("map/world_map.jpg")
        self.scaled_map = pygame.transform.smoothscale(raw_map, (self.map_view_w, self.map_view_h))
        
        self.hovered_node = None

    def map_to_screen(self, coord):
        """Converts original 1024x682 map coordinate to current screen space."""
        x, y = coord
        sx = int(x * self.scale_x)
        sy = int(y * self.scale_y) + self.map_y_offset
        return (sx, sy)

    def handle_events(self, events):
        gs = self.game_state

        # 1. Handle Active Modal Events first
        if gs.active_modal:
            if gs.active_modal in self.modals:
                if self.modals[gs.active_modal].handle_events(events):
                    return
            elif gs.active_modal == "location" and self.location_modal:
                if self.location_modal.handle_events(events):
                    return

        # 2. Handle HUD clicks
        if self.hud.handle_events(events):
            return

        # 3. Handle Game World Map Interaction
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if gs.active_modal:
                        gs.active_modal = None
                    else:
                        gs.scene_manager.switch_to("main_menu")
                elif event.key == pygame.K_i:
                    self.hud.on_inventory_click()
                elif event.key == pygame.K_m:
                    self.hud.on_shop_click()
                elif event.key == pygame.K_r:
                    self.hud.on_route_click()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if mouse_pos[1] > self.map_y_offset and not gs.active_modal:
                    # Check if clicked on a location badge
                    for loc_name, loc_data in LOCATIONS.items():
                        sx, sy = self.map_to_screen(loc_data["coord"])
                        dist = math.hypot(mouse_pos[0] - sx, mouse_pos[1] - sy)
                        if dist <= 32:
                            self.open_location_modal(loc_name)
                            return

    def open_location_modal(self, location_name):
        self.location_modal = LocationModal(self.game_state, location_name)
        self.game_state.active_modal = "location"

    def update(self, dt):
        self.game_state.update(dt)

        # Update hovered node
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_node = None
        if mouse_pos[1] > self.map_y_offset and not self.game_state.active_modal:
            for loc_name, loc_data in LOCATIONS.items():
                sx, sy = self.map_to_screen(loc_data["coord"])
                if math.hypot(mouse_pos[0] - sx, mouse_pos[1] - sy) <= 32:
                    self.hovered_node = (loc_name, loc_data, (sx, sy))
                    break

    def draw(self, screen):
        loader = AssetLoader.get()
        gs = self.game_state

        # 1. Draw Scaled World Map
        screen.blit(self.scaled_map, (0, self.map_y_offset))

        # 2. Draw Road Graph Edges (Dotted Paths matching map roads)
        self.draw_graph_edges(screen)

        # 3. Draw Active Route Highlights (Dijkstra / BFS / DFS)
        if gs.show_route_on_map and gs.current_route and gs.current_route["path"]:
            self.draw_highlighted_route(screen, gs.current_route["path"])

        # 4. Draw Location Highlights and Route Step Indicators
        self.draw_location_nodes(screen)

        # 5. Draw Player Position Marker
        self.draw_player_marker(screen)

        # 6. Draw Top HUD
        self.hud.draw(screen)

        # 7. Draw Active Modal if present
        if gs.active_modal:
            if gs.active_modal in self.modals:
                self.modals[gs.active_modal].draw(screen)
            elif gs.active_modal == "location" and self.location_modal:
                self.location_modal.draw(screen)

        # 8. Draw Toast Notification
        self.draw_toast(screen)

    def draw_graph_edges(self, screen):
        """Draws subtle dotted white/parchment lines along graph edges."""
        for u, v, _ in EDGES:
            p1 = self.map_to_screen(LOCATIONS[u]["coord"])
            p2 = self.map_to_screen(LOCATIONS[v]["coord"])
            self.draw_dashed_line(screen, (245, 235, 205, 110), p1, p2, width=2, dash_len=6)

    def draw_highlighted_route(self, screen, path):
        """Draws glowing pulsing animated trail along the active route."""
        if len(path) < 2:
            return

        pulse = (math.sin(pygame.time.get_ticks() * 0.006) + 1.0) / 2.0
        glow_color = (
            int(50 + 50 * pulse),
            int(220 + 35 * pulse),
            int(120 + 70 * pulse)
        )

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            p1 = self.map_to_screen(LOCATIONS[u]["coord"])
            p2 = self.map_to_screen(LOCATIONS[v]["coord"])
            
            # Outer halo
            pygame.draw.line(screen, (20, 140, 70), p1, p2, width=7)
            # Glowing core line
            pygame.draw.line(screen, glow_color, p1, p2, width=3)

    def draw_location_nodes(self, screen):
        loader = AssetLoader.get()
        font_num = loader.get_font(12, bold=True)
        font_tt = loader.get_font(13, bold=True)
        active_route_path = self.game_state.current_route["path"] if (self.game_state.show_route_on_map and self.game_state.current_route) else []

        pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1.0) / 2.0

        for name, data in LOCATIONS.items():
            sx, sy = self.map_to_screen(data["coord"])
            is_hover = (self.hovered_node and self.hovered_node[0] == name)
            is_in_route = name in active_route_path

            # If hovered: Draw an elegant glowing golden frame around the landmark badge
            if is_hover:
                glow_r = int(22 + 4 * pulse)
                pygame.draw.circle(screen, (255, 215, 60), (sx, sy), glow_r, width=2)
                
                # Floating tooltip badge above location
                tt_surf = font_tt.render(name, True, COLORS["text_light"])
                tt_w = tt_surf.get_width() + 16
                tt_h = 24
                tt_rect = pygame.Rect(sx - tt_w // 2, sy - 34, tt_w, tt_h)
                pygame.draw.rect(screen, (32, 24, 16), tt_rect, border_radius=6)
                pygame.draw.rect(screen, COLORS["gold"], tt_rect, width=1, border_radius=6)
                screen.blit(tt_surf, (tt_rect.centerx - tt_surf.get_width()//2, tt_rect.centery - tt_surf.get_height()//2))

            # If in active route: Draw a numbered glowing green milestone badge
            if is_in_route:
                step_idx = active_route_path.index(name) + 1
                badge_rect = pygame.Rect(sx - 11, sy - 11, 22, 22)
                pygame.draw.circle(screen, (40, 160, 80), (sx, sy), 11)
                pygame.draw.circle(screen, COLORS["gold_border"], (sx, sy), 11, width=1)
                num_text = font_num.render(str(step_idx), True, COLORS["text_light"])
                screen.blit(num_text, (sx - num_text.get_width()//2, sy - num_text.get_height()//2))

    def draw_player_marker(self, screen):
        p = self.game_state.player
        loc_data = LOCATIONS.get(p.current_location)
        if not loc_data:
            return

        sx, sy = self.map_to_screen(loc_data["coord"])
        pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1.0) / 2.0
        radius = int(18 + 6 * pulse)

        # Outer pulsing rings
        pygame.draw.circle(screen, (245, 215, 60), (sx, sy), radius, width=2)
        pygame.draw.circle(screen, (255, 235, 100), (sx, sy), 7)
        pygame.draw.circle(screen, (180, 50, 40), (sx, sy), 3)

    def draw_toast(self, screen):
        msg = self.game_state.toast_message
        if not msg:
            return

        loader = AssetLoader.get()
        font = loader.get_font(15, bold=True)
        text_surf = font.render(msg, True, COLORS["text_light"])
        
        pad_x, pad_y = 20, 10
        toast_w = text_surf.get_width() + pad_x * 2
        toast_h = text_surf.get_height() + pad_y * 2
        toast_x = (WIDTH - toast_w) // 2
        toast_y = HEIGHT - toast_h - 24

        toast_rect = pygame.Rect(toast_x, toast_y, toast_w, toast_h)
        toast_surf = pygame.Surface((toast_w, toast_h), pygame.SRCALPHA)
        toast_surf.fill((24, 30, 36, 235))
        screen.blit(toast_surf, (toast_x, toast_y))
        pygame.draw.rect(screen, COLORS["gold_border"], toast_rect, width=2, border_radius=6)
        screen.blit(text_surf, (toast_x + pad_x, toast_y + pad_y))

    def draw_dashed_line(self, surface, color, start_pos, end_pos, width=1, dash_len=5):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = math.hypot(x2 - x1, y2 - y1)
        if dl == 0:
            return
        dx = (x2 - x1) / dl
        dy = (y2 - y1) / dl
        
        step = dash_len * 2
        num_steps = int(dl // step)
        for i in range(num_steps):
            s_x = x1 + dx * (i * step)
            s_y = y1 + dy * (i * step)
            e_x = s_x + dx * dash_len
            e_y = s_y + dy * dash_len
            pygame.draw.line(surface, color, (s_x, s_y), (e_x, e_y), width)
