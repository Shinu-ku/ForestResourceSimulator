ITEMS_DATABASE = {
    # Resources (Wood, Minerals, Foraged)
    "pine_wood": {
        "name": "Pine Wood",
        "category": "Resources",
        "buy_price": 10,
        "sell_price": 8,
        "weight": 1.0,
        "description": "Standard timber gathered from the Pine Forest.",
        "icon": "pine_wood.png"
    },
    "oak_wood": {
        "name": "Oak Wood",
        "category": "Resources",
        "buy_price": 18,
        "sell_price": 14,
        "weight": 1.2,
        "description": "Sturdy hardwood harvested in Oak Forest.",
        "icon": "oak_wood.png"
    },
    "redwood_wood": {
        "name": "Redwood Wood",
        "category": "Resources",
        "buy_price": 45,
        "sell_price": 36,
        "weight": 1.5,
        "description": "Prized ancient timber from the towering Redwood giants.",
        "icon": "redwood_wood.png"
    },
    "stone": {
        "name": "Stone",
        "category": "Resources",
        "buy_price": 12,
        "sell_price": 9,
        "weight": 2.0,
        "description": "Common rough stone mined from mountains and quarries.",
        "icon": "stone.png"
    },
    "iron_ore": {
        "name": "Iron Ore",
        "category": "Resources",
        "buy_price": 40,
        "sell_price": 32,
        "weight": 2.5,
        "description": "Dense metallic ore found in iron veins.",
        "icon": "iron_ore.png"
    },
    "berries": {
        "name": "Berries",
        "category": "Resources",
        "buy_price": 6,
        "sell_price": 4,
        "weight": 0.2,
        "description": "Sweet wild berries that restore stamina when eaten.",
        "icon": "berries.png"
    },
    "mushrooms": {
        "name": "Mushrooms",
        "category": "Resources",
        "buy_price": 8,
        "sell_price": 6,
        "weight": 0.3,
        "description": "Nutritious edible fungi gathered in damp forest floors.",
        "icon": "mushrooms.png"
    },
    "herb": {
        "name": "Herb",
        "category": "Resources",
        "buy_price": 10,
        "sell_price": 8,
        "weight": 0.2,
        "description": "Aromatic medicinal herbs used for tonics.",
        "icon": "herb.png"
    },
    "flower": {
        "name": "Flower",
        "category": "Resources",
        "buy_price": 7,
        "sell_price": 5,
        "weight": 0.1,
        "description": "Fragrant wild blossoms.",
        "icon": "flower.png"
    },
    "fish": {
        "name": "Fish",
        "category": "Resources",
        "buy_price": 20,
        "sell_price": 15,
        "weight": 0.8,
        "description": "Fresh catch from rivers and coastal fishing docks.",
        "icon": "fish.png"
    },
    "leather": {
        "name": "Leather",
        "category": "Materials",
        "buy_price": 35,
        "sell_price": 25,
        "weight": 1.0,
        "description": "Tanned hide prepared by hunters.",
        "icon": "leather.png"
    },
    "crystal": {
        "name": "Crystal",
        "category": "Materials",
        "buy_price": 100,
        "sell_price": 80,
        "weight": 0.5,
        "description": "Luminescent mineral crystal discovered in ancient ruins.",
        "icon": "crystal.png"
    },
    
    # Tools
    "basic_axe": {
        "name": "Basic Axe",
        "category": "Tools",
        "buy_price": 50,
        "sell_price": 25,
        "weight": 3.0,
        "description": "A simple iron woodcutter's hatchet (+1 Power).",
        "power": 1,
        "icon": "pine_wood.png"
    },
    "sturdy_axe": {
        "name": "Sturdy Axe",
        "category": "Tools",
        "buy_price": 180,
        "sell_price": 90,
        "weight": 4.0,
        "description": "A reinforced logging axe (+2 Power).",
        "power": 2,
        "icon": "iron_ore.png"
    },
    "lumberjack_axe": {
        "name": "Lumberjack Axe",
        "category": "Tools",
        "buy_price": 450,
        "sell_price": 225,
        "weight": 4.5,
        "description": "Masterwork steel axe forged for veteran woodcutters (+3 Power).",
        "power": 3,
        "icon": "crystal.png"
    },
    "pickaxe": {
        "name": "Miner's Pickaxe",
        "category": "Tools",
        "buy_price": 120,
        "sell_price": 60,
        "weight": 4.0,
        "description": "Tool required to mine stone and iron veins.",
        "icon": "stone.png"
    },
    "fishing_rod": {
        "name": "Fishing Rod",
        "category": "Tools",
        "buy_price": 80,
        "sell_price": 40,
        "weight": 1.5,
        "description": "Handy rod for catching river and sea fish.",
        "icon": "fish.png"
    },
}

def get_item_info(item_id):
    return ITEMS_DATABASE.get(item_id, {
        "name": item_id.replace("_", " ").title(),
        "category": "Others",
        "buy_price": 10,
        "sell_price": 5,
        "weight": 1.0,
        "description": "An adventurer's item.",
        "icon": "pine_wood.png"
    })
