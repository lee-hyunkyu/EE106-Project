class PriorityQueue:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items += [item]
        self.heapify()

    def pop(self):
        return self._items.pop(0)

    def heapify(self):
        self._items = sorted(self._items)

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)