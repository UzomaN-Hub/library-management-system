import random

import pytest

from library.book import Book
from library.sorting import bubble_sort, merge_sort

SORTS = [merge_sort, bubble_sort]


@pytest.mark.parametrize("sort", SORTS)
def test_empty_list(sort):
    assert sort([]) == []


@pytest.mark.parametrize("sort", SORTS)
def test_single_item(sort):
    assert sort([7]) == [7]


@pytest.mark.parametrize("sort", SORTS)
def test_already_sorted(sort):
    assert sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_reverse_order(sort):
    assert sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("sort", SORTS)
def test_all_zero_values(sort):
    assert sort([0, 0, 0, 0]) == [0, 0, 0, 0]


@pytest.mark.parametrize("sort", SORTS)
def test_negative_and_duplicate_values(sort):
    assert sort([3, -1, 3, 0, -1]) == [-1, -1, 0, 3, 3]


@pytest.mark.parametrize("sort", SORTS)
def test_integers_larger_than_64_bits(sort):
    values = [2 ** 100, 2 ** 70, -(2 ** 90), 5]
    assert sort(values) == [-(2 ** 90), 5, 2 ** 70, 2 ** 100]


@pytest.mark.parametrize("sort", SORTS)
def test_original_list_is_not_changed(sort):
    original = [3, 1, 2]
    sort(original)
    assert original == [3, 1, 2]


def test_books_sorted_by_title_ignoring_case():
    books = [
        Book("3", "python crash course", "Matthes", 2019),
        Book("1", "Clean Code", "Martin", 2008),
        Book("2", "algorithms", "Sedgewick", 2011),
    ]
    result = merge_sort(books, key=lambda book: book.title.lower())
    assert [book.title for book in result] == [
        "algorithms",
        "Clean Code",
        "python crash course",
    ]


def test_merge_sort_is_stable():
    books = [
        Book("1", "Same Title", "First", 2000),
        Book("2", "Same Title", "Second", 2001),
        Book("3", "A Title", "Third", 2002),
    ]
    result = merge_sort(books, key=lambda book: book.title)
    assert [book.author for book in result] == ["Third", "First", "Second"]


def test_merge_sort_matches_python_sort_on_large_random_list():
    values = [random.randint(-1_000_000, 1_000_000) for _ in range(100_000)]
    assert merge_sort(values) == sorted(values)