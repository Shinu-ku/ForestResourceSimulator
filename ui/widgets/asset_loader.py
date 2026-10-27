import os
import pygame

class AssetLoader:
    _instance = None
    
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.assets_dir = os.path.join(self.base_dir, "assets")

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = AssetLoader()
        return cls._instance

    def get_image(self, rel_path, size=None):
        key = (rel_path, size)
        if key in self.images:
            return self.images[key]
            
        full_path = os.path.join(self.assets_dir, "images", rel_path)
        if not os.path.exists(full_path):
            # Fallback placeholder surface
            w, h = size if size else (36, 36)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((100, 100, 100, 180))
            self.images[key] = surf
            return surf
            
        try:
            surf = pygame.image.load(full_path).convert_alpha()
            if size:
                surf = pygame.transform.smoothscale(surf, size)
            self.images[key] = surf
            return surf
        except Exception:
            w, h = size if size else (36, 36)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((150, 50, 50, 180))
            self.images[key] = surf
            return surf

    def get_font(self, size, bold=False):
        key = (size, bold)
        if key in self.fonts:
            return self.fonts[key]
            
        try:
            # Look for bundled ttf if available or system font
            font = pygame.font.SysFont("georgia,serif", size, bold=bold)
        except Exception:
            font = pygame.font.Font(None, size)
            
        self.fonts[key] = font
        return font
