from datetime import date, timedelta

import pytest

from library.book import Book
from library.library import LOAN_PERIOD_DAYS, Library

TODAY = date(2026, 11, 1)


@pytest.fixture
def library():
    lib = Library()
    lib.add_book(Book("111", "Clean Code", "Martin", 2008))
    lib.add_book(Book("222", "Algorithms", "Sedgewick", 2011))
    lib.add_book(Book("333", "Python Crash Course", "Matthes", 2019))
    return lib


def test_empty_library():
    lib = Library()
    assert len(lib) == 0
    assert lib.find_by_isbn("111") is None
    assert lib.books_sorted_by_title() == []
    assert lib.find_by_title("Anything") == []
    assert lib.overdue_loans(TODAY) == []


def test_add_and_find_by_isbn(library):
    assert library.find_by_isbn("222").title == "Algorithms"
    assert len(library) == 3


def test_duplicate_isbn_is_rejected(library):
    with pytest.raises(ValueError):
        library.add_book(Book("111", "Another Book", "Someone", 2020))


def test_books_sorted_by_title(library):
    titles = [book.title for book in library.books_sorted_by_title()]
    assert titles == ["Algorithms", "Clean Code", "Python Crash Course"]


def test_sorted_list_updates_after_adding(library):
    library.books_sorted_by_title()
    library.add_book(Book("444", "Bash Basics", "Writer", 2021))
    titles = [book.title for book in library.books_sorted_by_title()]
    assert titles[1] == "Bash Basics"


def test_find_by_title_ignores_case_and_spaces(library):
    result = library.find_by_title("  clean CODE ")
    assert [book.isbn for book in result] == ["111"]


def test_find_by_title_returns_all_copies(library):
    library.add_book(Book("999", "Clean Code", "Martin", 2008))
    result = library.find_by_title("Clean Code")
    assert sorted(book.isbn for book in result) == ["111", "999"]


def test_remove_book(library):
    library.remove_book("111")
    assert library.find_by_isbn("111") is None
    assert library.find_by_title("Clean Code") == []


def test_remove_missing_book_raises_error(library):
    with pytest.raises(KeyError):
        library.remove_book("000")


def test_borrow_sets_due_date(library):
    due = library.borrow_book("111", "M001", TODAY)
    assert due == TODAY + timedelta(days=LOAN_PERIOD_DAYS)
    assert library.find_by_isbn("111").available is False


def test_cannot_borrow_book_on_loan(library):
    library.borrow_book("111", "M001", TODAY)
    with pytest.raises(ValueError):
        library.borrow_book("111", "M002", TODAY)


def test_cannot_remove_book_on_loan(library):
    library.borrow_book("111", "M001", TODAY)
    with pytest.raises(ValueError):
        library.remove_book("111")


def test_return_book(library):
    library.borrow_book("111", "M001", TODAY)
    assert library.return_book("111") is None
    assert library.find_by_isbn("111").available is True


def test_return_book_not_on_loan_raises_error(library):
    with pytest.raises(ValueError):
        library.return_book("111")


def test_cannot_reserve_available_book(library):
    with pytest.raises(ValueError):
        library.reserve_book("111", "M002")


def test_reservations_are_first_come_first_served(library):
    library.borrow_book("111", "M001", TODAY)
    assert library.reserve_book("111", "M002") == 1
    assert library.reserve_book("111", "M003") == 2
    assert library.return_book("111") == "M002"
    with pytest.raises(ValueError):
        library.borrow_book("111", "M003", TODAY)
    library.borrow_book("111", "M002", TODAY)
    assert library.return_book("111") == "M003"


def test_member_cannot_reserve_twice(library):
    library.borrow_book("111", "M001", TODAY)
    library.reserve_book("111", "M002")
    with pytest.raises(ValueError):
        library.reserve_book("111", "M002")


def test_overdue_loans(library):
    library.borrow_book("111", "M001", TODAY)
    library.borrow_book("222", "M002", TODAY + timedelta(days=5))
    check_day = TODAY + timedelta(days=LOAN_PERIOD_DAYS + 1)
    overdue = library.overdue_loans(check_day)
    assert [(isbn, member) for _, isbn, member in overdue] == [("111", "M001")]


def test_overdue_list_ignores_returned_books(library):
    library.borrow_book("111", "M001", TODAY)
    library.return_book("111")
    later = TODAY + timedelta(days=30)
    assert library.overdue_loans(later) == []


def test_overdue_check_can_be_repeated(library):
    library.borrow_book("111", "M001", TODAY)
    later = TODAY + timedelta(days=30)
    assert len(library.overdue_loans(later)) == 1
    assert len(library.overdue_loans(later)) == 1


def test_operations_on_missing_book_raise_key_error(library):
    with pytest.raises(KeyError):
        library.borrow_book("000", "M001", TODAY)
    with pytest.raises(KeyError):
        library.reserve_book("000", "M001")