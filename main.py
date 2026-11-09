"""Command-line menu for the library management system."""

from datetime import date

from library.book import Book
from library.library import Library
from library.sample_data import SAMPLE_BOOKS

MENU = """
===== Library Management System =====
1. Add a book
2. Find a book by ISBN
3. Find a book by title
4. List all books (A to Z)
5. Borrow a book
6. Return a book
7. Reserve a book
8. Show overdue loans
9. Remove a book
0. Exit
"""


def show_book(book):
    status = "Available" if book.available else "On loan"
    print(f"  {book.isbn} | {book.title} | {book.author} ({book.year}) | {status}")


def add_book(library):
    isbn = input("ISBN: ")
    title = input("Title: ")
    author = input("Author: ")
    year = int(input("Year: "))
    library.add_book(Book(isbn, title, author, year))
    print("Book added.")


def find_by_isbn(library):
    book = library.find_by_isbn(input("ISBN: ").strip())
    if book is None:
        print("No book found with that ISBN.")
    else:
        show_book(book)


def find_by_title(library):
    books = library.find_by_title(input("Title: "))
    if not books:
        print("No book found with that title.")
    for book in books:
        show_book(book)


def list_books(library):
    books = library.books_sorted_by_title()
    if not books:
        print("The library has no books.")
    for book in books:
        show_book(book)


def borrow_book(library):
    isbn = input("ISBN: ").strip()
    member_id = input("Member ID: ").strip()
    due_date = library.borrow_book(isbn, member_id, date.today())
    print(f"Book borrowed. Due back on {due_date:%d/%m/%Y}.")


def return_book(library):
    next_member = library.return_book(input("ISBN: ").strip())
    print("Book returned.")
    if next_member is not None:
        print(f"This book is reserved for member {next_member}.")


def reserve_book(library):
    isbn = input("ISBN: ").strip()
    member_id = input("Member ID: ").strip()
    position = library.reserve_book(isbn, member_id)
    print(f"Reservation made. Position in queue: {position}.")


def show_overdue(library):
    overdue = library.overdue_loans(date.today())
    if not overdue:
        print("No overdue loans.")
    for due_date, isbn, member_id in overdue:
        print(f"  {isbn} | member {member_id} | due {due_date:%d/%m/%Y}")


def remove_book(library):
    book = library.remove_book(input("ISBN: ").strip())
    print(f"Removed: {book.title}")


ACTIONS = {
    "1": add_book,
    "2": find_by_isbn,
    "3": find_by_title,
    "4": list_books,
    "5": borrow_book,
    "6": return_book,
    "7": reserve_book,
    "8": show_overdue,
    "9": remove_book,
}


def build_library():
    library = Library()
    for book in SAMPLE_BOOKS:
        library.add_book(Book(book.isbn, book.title, book.author, book.year))
    return library


def main():
    library = build_library()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Please choose a number from the menu.")
            continue
        try:
            action(library)
        except (ValueError, KeyError) as error:
            message = error.args[0] if error.args else error
            print(f"Error: {message}")


if __name__ == "__main__":
    main()