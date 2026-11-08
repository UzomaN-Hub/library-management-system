import random
from datetime import date

import pytest

from library.min_heap import MinHeap


def test_new_heap_is_empty():
    heap = MinHeap()
    assert heap.is_empty()
    assert len(heap) == 0


def test_pop_from_empty_heap_raises_error():
    with pytest.raises(IndexError):
        MinHeap().pop()


def test_peek_at_empty_heap_raises_error():
    with pytest.raises(IndexError):
        MinHeap().peek()


def test_none_priority_is_rejected():
    with pytest.raises(ValueError):
        MinHeap().push(None, "loan")


def test_earliest_due_date_comes_out_first():
    heap = MinHeap()
    heap.push(date(2026, 12, 20), "Loan C")
    heap.push(date(2026, 12, 1), "Loan A")
    heap.push(date(2026, 12, 10), "Loan B")
    assert heap.pop() == (date(2026, 12, 1), "Loan A")
    assert heap.pop() == (date(2026, 12, 10), "Loan B")
    assert heap.pop() == (date(2026, 12, 20), "Loan C")
    assert heap.is_empty()


def test_peek_does_not_remove():
    heap = MinHeap()
    heap.push(5, "five")
    heap.push(1, "one")
    assert heap.peek() == (1, "one")
    assert len(heap) == 2


def test_equal_priorities_keep_insertion_order():
    heap = MinHeap()
    heap.push(1, "first")
    heap.push(1, "second")
    heap.push(1, "third")
    assert [heap.pop()[1] for _ in range(3)] == ["first", "second", "third"]


def test_values_that_cannot_be_compared():
    heap = MinHeap()
    heap.push(1, {"isbn": "1"})
    heap.push(1, {"isbn": "2"})
    assert heap.pop() == (1, {"isbn": "1"})


def test_zero_and_negative_priorities():
    heap = MinHeap()
    for priority in [0, -5, 3, 0]:
        heap.push(priority, priority)
    assert [heap.pop()[0] for _ in range(4)] == [-5, 0, 0, 3]


def test_priorities_larger_than_64_bits():
    heap = MinHeap()
    heap.push(2 ** 100, "big")
    heap.push(2 ** 70, "smaller")
    assert heap.pop() == (2 ** 70, "smaller")


def test_large_random_input_comes_out_sorted():
    values = [random.randint(0, 1_000_000) for _ in range(100_000)]
    heap = MinHeap()
    for value in values:
        heap.push(value, value)
    result = [heap.pop()[0] for _ in range(len(values))]
    assert result == sorted(values)