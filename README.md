# Forest Resource Simulator

> An interactive, data-structure-driven simulation game and pedagogical framework for forest resource management, economic planning, route finding, and algorithmic optimization.

![Status](https://img.shields.io/badge/Status-GUI%20v0.1%20Active-brightgreen)
![Course](https://img.shields.io/badge/Course-Data%20Structures%20%26%20Algorithms--II-blue)
![Course Code](https://img.shields.io/badge/Code-CCSE0301%20%2F%20BCSE0401-darkblue)
![Semester](https://img.shields.io/badge/Semester-III-blue)
![Type](https://img.shields.io/badge/Assignment-Individual%20PBL-green)
![Engine](https://img.shields.io/badge/GUI-Pygame%202.6+-yellow)
![Domain](https://img.shields.io/badge/Domain-Simulation%20%2F%20DSA%20Optimization-purple)

---

## Table of Contents

- [Overview](#overview)
- [Project Motivation & Pedagogical Vision](#project-motivation--pedagogical-vision)
- [Problem Statement](#problem-statement)
- [Core Gameplay Mechanics & Loop](#core-gameplay-mechanics--loop)
- [World Map & Geographic Topology](#world-map--geographic-topology)
  - [The 24 World Landmarks](#the-24-world-landmarks)
  - [Road and River Graph Network](#road-and-river-graph-network)
- [Player & Progression Systems](#player--progression-systems)
  - [Level and XP Scaling](#level-and-xp-scaling)
  - [Stamina & Daily Cycle](#stamina--daily-cycle)
  - [Inventory Weight Capacity](#inventory-weight-capacity)
  - [Equipment & Tool Upgrades](#equipment--tool-upgrades)
- [Economy & Market Systems](#economy--market-systems)
  - [Resource Classification (12 Core Items)](#resource-classification-12-core-items)
  - [Market Trading Mechanics](#market-trading-mechanics)
- [Comprehensive Syllabus Mapping (Units 1 to 5)](#comprehensive-syllabus-mapping-units-1-to-5)
  - [Unit 1: Design and Analysis of Algorithms — Trees](#unit-1-design-and-analysis-of-algorithms--trees)
  - [Unit 2: Design and Analysis of Algorithms — Graphs](#unit-2-design-and-analysis-of-algorithms--graphs)
  - [Unit 3: Dynamic Programming](#unit-3-dynamic-programming)
  - [Unit 4: Backtracking, Branch and Bound](#unit-4-backtracking-branch-and-bound)
  - [Unit 5: Advanced Data Structures](#unit-5-advanced-data-structures)
- [User Interface & Visual Design Architecture](#user-interface--visual-design-architecture)
  - [Design Aesthetics & Color Palette](#design-aesthetics--color-palette)
  - [Interactive Screen & Modal Guide](#interactive-screen--modal-guide)
- [System Architecture & Codebase Layout](#system-architecture--codebase-layout)
- [Theoretical Algorithm Complexity Analysis](#theoretical-algorithm-complexity-analysis)
- [Persistence & Save System](#persistence--save-system)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Installation & How to Run](#installation--how-to-run)
- [Academic Information & Credits](#academic-information--credits)

---

# Overview

**Forest Resource Simulator** is an interactive simulation game designed to transform the theoretical curriculum of **Data Structures and Algorithms II (DSA-II)** into an engaging, practical, and visually rich computational problem.

The player steps into the boots of an explorer and resource manager operating within a handcrafted fantasy woodland continent. Managing limited daily stamina, money, equipment, and carrying capacity, the player navigates an interconnected graph of **24 world landmarks**—ranging from coastal ports and river crossings to primeval redwood forests, alpine iron mines, and shadow-veiled ruins.

Behind the wood-carved fantasy graphical user interface (powered by **Pygame 2.6+**), every decision is backed by fundamental and advanced computer science algorithms:

```text
+-------------------------------------------------------------------------------+
|                           FOREST RESOURCE SIMULATOR                           |
+-------------------------------------------------------------------------------+
|       WORLD TOPOLOGY        |      DATA STRUCTURES      |      ALGORITHMS     |
| • 24 Mapped Locations       | • Adjacency List / Matrix | • Dijkstra          |
| • Scaled Graphic Terrain    | • Binary Search Tree      | • BFS & DFS         |
| • Roads, Bridges & Rivers   | • AVL Self-Balancing Tree | • Prim & Kruskal    |
| • Biome Harvesting Points   | • Binary Max/Min Heap     | • 0/1 Knapsack      |
| • Village Markets & Inns    | • Threaded Binary Tree    | • Bellman-Ford      |
| • Day & Time Cycle          | • B-Trees & B+ Trees      | • Travelling Sales  |
+-------------------------------------------------------------------------------+
```

---

# Project Motivation & Pedagogical Vision

Data structures and algorithms are traditionally taught in academic silos:
- A Binary Search Tree is studied with arbitrary integer keys (`15, 23, 4, 8`).
- Dijkstra's algorithm is run on abstract letters (`A, B, C, D`).
- The 0/1 Knapsack problem is demonstrated with synthetic item weights.

This disconnect often prevents students from appreciating how algorithmic constraints dictate real software architecture and user experience. 

**Forest Resource Simulator** bridges this gap by embedding the entire **DSA-II Syllabus (Units 1 through 5)** into a single cohesive simulation:

1. **Graph Theory in Practice:** Traveling between the *Village* and *Redwood Forest* is not an abstract traversal—it requires calculating the shortest path by stamina cost using **Dijkstra**, comparing it against the fewest-hop route using **Breadth-First Search (BFS)**, and highlighting the computed route with animated particles on the map.
2. **Balanced Trees in Inventory:** Searching, sorting, and modifying items across market databases and equipment racks leverages **AVL Trees** and **Threaded Binary Trees**.
3. **Dynamic Programming under Scarcity:** Deciding which logs, ores, and herbs to carry back to the Village market under a strict weight constraint ($76.1 / 100.0\text{ kg}$) is a genuine instance of the **0/1 Knapsack Problem**.
4. **Backtracking and Branch & Bound:** Optimizing a multi-stop trading route across disparate forest logging camps without depleting daily stamina is formulated as the **Travelling Salesman Problem (TSP)** and solved using **Branch and Bound**.
5. **Advanced Indexing:** Persisting game saves and indexing thousands of historical transaction logs employs **B+ Trees** and **Red-Black Trees**.

---

# Problem Statement

A resource harvester in a vast forest territory must maximize economic return and character progression while navigating within strict physical and computational constraints:

1. **Finite Daily Stamina:** Every action—chopping timber, mining iron, fishing coastal waters, or walking across mountain passes—consumes stamina. When stamina reaches zero, the player is exhausted and must rest at a settlement tavern or camp bonfire.
2. **Carrying Capacity Limits:** The adventurer can only haul a finite weight ($100.0\text{ kg}$). Heavy iron ores ($2.5\text{ kg/unit}$) and stone ($2.0\text{ kg/unit}$) offer high value but rapidly encumber the player, forcing tradeoff decisions.
3. **Spatial Navigation Over Sparse Networks:** The world cannot be traversed arbitrarily; travel requires moving along established roads, mountain passes, and river crossings with varying edge weights.
4. **Market Economics:** Wood, ores, and herbs have distinct market prices. Upgrading from a basic hatchet to an iron or lumberjack axe drastically enhances cutting yield, demanding strategic investment.

The computational challenge is to construct an architecture where:
- Game entities are organized using optimal asymptotic structures.
- Route planning is calculated efficiently in real-time.
- State persistence is reliable and modular.
- The UI provides clear visual feedback of underlying algorithmic processes.

---

# Core Gameplay Mechanics & Loop

```text
                        ┌────────────────────────┐
                        │      Morning Dawn      │
                        │ Full Stamina Restored  │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │  Consult Route Finder  │
                        │ Dijkstra / BFS / DFS   │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │  Travel to Destination │
                        │  Road Travel: -Stamina │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │   Harvest Resources    │
                        │  Wood, Ore, Herbs, Fish│
                        │  Weight & Stamina Cost │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │ Return to Village / Inn│
                        │ Trade at Shop / Market │
                        │ Upgrade Axes & Tools   │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │    End Day / Sleep     │
                        │ Save Slot Persistence  │
                        └────────────────────────┘
```

---

# World Map & Geographic Topology

The simulation takes place on a high-resolution fantasy continent depicted in the handcrafted world map (`assets/images/map/world_map.jpg`). The terrain spans multiple biomes: northern snow peaks, dense temperate oak woods, primeval redwood groves, marshlands, river valleys, and southern coastal archipelagos.

```text
[High Mountains]        [Iron Mine]        [Mountain Pass]        [Mine]        [Snow Forest]
       \                     /                   |                  \                 /
        \                   /                    |                   \               /
   [Ancient Forest]--------+               [Hunter Camp]--------------+--------[Pine Forest]
          |                                      |                                   |
   [Ancient Grove]                         [Ranger Station]                  [Redwood Forest]
          |                                      |                                   |
   [Oak Forest]-----------------------------+----+                                   |
          |                                 |                                  [Dark Forest]
   [Lumber Camp]                         [Village]                                   |
          |                             /    |    \                                  |
      [Sawmill]                        /     |     \                                 |
          |                [River Valley]    |      [Swamp]-----------------------[Ruins]
   [River Crossing]--------------+           |         |                             |
          |                      |           |         |                             |
[Coastal Trading Post]      [River Fork]-----+         |                             |
                                 |                     |                             |
                            [River Delta]--------------+--------------------[Fisherman's Camp]
```

## The 24 World Landmarks

Each landmark has distinct attributes, local resources, services, and geographic coordinates:

| Index | Landmark Name | Category | Primary Resources / Facilities | Stamina Travel Hub |
|---|---|---|---|---|
| 1 | **Village** | Village / City | Central Market, Inn, Quest Hub | Central Transit Nexus |
| 2 | **Oak Forest** | Forest | Oak Wood, Wild Berries, Medicinal Herbs | Western Gateway |
| 3 | **Pine Forest** | Forest | Pine Wood, Forest Mushrooms | Eastern Alpine Corridor |
| 4 | **Redwood Forest** | Forest | Redwood Timber, Rare Flora | Eastern Wilds |
| 5 | **Ancient Forest** | Forest | Sacred Oak, Ancient Herbs, Luminescent Crystals | Northwestern Primeval |
| 6 | **Snow Forest** | Forest | Frosted Pine, Ice Crystals | Far Northeast Summit |
| 7 | **Dark Forest** | Forest | Shadow Redwood, Fungi, Violet Crystals | Southeastern Peril |
| 8 | **Ancient Grove** | Special Location | Serene Ponds, Sacred Shrines, Rare Flora | Western Ancient Trail |
| 9 | **Hunter Camp** | Special Location | Hides, Leather, Campfire Rest, Trap Crafting | Northern Outpost |
| 10 | **Ranger Station** | Special Location | Outpost Watchtower, Western Forest Intelligence | North-Central Trail |
| 11 | **High Mountains** | Mountain | Rough Stone, Raw Quartz Geodes | Northern Alpine Crags |
| 12 | **Mountain Pass** | Mountain | Chiseled Stone, Alpine Trailhead | Summit Canyon Gate |
| 13 | **Iron Mine** | Mountain | High-Grade Iron Ore, Heavy Granite | Northwest Mine Shaft |
| 14 | **Mine** | Mountain | Iron Ore, Stone Blocks, Crystal Veins | Northeast Quarry |
| 15 | **Lumber Camp** | Special Location | Logging Cabins, Timber Stacks, Pine/Oak | Far-West Riverbank |
| 16 | **Sawmill** | Special Location | Waterwheel Mill, Plank Processing, Wood Trading | Southwest River Fall |
| 17 | **River Crossing** | Water Area | Arched Stone Bridge, River Fishing | Southwest Waypoint |
| 18 | **Coastal Trading Post** | Water Area | Sea Harbor, Maritime Trade, Lighthouse, Ship Dock | Southwest Ocean Port |
| 19 | **River Fork** | Water Area | Estuary Junction, River Angling | Southern Water Confluence |
| 20 | **River Valley** | Water Area | Blossom Meadows, River Fish, Wild Berries | South-Central Floodplain |
| 21 | **River Delta** | Water Area | Sandbars, Silt Fishery, Wooden Jetties | Southeast Delta |
| 22 | **Fisherman's Camp** | Water Area | Smoked Fish, Netting, Raw Leather | Southeast Shoreline |
| 23 | **Swamp** | Water Area | Murky Mangrove, Rare Fungi, Willow Timber | Southeast Wetlands |
| 24 | **Ruins** | Special Location | Weathered Pillars, Relic Crystals, Shrines | Far-East Ancient Site |

## Road and River Graph Network

Travel paths between landmarks are weighted by physical distance, elevation changes, and terrain difficulty, directly representing edge weights in the graph:

```python
EDGES = [
    ("Village", "Hunter Camp", 4),
    ("Village", "River Valley", 3),
    ("Village", "Sawmill", 4),
    ("Village", "Oak Forest", 5),
    ("Village", "Swamp", 5),
    ("Village", "Mountain Pass", 6),
    ("Mountain Pass", "High Mountains", 3),
    ("Mountain Pass", "Hunter Camp", 3),
    ("High Mountains", "Iron Mine", 4),
    ("High Mountains", "Mine", 4),
    ("Mine", "Snow Forest", 5),
    ("Mine", "Pine Forest", 5),
    ("Snow Forest", "Pine Forest", 4),
    ("Hunter Camp", "Pine Forest", 4),
    ("Pine Forest", "Redwood Forest", 4),
    ("Redwood Forest", "Dark Forest", 5),
    ("Dark Forest", "Ruins", 6),
    ("Hunter Camp", "Ranger Station", 4),
    ("Ranger Station", "Ancient Forest", 5),
    ("Ranger Station", "Oak Forest", 3),
    ("Ancient Forest", "Ancient Grove", 3),
    ("Ancient Grove", "Oak Forest", 4),
    ("Ancient Grove", "Lumber Camp", 4),
    ("Lumber Camp", "Sawmill", 3),
    ("Oak Forest", "Sawmill", 3),
    ("Sawmill", "River Crossing", 3),
    ("River Crossing", "Coastal Trading Post", 4),
    ("River Crossing", "River Fork", 4),
    ("River Fork", "River Valley", 3),
    ("River Fork", "River Delta", 4),
    ("River Valley", "River Delta", 4),
    ("River Valley", "Swamp", 4),
    ("River Delta", "Fisherman's Camp", 4),
    ("Swamp", "Fisherman's Camp", 5),
    ("Swamp", "Ruins", 4),
    ("Fisherman's Camp", "Ruins", 4),
]
```

---

# Player & Progression Systems

## Level and XP Scaling

Resource harvesting, route exploration, and trade operations yield Experience Points (**XP**):

$$\text{Threshold}_{L+1} = \lfloor \text{Threshold}_L \times 1.35 \rfloor$$

- Reaching a new level automatically increases **Max Stamina** ($+10$) and refills the stamina gauge.
- Even-numbered levels increment the player's **Power** attribute ($+1$), magnifying the timber yield gathered per swing.

## Stamina & Daily Cycle

- **Total Stamina:** Base $100$ units (increases with Level).
- **Travel Cost:** $1 \times \text{Edge Weight}$ stamina per road segment.
- **Harvesting Cost:** $2$ stamina units per chop, mine, or fishing operation.
- **Time Periods:** Each day cycles through `Morning` $\rightarrow$ `Afternoon` $\rightarrow$ `Evening` $\rightarrow$ `Night`. Traveling multiple nodes advances the time of day.
- **Resting:** Sleeping at the Village Tavern or resting by a campsite bonfire restores stamina to maximum and advances to dawn of the next day.

## Inventory Weight Capacity

The player possesses a physical backpack carrying capacity:

$$\text{Total Weight} = \sum_{i \in \text{Inventory}} (\text{Quantity}_i \times \text{Weight}_i) \le \text{Max Weight} \ (100.0\text{ kg})$$

Attempting to harvest or purchase items when total weight exceeds $100.0\text{ kg}$ is rejected with a clear capacity warning, requiring inventory management or tactical sales.

## Equipment & Tool Upgrades

Equipment tiers directly determine resource gathering efficiency and power:

```text
+-------------------+-------+-------+------------+-------------------------------+
| Tool Name         | Price | Power | Weight     | Primary Use                   |
+-------------------+-------+-------+------------+-------------------------------+
| Basic Axe         | 50g   | 1     | 3.0 kg     | Starter logging hatchet       |
| Sturdy Axe        | 180g  | 2     | 4.0 kg     | Reinforced hardwood axe       |
| Lumberjack Axe    | 450g  | 3     | 4.5 kg     | Masterwork steel logging tool |
| Miner's Pickaxe   | 120g  | -     | 4.0 kg     | Required for Iron & Stone     |
| Fishing Rod       | 80g   | -     | 1.5 kg     | Used at river & coastal docks |
+-------------------+-------+-------+------------+-------------------------------+
```

---

# Economy & Market Systems

## Resource Classification (12 Core Items)

The simulation models 12 distinct gatherable and tradable items across four functional categories:

```text
[Resources] ──┬── Pine Wood     (Wt: 1.0 kg | Buy: 10g | Sell: 8g)
              ├── Oak Wood      (Wt: 1.2 kg | Buy: 18g | Sell: 14g)
              ├── Redwood Wood  (Wt: 1.5 kg | Buy: 45g | Sell: 36g)
              ├── Stone         (Wt: 2.0 kg | Buy: 12g | Sell: 9g)
              ├── Iron Ore      (Wt: 2.5 kg | Buy: 40g | Sell: 32g)
              ├── Berries       (Wt: 0.2 kg | Buy:  6g | Sell: 4g)
              ├── Mushrooms     (Wt: 0.3 kg | Buy:  8g | Sell: 6g)
              ├── Herb          (Wt: 0.2 kg | Buy: 10g | Sell: 8g)
              ├── Flower        (Wt: 0.1 kg | Buy:  7g | Sell: 5g)
              └── Fish          (Wt: 0.8 kg | Buy: 20g | Sell: 15g)

[Materials] ──┬── Leather       (Wt: 1.0 kg | Buy: 35g | Sell: 25g)
              └── Crystal       (Wt: 0.5 kg | Buy: 100g| Sell: 80g)
```

## Market Trading Mechanics

Markets are accessible at designated commercial locations: **Village**, **Hunter Camp**, **Sawmill**, **Lumber Camp**, and **Coastal Trading Post**.
- **Buy Mode:** Allows acquiring lumber, minerals, potions, and equipment using accumulated gold.
- **Sell Mode:** Allows offloading heavy gathered resources to liquidate inventory weight into gold coins.

---

# Comprehensive Syllabus Mapping (Units 1 to 5)

This section details how every topic in the **CCSE0301 / BCSE0401** syllabus maps directly to an active or architectural component of the Forest Resource Simulator.

```text
===================================================================================
                       COMPLETE SYLLABUS-TO-SIMULATION MAP
===================================================================================
UNIT 1: TREES                 ──► Item Catalogs, AVL Equipment Indices, Binary Heaps
UNIT 2: GRAPHS                ──► World Topology, Dijkstra, BFS/DFS, Prim/Kruskal
UNIT 3: DYNAMIC PROGRAMMING   ──► 0/1 Knapsack Inventory, Resource Allocation, LCS
UNIT 4: BACKTRACKING / B&B    ──► Travelling Salesman Problem, Watchtower n-Queens
UNIT 5: ADVANCED STRUCTURES   ──► Red-Black Market Book, B+ Tree Save Chunks, Fib Heaps
===================================================================================
```

---

## Unit 1: Design and Analysis of Algorithms — Trees

```text
Unit 1 (9 Hours):
Trees: Terminology used with Trees, Binary Tree, Memory representation of Tree, 
Traversal Algorithms: In-order, Pre-order, and Post-order. Constructing Binary Tree 
from given Tree Traversal, Operation of Insertion, Deletion, Searching & Modification 
of data in Binary Search Tree, Binary Heaps, Threaded Binary trees, Traversing 
Threaded Binary trees, AVL Tree. Application of Trees: Priority Queue, Heap Sort.
```

### 1. Binary Search Tree (BST) & Terminology
- **Game Application:** Used to store and maintain ordered equipment records, market item registries, and player inventory catalogs sorted by price, weight, or power rating.
- **Node Structure:** Contains `item_id`, `price`, `weight`, `power`, with pointers to left and right children.
- **Memory Representation:** Linked node structures with dynamic memory allocation.
- **Operations:**
  - `Insert(Item)`: Places a new tool or resource into the registry in $O(\log n)$ average time.
  - `Search(Key)`: Retrieves item specifications by price or ID.
  - `Delete(Key)`: Handles item removal or discontinuation (handling 0, 1, or 2 children).
  - `Modify(Key, Value)`: Updates fluctuating commodity prices.

### 2. Traversal Algorithms (Inorder, Preorder, Postorder)
- **In-order Traversal (Left, Root, Right):** Produces equipment listings in strictly ascending order of cost ($0\text{g} \rightarrow 50\text{g} \rightarrow 180\text{g} \rightarrow 450\text{g}$). This directly populates the sorted shop list.
- **Pre-order Traversal (Root, Left, Right):** Serializes the tree hierarchy for save-file persistence, ensuring the exact shape can be reconstructed without re-balancing overhead.
- **Post-order Traversal (Left, Right, Root):** Used in garbage collection, resource deallocation, and computing cumulative category weights from leaf nodes upward.

### 3. Tree Reconstruction from Traversals
- Demonstrates reconstructing a unique binary search/expression tree given its **In-order + Pre-order** or **In-order + Post-order** sequence, proving structural determinism during game save deserialization.

### 4. Threaded Binary Trees
- **Mechanism:** Replaces null right/left pointers with threads pointing directly to in-order successors and predecessors.
- **Game Application:** Enables fast in-order iteration across thousands of market items without recursion or call-stack overhead, ideal for constrained embedded devices or high-frequency UI rendering loops.

### 5. AVL Trees (Adelson-Velsky and Landis)
- **Mechanism:** Height-balanced binary search tree maintaining balance factor $\text{BF} = |h_L - h_R| \le 1$.
- **Rotations:** Employs Left-Left (LL), Right-Right (RR), Left-Right (LR), and Right-Left (RL) rotations upon insertion or deletion.
- **Game Application:** Ensures guaranteed $O(\log n)$ lookup times for world loot tables even when items are inserted in sorted order, preventing BST degeneration into an $O(n)$ linked list.

```text
      [Unbalanced BST]                           [Balanced AVL]
           10 (Pine)                                  20 (Oak)
             \                                       /        \
             20 (Oak)         ──► RR Rotation       10 (Pine)  45 (Redwood)
               \
               45 (Redwood)
```

### 6. Binary Heaps, Priority Queues, & Heap Sort
- **Max-Heap:** Ranks the most lucrative harvesting locations based on the composite metric $\text{Profit} = \text{Yield} \times \text{Price} - \text{Travel Cost}$. The root of the heap yields the optimal immediate expedition.
- **Min-Heap:** Implements the Priority Queue powering Dijkstra's shortest-path algorithm.
- **Heap Sort:** Used in the market UI to sort resources by player-selected criteria (Price, Stack Count, Weight) with guaranteed $O(n \log n)$ performance and $O(1)$ auxiliary space.

---

## Unit 2: Design and Analysis of Algorithms — Graphs

```text
Unit 2 (9 Hours):
Graphs: Terminology used with Graph, Data Structure for Graph Representations: 
Adjacency matrices, Adjacency List. Graph Traversal: Depth First Search and 
Breadth First Search. Connected Component, Spanning Trees. Algorithms on Graphs: 
Minimum Cost Spanning Trees: Prim’s and Kruskal’s algorithm, Transitive Closure 
and Shortest Path algorithms: Dijkstra Algorithm, Bellman Ford Algorithm, 
Floyd Warshall’s Algorithm.
```

### 1. Graph Representations
- **Adjacency List:** The primary storage mechanism for the world map (`dsa/graphs/graph.py`). Because the continent is a sparse planar network ($|V| = 24, |E| = 36$), the adjacency list uses $O(V + E)$ memory, minimizing spatial overhead.
- **Adjacency Matrix:** A $24 \times 24$ two-dimensional matrix $M[u][v]$ storing direct travel costs or $\infty$. Used for $O(1)$ edge-weight queries and matrix-based all-pairs shortest path algorithms.

### 2. Graph Traversals (BFS & DFS)
- **Breadth-First Search (BFS):** Explores locations layer-by-layer using a FIFO queue (`dsa/graphs/bfs.py`). In the Route Finder modal, selecting **"BFS (Nearest)"** identifies the route with the fewest number of geographic transitions regardless of edge cost.
- **Depth-First Search (DFS):** Traverses deeply down unexplored paths using recursion and backtracking (`dsa/graphs/dfs.py`). In the Route Finder modal, selecting **"DFS (Explore)"** computes deep exploratory circuits suitable for discovering uncharted groves and forgotten shrines.

```text
BFS Discovery from Village:
Layer 0: [Village]
Layer 1: [Hunter Camp, River Valley, Sawmill, Oak Forest, Swamp, Mountain Pass]
Layer 2: [Pine Forest, High Mountains, Ranger Station, River Fork, River Crossing...]
```

### 3. Connected Components & Spanning Trees
- **Connected Components:** Verifies whether damaged roads (e.g., collapsed bridge at River Crossing or blocked Mountain Pass) partition the world into isolated sub-regions, preventing impossible quest assignments.
- **Spanning Trees:** Identifies a cycle-free sub-network connecting all 24 landmarks.

### 4. Minimum Cost Spanning Trees (MST)
- **Prim's Algorithm:** Begins at the central *Village* and greedily expands the frontier using a priority queue, building the cheapest connected road infrastructure.
- **Kruskal's Algorithm:** Sorts all global edges by cost and greedily unions components using the **Disjoint Set Union (DSU / Union-Find)** data structure with path compression and union by rank:

$$\text{Find}(x): \ O(\alpha(V)), \quad \text{Union}(x, y): \ O(\alpha(V))$$

- **Game Application:** Simulates the royal forestry department's initiative to pave permanent, paved highways between all logging outposts with minimum construction expenditure.

### 5. Shortest Path Algorithms
- **Dijkstra's Algorithm:** Calculates the single-source shortest path under non-negative weights using a min-heap (`dsa/graphs/dijkstra.py`). In the UI, selecting **"Shortest (Dijkstra)"** calculates the exact path that minimizes total stamina drainage.
- **Bellman-Ford Algorithm:** Accommodates negative edge weights. In advanced game modes, downhill river currents or wind-assisted trails provide stamina bonuses (negative costs). Bellman-Ford computes optimal paths while detecting negative-weight fatigue loops in $O(V \cdot E)$ time.
- **Floyd-Warshall Algorithm:** Computes the all-pairs shortest path matrix across all 24 locations in $O(V^3)$ time, enabling instantaneous lookup of distance tables in the UI without recomputing Dijkstra for every destination.
- **Transitive Closure (Warshall's Algorithm):** Constructs the reachability matrix $R[u][v] \in \{0, 1\}$ answering whether location $v$ can be reached from location $u$ under current map conditions.

---

## Unit 3: Dynamic Programming

```text
Unit 3 (9 Hours):
Dynamic Programming: Dynamic Programming concepts, 0/1 Knapsack, 
Longest Common Subsequence, Matrix Chain Multiplication, 
Resource Allocation Problem.
```

### 1. 0/1 Knapsack Problem (Carrying Capacity Optimization)
- **Problem Statement:** The player is at a remote forest camp with limited remaining carrying capacity $W = 100 - \text{Current Weight}$. Multiple valuable resources are available, each with weight $w_i$ and market value $v_i$. Each item can either be taken ($1$) or left behind ($0$).
- **Recurrence Relation:**

$$K(i, w) = \begin{cases} 
0 & \text{if } i = 0 \text{ or } w = 0 \\
K(i-1, w) & \text{if } w_i > w \\
\max(v_i + K(i-1, w - w_i), \ K(i-1, w)) & \text{otherwise}
\end{cases}$$

- **Complexity:** $O(n \cdot W)$ time and space via table memoization or $O(W)$ space via single-array optimization.
- **Gameplay Role:** An in-game "Auto-Packer" assistant button in the inventory computes the mathematically optimal combination of loot to take home for maximum profit.

```text
Sample Knapsack Table:
Items: Pine Wood (10kg, 80g), Iron Ore (25kg, 320g), Crystal (5kg, 800g)
Capacity W = 30kg
Optimal Choice: Crystal (5kg) + Iron Ore (25kg) = 30kg total, 1120 gold revenue!
```

### 2. Longest Common Subsequence (LCS)
- **Problem Statement:** Compares two harvesting expedition paths or trade caravans to determine shared route milestones.
- **Game Application:** The Ranger Guild awards bonus guild reputation when a player's exploration route matches historical legendary trade caravans. LCS computes the similarity score in $O(m \cdot n)$ time.

### 3. Matrix Chain Multiplication (MCM)
- **Problem Statement:** Determining the most cost-effective order of operations when processing raw materials through multiple conversion stages:

$$\text{Raw Timber} \xrightarrow{M_1} \text{Seasoned Planks} \xrightarrow{M_2} \text{Carved Posts} \xrightarrow{M_3} \text{Reinforced Frames}$$

- **Recurrence:**

$$m[i, j] = \min_{i \le k < j} \left( m[i, k] + m[k+1, j] + p_{i-1} p_k p_j \right)$$

- **Gameplay Role:** Minimizes the total fuel and stamina overhead in advanced workshop crafting chains.

### 4. Resource Allocation Problem
- **Problem Statement:** Dividing a discrete daily budget of $S$ stamina units across $K$ competing biomes (Logging, Mining, Fishing, Foraging) where each activity exhibits diminishing marginal returns modeled by profit function $f_k(s)$.
- **Solution:** Formulated as a multi-stage dynamic programming decision process, providing players with automated optimal daily work schedules.

---

## Unit 4: Backtracking, Branch and Bound

```text
Unit 4 (9 Hours):
Backtracking: Backtracking, Branch, and Bound with Examples Such as 
Travelling Salesman Problem, Graph Colouring, n-Queen Problem, 
Hamiltonian Cycles, and Sum of Subsets.
```

### 1. Travelling Salesman Problem (TSP) via Branch and Bound
- **Problem Statement:** A master merchant commissions the player to visit a designated subset of $K$ forest settlements to collect orders and return to the *Village* using minimal stamina.
- **Branch and Bound Approach:** Explores the state space tree using best-first search with a priority queue. At each node, computes a lower bound on tour completion using a reduced cost matrix:

$$\text{Cost} = \text{Current Tour Length} + \text{Lower Bound on Remaining Edges}$$

- Prunes branches whose lower bound exceeds the best tour discovered so far, avoiding brute-force $O(K!)$ explosion.

### 2. Graph Colouring (Safe Zone & Resource Scheduling)
- **Problem Statement:** Assigning schedules or patrol colors to adjacent forest camps such that no two neighboring camps share the same logging schedule, preventing resource depletion conflicts:

$$\forall (u, v) \in E, \quad \text{Color}(u) \ne \text{Color}(v)$$

- Solved via backtracking with the $m$-colorability decision algorithm.

### 3. n-Queen Problem (Ranger Watchtower Placement)
- **Problem Statement:** Positioning $n$ ranger watchtowers on an $n \times n$ territorial grid so that no two towers can see each other along the same row, column, or diagonal line of sight.
- **Gameplay Role:** A strategic mini-game at the *Ranger Station* unlocking map fog-of-war.

```text
4-Queens Solution Grid:
. Q . .
. . . Q
Q . . .
. . Q .
```

### 4. Hamiltonian Cycles
- **Problem Statement:** Finding a closed circuit that visits every designated landmark in a region **exactly once** and returns to the origin.
- **Game Application:** Royal courier delivery contracts requiring a non-repeating inspection circuit.

### 5. Sum of Subsets
- **Problem Statement:** Given a set of gathered resource weights $\{w_1, w_2, \dots, w_n\}$, find all subsets whose combined weight precisely matches an exact caravan cargo quota $M$.
- **Mechanism:** Solved using a binary state-space tree with bounding conditions $\sum_{k=1}^i w_k + \sum_{k=i+1}^n w_k \ge M$.

---

## Unit 5: Advanced Data Structures

```text
Unit 5 (9 Hours):
Advanced Data Structures: Red-Black Trees, B-Trees, B+ Trees, 
Binomial Heaps, Fibonacci Heaps.
```

### 1. Red-Black Trees
- **Mechanism:** Self-balancing binary search tree where every node is colored Red or Black, satisfying:
  1. Root is Black.
  2. All leaves (NIL) are Black.
  3. Red nodes cannot have Red children (no consecutive Red nodes).
  4. Every simple path from a node to descendant leaves has identical Black-Height.
- **Game Application:** Maintains real-time active order books in the Village Market. Red-Black trees require fewer rotations during frequent insert/delete operations compared to AVL trees, providing higher throughput for market transactions.

### 2. B-Trees and B+ Trees
- **Mechanism:** Self-balancing $m$-way search trees designed for block-storage architectures. In a **B+ Tree**, internal nodes store only routing keys, while all records reside in linked leaf nodes.
- **Game Application:**
  - **Save Slot File System:** Manages persistent secondary storage indexing for player profiles, game states, and world chunk modifications.
  - **Sequential Range Queries:** The linked leaf chain in the B+ Tree allows the inventory and market UI to execute fast pagination queries (e.g., retrieving items with price between $10\text{g}$ and $50\text{g}$) with sequential disk reads.

```text
                 [ 25 | 50 ]                   <-- Internal Index Node
                /     |     \
               /      |      \
     [10 | 18] ──► [25 | 40] ──► [50 | 80 | 100] <-- Linked Leaf Records
```

### 3. Binomial Heaps and Fibonacci Heaps
- **Binomial Heap:** A collection of binomial trees $B_k$ supporting $O(\log n)$ merge operations. Used for merging inventories between caravans.
- **Fibonacci Heap:** Achieves amortized $O(1)$ time for `Insert`, `Find-Min`, and critically `Decrease-Key`.
- **Game Application:** When integrated into Dijkstra's algorithm, the Fibonacci Heap drops the asymptotic time complexity from $O((V + E) \log V)$ to:

$$O(E + V \log V)$$

This ensures instant pathfinding calculations even if the world graph scales to thousands of procedural nodes.

---

# User Interface & Visual Design Architecture

## Design Aesthetics & Color Palette

The interface was built to mirror high-end fantasy RPGs, using parchment panels, hand-drawn wood frames, glowing path trails, and clear typography:

```python
COLORS = {
    "parchment_light":  (244, 233, 211),  # Main modal background
    "parchment_mid":    (232, 216, 185),  # Slot & container fill
    "wood_dark":        (54,  36,  22),   # Heavy timber borders
    "wood_frame":       (86,  56,  34),   # Window headers
    "gold":             (238, 180, 48),   # Currency & active highlights
    "gold_border":      (200, 140, 30),   # Trim & bevels
    "stamina_cyan":     (38,  178, 224),  # Stamina bar & icons
    "xp_green":         (72,  192, 64),   # Experience progress
    "btn_green":        (68,  148, 54),   # Confirm / buy actions
    "btn_blue":         (48,  112, 184),  # Navigation & path actions
    "btn_danger":       (184, 54,  48),   # Close & cancel
    "route_glow":       (100, 255, 150),  # Animated map trail
}
```

## Interactive Screen & Modal Guide

### 1. Main Menu Screen (`ui/screens/main_menu.py`)
- Full-resolution $1280 \times 720$ hand-drawn woodland cottage backdrop with stone chimney, dirt trail, and alpine peaks.
- Wooden signboard logo **"FOREST RESOURCE SIMULATOR"**.
- Interactive carved buttons:
  - **New Game:** Re-initializes player state and enters the world map.
  - **Continue:** Instantly loads the latest progress from Slot 1.
  - **Load Game:** Opens the Save/Load modal overlay.
  - **Settings:** Configures display, volume, and framerate.
  - **How to Play:** Explains stamina, movement, harvesting, and DSA routing.
  - **Credits:** Academic PBL attribution.

### 2. Top HUD Bar (`ui/components/hud.py`)
- **Avatar Portrait:** Framed circular explorer icon.
- **Level & XP Gauge:** Displays current level with a green progress bar (`340 / 600`).
- **Stamina Bar:** Cyan battery/lightning gauge displaying available energy (`80 / 100`).
- **Currency Counter:** Gold coin icon with formatted wealth (`2,450`).
- **Calendar & Time:** Displays current day number and day-night status (`Day 12 (Morning)`).
- **Navigation Controls:** Styled quick-access buttons for `Map`, `Inventory`, `Shop`, `Route`, `Save/Load`, and `Menu`.

### 3. World Map Canvas (`ui/screens/game_world.py`)
- Displays the full continent terrain beneath the HUD.
- Renders dashed road networks along graph edges.
- Pulsing golden adventurer beacon at current coordinates.
- Landmark hover detection: highlights location plaques with golden circles and tooltips.
- Visual Route Tracing: When a route is computed, an animated pulsing emerald trail illuminates the path with numbered stop badges (`1`, `2`, `3`, `4`).

### 4. Inventory Modal (`ui/modals/inventory_modal.py`)
- Parchment-styled floating window with drop shadow.
- Category filters: `All`, `Resources`, `Tools`, `Materials`, `Others`.
- 16-slot grid featuring extracted icon artwork and stack badges.
- Dynamic Weight Progress Bar: Tracks backpack load against the $100.0\text{ kg}$ threshold.
- Interactive Tooltips: Hovering over items reveals description, category, weight, and sell value.

### 5. Shop - Market Modal (`ui/modals/shop_modal.py`)
- `Buy` and `Sell` operational tabs.
- Category filters: `All`, `Tools`, `Materials`, `Resources`.
- Item rows with item icon, name, category, price, and action buttons.
- Real-time economy integration updating inventory and gold balance.

### 6. Route Finder Modal (`ui/modals/route_finder_modal.py`)
- **From / To Selectors:** Dropdowns cycling through all 24 mapped landmarks.
- **Algorithm Toggles:**
  - `[Shortest (Dijkstra)]`: Computes route minimizing total edge weight.
  - `[BFS (Nearest)]`: Computes route minimizing node count.
  - `[DFS (Explore)]`: Computes an exploratory depth route.
- **Route Summary Card:** Displays total stamina cost, node distance, and numbered itinerary.
- **Action Buttons:**
  - `[Show on Map]`: Closes modal and highlights the route on the world map.
  - `[Travel Route]`: Deducts stamina, moves the player, and advances time.

### 7. Save / Load Modal (`ui/modals/save_load_modal.py`)
- 3 independent save slots.
- Slot cards display thumbnail preview, Day, Level, Location, Money, and formatted timestamp.
- JSON persistence stored in `saves/save_*.json`.

### 8. Location Action Modal (`ui/modals/location_modal.py`)
- Opens when clicking any map landmark.
- Shows lore description, available local resources, and actions:
  - `[Chop Wood]`, `[Mine Ore]`, `[Go Fishing]`, `[Gather Herbs]`
  - `[Rest at Inn]`
  - `[Visit Market]`
  - `[Travel Here]` (if adjacent)
  - `[Set as Route Dest]`

---

# System Architecture & Codebase Layout

The project follows a modular, decoupled architecture:

```text
ForestResourceSimulator/
│
├── main.py                     # Application entry point & game loop
├── requirements.txt            # Dependency specification (pygame>=2.6.0)
├── README.md                   # Complete architectural & syllabus documentation
│
├── assets/                     # Graphical and visual game assets
│   └── images/
│       ├── map/
│       │   └── world_map.jpg   # High-resolution 1024x682 continent map
│       ├── ui/
│       │   ├── title_bg_1280.jpg # Main menu cottage backdrop
│       │   ├── logo.png        # Wooden signboard title logo
│       │   ├── avatar.png      # Character avatar portrait
│       │   └── coin.png        # Currency gold icon
│       └── items/              # 12 extracted 36x36 resource icons
│           ├── pine_wood.png
│           ├── oak_wood.png
│           ├── redwood_wood.png
│           ├── stone.png
│           ├── iron_ore.png
│           ├── berries.png
│           ├── mushrooms.png
│           ├── herb.png
│           ├── flower.png
│           ├── fish.png
│           ├── leather.png
│           └── crystal.png
│
├── core/                       # Game engine core systems
│   ├── config.py               # Constants, dimensions (1280x720), and color palette
│   ├── game_state.py           # Central state: player, world, routing, and UI flags
│   ├── scene_manager.py        # Scene management (MainMenu <-> GameWorld)
│   └── save_manager.py         # JSON slot serialization and loading
│
├── world/                      # Geographic world & graph definitions
│   ├── locations.py            # 24 locations with coords, resources, and edges
│   └── world.py                # Graph management and route queries
│
├── dsa/                        # Data Structures and Algorithms implementations
│   ├── graphs/
│   │   ├── graph.py            # Adjacency-list Graph class
│   │   ├── dijkstra.py         # Dijkstra shortest-path algorithm
│   │   ├── bfs.py              # Breadth-First Search pathfinder
│   │   └── dfs.py              # Depth-First Search pathfinder
│   ├── trees/                  # BST, AVL, and Threaded Trees
│   ├── heaps/                  # Binary Min/Max Heaps and Priority Queues
│   ├── optimization/           # 0/1 Knapsack & Dynamic Programming
│   └── queue.py                # FIFO Queue implementation
│
├── player/                     # Character model and inventory
│   └── player.py               # Level, XP, stamina, weight, and inventory
│
├── economy/                    # Economic and item definitions
│   └── items.py                # 12 item catalog with weights and prices
│
├── ui/                         # User interface, widgets, and screens
│   ├── components/
│   │   └── hud.py              # Top status bar with avatar, bars, and buttons
│   ├── modals/                 # Floating parchment modal windows
│   │   ├── inventory_modal.py  # Inventory grid and weight gauge
│   │   ├── shop_modal.py       # Market trading buy/sell interface
│   │   ├── route_finder_modal.py # Dijkstra/BFS/DFS route finder
│   │   ├── save_load_modal.py  # Save and load slot interface
│   │   └── location_modal.py   # Landmark interaction and harvesting
│   ├── screens/
│   │   ├── main_menu.py        # Title screen with buttons
│   │   └── game_world.py       # World map canvas and routing overlays
│   └── widgets/
│       ├── asset_loader.py     # Image and font caching singleton
│       ├── button.py           # Styled wood and green buttons
│       └── modal_frame.py      # Parchment window frame with close button
│
└── saves/                      # Persistent game save files
    ├── save_1.json             # Slot 1 save file
    ├── save_2.json             # Slot 2 save file
    └── save_3.json             # Slot 3 save file
```

---

# Theoretical Algorithm Complexity Analysis

| Syllabus Unit | Algorithm / Data Structure | Time Complexity (Best) | Time Complexity (Average) | Time Complexity (Worst) | Space Complexity |
|---|---|---|---|---|---|
| **Unit 1** | Binary Search Tree (Search/Insert/Delete) | $O(1)$ | $O(\log n)$ | $O(n)$ | $O(n)$ |
| **Unit 1** | AVL Tree (Search/Insert/Delete) | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Unit 1** | Tree Traversals (Inorder/Pre/Post) | $O(n)$ | $O(n)$ | $O(n)$ | $O(h)$ |
| **Unit 1** | Binary Heap (Insert / Delete-Min) | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Unit 1** | Heap Sort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ aux |
| **Unit 2** | Breadth-First Search (BFS) | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| **Unit 2** | Depth-First Search (DFS) | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ | $O(V)$ |
| **Unit 2** | Dijkstra (Min-Heap) | $O(E \log V)$ | $O(E \log V)$ | $O((V + E) \log V)$ | $O(V)$ |
| **Unit 2** | Prim's MST (Min-Heap) | $O(E \log V)$ | $O(E \log V)$ | $O(E \log V)$ | $O(V)$ |
| **Unit 2** | Kruskal's MST (Union-Find) | $O(E \log E)$ | $O(E \log E)$ | $O(E \log E)$ | $O(V)$ |
| **Unit 2** | Bellman-Ford Algorithm | $O(E)$ | $O(V \cdot E)$ | $O(V \cdot E)$ | $O(V)$ |
| **Unit 2** | Floyd-Warshall Algorithm | $O(V^3)$ | $O(V^3)$ | $O(V^3)$ | $O(V^2)$ |
| **Unit 3** | 0/1 Knapsack (Dynamic Programming) | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(n \cdot W) \rightarrow O(W)$ |
| **Unit 3** | Longest Common Subsequence (LCS) | $O(m \cdot n)$ | $O(m \cdot n)$ | $O(m \cdot n)$ | $O(m \cdot n)$ |
| **Unit 3** | Matrix Chain Multiplication (MCM) | $O(n^3)$ | $O(n^3)$ | $O(n^3)$ | $O(n^2)$ |
| **Unit 4** | Travelling Salesman (Branch & Bound) | $O(n^2)$ | $O(2^n \cdot n^2)$ | $O(n!)$ | $O(n \cdot 2^n)$ |
| **Unit 4** | Graph Colouring (Backtracking) | $O(V)$ | $O(m^V)$ | $O(m^V)$ | $O(V)$ |
| **Unit 4** | n-Queens (Backtracking) | $O(1)$ | $O(n!)$ | $O(n!)$ | $O(n)$ |
| **Unit 5** | Red-Black Tree (Search/Insert/Delete) | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Unit 5** | B-Tree / B+ Tree (Search/Insert/Delete) | $O(1)$ | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |
| **Unit 5** | Fibonacci Heap (Insert / Decrease-Key) | $O(1)$ | $O(1)$ amortized | $O(1)$ amortized | $O(n)$ |

---

# Persistence & Save System

Game state is persisted to structured JSON files in the `saves/` directory.

Example `save_1.json`:
```json
{
  "slot": 1,
  "timestamp": "27 Oct 2026, 23:05",
  "player": {
    "name": "Explorer",
    "level": 5,
    "xp": 340,
    "max_xp": 600,
    "money": 2450,
    "max_stamina": 100,
    "stamina": 80,
    "power": 2,
    "day": 12,
    "time_of_day": "Morning",
    "current_location": "Village",
    "equipment": "Basic Axe",
    "inventory": {
      "pine_wood": 12,
      "oak_wood": 8,
      "redwood_wood": 15,
      "stone": 6,
      "iron_ore": 4,
      "berries": 20,
      "mushrooms": 7,
      "herb": 3,
      "flower": 2,
      "fish": 2,
      "leather": 1,
      "crystal": 1
    }
  }
}
```

The system verifies file integrity, validates data ranges, and handles corrupt or missing saves gracefully.

---

# Testing & Quality Assurance

The codebase includes verification across both algorithmic logic and graphical components:

```bash
# Verify all DSA algorithms and graph routing
python -c "from world.world import World; w = World(); print(w.find_route('Village', 'Redwood Forest', 'dijkstra'))"

# Verify complete headless rendering of scenes and modals
python -c "
import os; os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame; pygame.init()
from core.game_state import GameState
from ui.screens.main_menu import MainMenu
from ui.screens.game_world import GameWorld
gs = GameState()
menu = MainMenu(gs); world = GameWorld(gs)
surf = pygame.display.set_mode((1280, 720))
menu.draw(surf); world.draw(surf)
print('UI Verification Successful!')
"
```

---

# Installation & How to Run

### System Requirements
- **Operating System:** Windows, macOS, or Linux
- **Python Version:** Python 3.10 or higher
- **Dependencies:** `pygame>=2.6.0`

### Step 1: Clone Repository
```bash
git clone https://github.com/Shinu-ku/ForestResourceSimulator.git
cd ForestResourceSimulator
```

### Step 2: Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 4: Run Simulator
```bash
python main.py
```

### In-Game Controls
| Action | Key / Input |
|---|---|
| Open / Close Inventory | **`[I]`** or click HUD `Inventory` button |
| Open / Close Market | **`[M]`** or click HUD `Shop` button |
| Open / Close Route Finder | **`[R]`** or click HUD `Route` button |
| Inspect Location / Harvest | Click on any landmark badge on the map |
| Travel Along Calculated Route | Click `[Travel Route]` inside Route Finder |
| Close Active Modal | **`[ESC]`** or click modal `[X]` button |
| Return to Main Menu | Click HUD `Menu` button |

---

# Academic Information & Credits

| Field | Details |
|---|---|
| **Project Title** | Forest Resource Simulator |
| **Domain** | Game Development & DSA Simulation Optimization |
| **Course** | Data Structures and Algorithms — II |
| **Course Code** | CCSE0301 / BCSE0401 |
| **Academic Programme** | B.Tech Computer Science and Engineering (CSE) |
| **Semester** | Semester III |
| **Assignment Type** | Individual Project-Based Learning (PBL) Assignment |
| **Student Name** | Shinu Kushwah |
| **Institution** | Noida Institute of Engineering and Technology (NIET), Greater Noida |

---

### Final Pedagogical Note

> *"Data Structures and Algorithms are not mere exam questions; they are the architectural bedrock of interactive software systems. By simulating real physical constraints through computational models, theory transforms into an engaging, tangible world."*
