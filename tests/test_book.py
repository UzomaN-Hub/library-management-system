import pytest

from library.book import Book


def test_create_book():
    book = Book("9780262046305", "Introduction to Algorithms", "Cormen", 2022)
    assert book.isbn == "9780262046305"
    assert book.title == "Introduction to Algorithms"
    assert book.available is True


def test_whitespace_is_trimmed():
    book = Book("  9780262046305 ", "  Clean Code  ", "Martin", 2008)
    assert book.isbn == "9780262046305"
    assert book.title == "Clean Code"


@pytest.mark.parametrize("isbn", ["", "   ", None])
def test_missing_isbn_is_rejected(isbn):
    with pytest.raises(ValueError):
        Book(isbn, "Some Title", "Author", 2020)


@pytest.mark.parametrize("title", ["", "   ", None])
def test_missing_title_is_rejected(title):
    with pytest.raises(ValueError):
        Book("9780262046305", title, "Author", 2020)