import pytest

from library.book import Book
from library.searching import binary_search, linear_search
from library.sorting import merge_sort

SEARCHES = [binary_search, linear_search]


@pytest.mark.parametrize("search", SEARCHES)
def test_empty_list_returns_minus_one(search):
    assert search([], 5) == -1


@pytest.mark.parametrize("search", SEARCHES)
def test_single_item_found(search):
    assert search([5], 5) == 0


@pytest.mark.parametrize("search", SEARCHES)
def test_single_item_not_found(search):
    assert search([5], 3) == -1


@pytest.mark.parametrize("search", SEARCHES)
@pytest.mark.parametrize("target, expected", [(1, 0), (5, 2), (9, 4)])
def test_first_middle_and_last_items(search, target, expected):
    assert search([1, 3, 5, 7, 9], target) == expected


@pytest.mark.parametrize("search", SEARCHES)
@pytest.mark.parametrize("target", [0, 4, 10])
def test_missing_values(search, target):
    assert search([1, 3, 5, 7, 9], target) == -1


@pytest.mark.parametrize("search", SEARCHES)
def test_duplicates_return_first_match(search):
    assert search([1, 2, 2, 2, 3], 2) == 1


@pytest.mark.parametrize("search", SEARCHES)
def test_all_zero_values(search):
    assert search([0, 0, 0], 0) == 0


@pytest.mark.parametrize("search", SEARCHES)
def test_integers_larger_than_64_bits(search):
    values = [2 ** 64, 2 ** 80, 2 ** 100]
    assert search(values, 2 ** 80) == 1


def test_find_book_by_title_ignoring_case():
    books = [
        Book("1", "Clean Code", "Martin", 2008),
        Book("2", "Algorithms", "Sedgewick", 2011),
        Book("3", "Python Crash Course", "Matthes", 2019),
    ]
    by_title = lambda book: book.title.lower()
    sorted_books = merge_sort(books, key=by_title)
    index = binary_search(sorted_books, "clean code", key=by_title)
    assert sorted_books[index].isbn == "1"


def test_binary_search_on_large_list():
    values = list(range(0, 2_000_000, 2))  # 1,000,000 even numbers
    assert binary_search(values, 1_999_998) == 999_999
    assert binary_search(values, 1_999_999) == -1