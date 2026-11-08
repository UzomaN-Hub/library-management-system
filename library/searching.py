"""Searching algorithms used to find books.

binary_search is used by the application on a list that is already sorted.
linear_search is kept as a baseline for the performance comparison.
"""


def binary_search(sorted_items, target, key=None):
    """Return the index of the first item whose key equals target, or -1.

    sorted_items must already be sorted by the same key.
    O(log n) in the average and worst case, O(1) in the best case.
    """
    if key is None:
        key = _identity
    low, high = 0, len(sorted_items) - 1
    found = -1
    while low <= high:
        middle = (low + high) // 2
        value = key(sorted_items[middle])
        if value == target:
            found = middle
            high = middle - 1  # keep looking left for the first match
        elif value < target:
            low = middle + 1
        else:
            high = middle - 1
    return found


def linear_search(items, target, key=None):
    """Return the index of the first matching item, or -1. O(n) worst case."""
    if key is None:
        key = _identity
    for index, item in enumerate(items):
        if key(item) == target:
            return index
    return -1


def _identity(value):
    return value