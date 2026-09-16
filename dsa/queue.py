class Queue:
    """FIFO queue implemented for the DSA project."""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._items.pop(0)

    def peek(self):
        return None if self.is_empty() else self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def items(self):
        """Return a safe snapshot in FIFO order for presentation code."""
        return self._items.copy()
