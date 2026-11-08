import pytest

from library.queue import Queue


def test_new_queue_is_empty():
    queue = Queue()
    assert queue.is_empty()
    assert len(queue) == 0
    assert list(queue) == []


def test_dequeue_from_empty_queue_raises_error():
    with pytest.raises(IndexError):
        Queue().dequeue()


def test_peek_at_empty_queue_raises_error():
    with pytest.raises(IndexError):
        Queue().peek()


def test_none_is_rejected():
    with pytest.raises(ValueError):
        Queue().enqueue(None)


def test_first_in_first_out_order():
    queue = Queue()
    for member in ["M001", "M002", "M003"]:
        queue.enqueue(member)
    assert queue.dequeue() == "M001"
    assert queue.dequeue() == "M002"
    assert queue.dequeue() == "M003"
    assert queue.is_empty()


def test_peek_does_not_remove():
    queue = Queue()
    queue.enqueue("M001")
    assert queue.peek() == "M001"
    assert len(queue) == 1


def test_queue_can_be_reused_after_emptying():
    queue = Queue()
    queue.enqueue("M001")
    queue.dequeue()
    queue.enqueue("M002")
    assert queue.peek() == "M002"
    assert len(queue) == 1


def test_zero_value_is_allowed():
    queue = Queue()
    queue.enqueue(0)
    assert queue.dequeue() == 0


def test_integer_larger_than_64_bits():
    queue = Queue()
    queue.enqueue(2 ** 100)
    assert queue.dequeue() == 2 ** 100


def test_contains():
    queue = Queue()
    queue.enqueue("M001")
    assert "M001" in queue
    assert "M999" not in queue


def test_one_million_items():
    queue = Queue()
    for number in range(1_000_000):
        queue.enqueue(number)
    assert len(queue) == 1_000_000
    assert queue.dequeue() == 0
    assert queue.peek() == 1