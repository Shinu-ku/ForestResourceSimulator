import os
import json
from datetime import datetime
from player.player import Player

SAVES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")

class SaveManager:
    def __init__(self):
        os.makedirs(SAVES_DIR, exist_ok=True)

    def get_slot_path(self, slot_num):
        return os.path.join(SAVES_DIR, f"save_{slot_num}.json")

    def get_slot_info(self, slot_num):
        path = self.get_slot_path(slot_num)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception:
            return None

    def save_slot(self, slot_num, player):
        path = self.get_slot_path(slot_num)
        slot_data = {
            "slot": slot_num,
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
            "player": player.to_dict()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(slot_data, f, indent=2)
        return True

    def load_slot(self, slot_num):
        data = self.get_slot_info(slot_num)
        if not data or "player" not in data:
            return None
        return Player.from_dict(data["player"])
