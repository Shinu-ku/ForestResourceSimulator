import pygame
import os

WIDTH = 1280
HEIGHT = 720
FPS = 60

# World Map Original Dimensions
MAP_ORIGINAL_WIDTH = 1024
MAP_ORIGINAL_HEIGHT = 682

# Theme Color Palette based on Fantasy Wood & Parchment UI
COLORS = {
    # Backgrounds & Overlays
    "bg_dark": (18, 22, 24),
    "hud_bg": (24, 32, 38),
    "hud_border": (46, 60, 70),
    "hud_sep": (40, 52, 60),
    "modal_backdrop": (10, 14, 16, 175),
    
    # Parchment & Wood Frames
    "parchment_light": (244, 233, 211),
    "parchment_mid": (232, 216, 185),
    "parchment_dark": (212, 192, 155),
    "wood_dark": (54, 36, 22),
    "wood_frame": (86, 56, 34),
    "wood_light": (128, 88, 56),
    "wood_hover": (106, 72, 44),
    
    # UI Elements & Badges
    "gold": (238, 180, 48),
    "gold_border": (200, 140, 30),
    "stamina_cyan": (38, 178, 224),
    "xp_green": (72, 192, 64),
    "xp_bg": (32, 64, 36),
    
    # Buttons
    "btn_green": (68, 148, 54),
    "btn_green_hover": (84, 176, 66),
    "btn_green_border": (48, 108, 38),
    "btn_blue": (48, 112, 184),
    "btn_blue_hover": (64, 136, 216),
    "btn_wood": (86, 56, 34),
    "btn_wood_hover": (112, 76, 48),
    "btn_danger": (184, 54, 48),
    "btn_danger_hover": (216, 68, 60),
    
    # Text
    "text_dark": (48, 32, 20),
    "text_mid": (90, 70, 50),
    "text_light": (245, 240, 230),
    "text_dim": (170, 175, 180),
    "text_gold": (245, 205, 80),
    
    # Map & Route Elements
    "route_line": (240, 220, 150),
    "route_highlight": (80, 230, 120),
    "route_glow": (100, 255, 150),
    "node_badge_bg": (52, 38, 26),
    "node_badge_border": (210, 165, 85),
    "node_badge_text": (245, 235, 215),
    "player_marker": (245, 215, 60),
}
