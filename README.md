# Forest Resource Simulator

A Python/Pygame GUI-only resource-management simulation created as a DSA-II PBL project.

## Current version

### Game
- Player creation
- Player statistics
- Day and stamina system
- Three forests
- Three wood types
- Wood cutting
- Inventory
- Selling wood
- GUI start screen and dashboard
- FIFO activity log backed by the custom Queue
- Forest travel route derived with graph BFS

### DSA foundation
The project already contains custom:
- Queue
- Graph with adjacency list
- BFS traversal

More structures and algorithms will be added progressively.

## Planned DSA integration

| Feature | DSA |
|---|---|
| Inventory | Linked List / Hash Table |
| Shop | Binary Search Tree |
| Forest map | Graph |
| Navigation | BFS / DFS / Dijkstra |
| Market | Heap / Priority Queue |
| Events | Queue |
| Skills | Tree |
| Inventory ranking | Sorting |
| Fast item lookup | Searching |
| Daily profit planning | Dynamic Programming |
| Special forest puzzles | Backtracking |

## Setup

```bash
python -m pip install -r requirements.txt
python main.py
```

The Pygame interface opens directly.

## Architecture

`Game` contains rules and state, while `gui/app.py` contains presentation and input handling. The DSA implementations are deliberately used by gameplay rather than existing only as separate examples.
