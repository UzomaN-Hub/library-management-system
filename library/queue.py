"""First-in, first-out queue built on a singly linked list."""


class _Node:
    """One item in the queue, linked to the item behind it."""

    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    """FIFO queue used for book reservations.

    enqueue adds to the back and dequeue removes from the front.
    Both are O(1) because the queue keeps a pointer to each end.
    """

    def __init__(self):
        self._front = None
        self._back = None
        self._size = 0

    def enqueue(self, value):
        """Add value to the back of the queue."""
        if value is None:
            raise ValueError("Cannot add None to the queue.")
        node = _Node(value)
        if self._back is None:
            self._front = node
        else:
            self._back.next = node
        self._back = node
        self._size += 1

    def dequeue(self):
        """Remove and return the value at the front of the queue."""
        if self._front is None:
            raise IndexError("Cannot dequeue from an empty queue.")
        node = self._front
        self._front = node.next
        if self._front is None:
            self._back = None
        self._size -= 1
        return node.value

    def peek(self):
        """Return the value at the front without removing it."""
        if self._front is None:
            raise IndexError("Cannot peek at an empty queue.")
        return self._front.value

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self._front
        while node is not None:
            yield node.value
            node = node.next

    def __contains__(self, value):
        return any(item == value for item in self)