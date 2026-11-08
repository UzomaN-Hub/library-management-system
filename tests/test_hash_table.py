import pytest

from library.hash_table import HashTable


def test_empty_table():
    table = HashTable()
    assert len(table) == 0
    assert table.get("9780262046305") is None
    assert "9780262046305" not in table
    assert table.keys() == []


def test_put_and_get():
    table = HashTable()
    table.put("9780262046305", "Introduction to Algorithms")
    assert table.get("9780262046305") == "Introduction to Algorithms"
    assert "9780262046305" in table
    assert len(table) == 1


def test_put_existing_key_replaces_value():
    table = HashTable()
    table.put("isbn-1", "Old title")
    table.put("isbn-1", "New title")
    assert table.get("isbn-1") == "New title"
    assert len(table) == 1


def test_remove():
    table = HashTable()
    table.put("isbn-1", "Book one")
    assert table.remove("isbn-1") == "Book one"
    assert len(table) == 0
    assert "isbn-1" not in table


def test_remove_missing_key_raises_error():
    table = HashTable()
    with pytest.raises(KeyError):
        table.remove("does-not-exist")


def test_none_key_is_rejected():
    table = HashTable()
    with pytest.raises(ValueError):
        table.put(None, "value")


def test_zero_and_empty_values_are_stored():
    table = HashTable()
    table.put(0, 0)
    table.put("empty", "")
    assert table.get(0) == 0
    assert table.get("empty") == ""
    assert 0 in table


def test_collisions_are_handled():
    # Capacity 1 forces every key into the same bucket.
    table = HashTable(capacity=1, max_load_factor=100)
    for number in range(50):
        table.put(f"isbn-{number}", number)
    assert len(table) == 50
    for number in range(50):
        assert table.get(f"isbn-{number}") == number


def test_table_resizes_when_load_factor_exceeded():
    table = HashTable(capacity=4)
    for number in range(10):
        table.put(number, number)
    assert table.capacity > 4
    assert all(table.get(number) == number for number in range(10))


def test_integer_key_larger_than_64_bits():
    big_key = 2 ** 100
    table = HashTable()
    table.put(big_key, "large key")
    assert table.get(big_key) == "large key"


def test_many_items():
    table = HashTable()
    for number in range(100_000):
        table.put(number, number * 2)
    assert len(table) == 100_000
    assert table.get(99_999) == 199_998


def test_invalid_capacity_is_rejected():
    with pytest.raises(ValueError):
        HashTable(capacity=0)