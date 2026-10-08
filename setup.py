import os
from pathlib import Path

base_dir = Path(r"d:\programming\Projects\ForestResourceSimulator")

dirs = [
    "core",
    "world",
    "player",
    "resources",
    "economy",
    "quests",
    "npcs",
    "crafting",
    "ui/screens",
    "ui/components",
    "ui/widgets",
    "data",
    "saves",
    "tests",
    "dsa/trees",
    "dsa/heaps",
    "dsa/graphs",
    "dsa/sorting",
    "dsa/optimization",
    "assets/images/player",
    "assets/images/trees",
    "assets/images/forests",
    "assets/images/buildings",
    "assets/images/npcs",
    "assets/images/resources",
    "assets/images/items",
    "assets/images/map",
    "assets/images/ui",
    "assets/audio/music",
    "assets/audio/ambience",
    "assets/audio/sfx",
    "assets/audio/ui",
    "assets/fonts"
]

for d in dirs:
    (base_dir / d).mkdir(parents=True, exist_ok=True)
    init_file = base_dir / d.split('/')[0] / "__init__.py"
    if not init_file.exists():
        init_file.touch()

print("Directories created successfully.")
