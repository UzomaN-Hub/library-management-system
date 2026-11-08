"""Binary min-heap used as a priority queue for loan due dates."""


class MinHeap:
    """Keeps the item with the smallest priority at the top.

    Items are stored in a Python list laid out as a complete binary tree:
    the children of index i are at 2i + 1 and 2i + 2, and its parent is
    at (i - 1) // 2. Each entry is (priority, order, value). The order
    number makes items with equal priority come out first-in, first-out.
    """

    def __init__(self):
        self._items = []
        self._counter = 0

    def push(self, priority, value):
        """Add value with the given priority. O(log n)."""
        if priority is None:
            raise ValueError("Priority cannot be None.")
        self._items.append((priority, self._counter, value))
        self._counter += 1
        self._sift_up(len(self._items) - 1)

    def pop(self):
        """Remove and return (priority, value) with the smallest priority."""
        if not self._items:
            raise IndexError("Cannot pop from an empty heap.")
        top = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._sift_down(0)
        return top[0], top[2]

    def peek(self):
        """Return (priority, value) with the smallest priority. O(1)."""
        if not self._items:
            raise IndexError("Cannot peek at an empty heap.")
        priority, _, value = self._items[0]
        return priority, value

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self._items[index] < self._items[parent]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _sift_down(self, index):
        size = len(self._items)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            if left < size and self._items[left] < self._items[smallest]:
                smallest = left
            if right < size and self._items[right] < self._items[smallest]:
                smallest = right
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def _swap(self, i, j):
        self._items[i], self._items[j] = self._items[j], self._items[i]