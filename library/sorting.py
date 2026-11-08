"""Sorting algorithms used to order books.

merge_sort is used by the application. bubble_sort is kept only as a
baseline so the two can be compared in the performance tests.
"""


def merge_sort(items, key=None):
    """Return a new list sorted in ascending order. O(n log n) in all cases.

    key is an optional function that picks the value to sort by,
    for example key=lambda book: book.title.lower().
    The sort is stable: items with equal keys keep their original order.
    """
    if key is None:
        key = _identity
    items = list(items)
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle], key)
    right = merge_sort(items[middle:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def bubble_sort(items, key=None):
    """Return a new sorted list. O(n^2) average and worst, O(n) best case."""
    if key is None:
        key = _identity
    items = list(items)
    n = len(items)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if key(items[i]) > key(items[i + 1]):
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break
    return items


def _identity(value):
    return value