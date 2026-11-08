"""Library service that combines the data structures into one system."""

from datetime import timedelta

from library.hash_table import HashTable
from library.min_heap import MinHeap
from library.queue import Queue
from library.searching import binary_search
from library.sorting import merge_sort

LOAN_PERIOD_DAYS = 14


def _title_key(book):
    return book.title.lower()


class Library:
    """Stores books and manages loans, returns and reservations.

    books          HashTable  ISBN -> Book            O(1) lookup by ISBN
    active_loans   HashTable  ISBN -> (member, due)   who has each book
    reservations   HashTable  ISBN -> Queue           waiting list per book
    due_dates      MinHeap    due date -> loan        earliest due on top
    """

    def __init__(self):
        self._books = HashTable()
        self._active_loans = HashTable()
        self._reservations = HashTable()
        self._due_dates = MinHeap()
        self._sorted_books = None  # cached title order, rebuilt when needed

    # ----- books -----

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self._books.put(book.isbn, book)
        self._sorted_books = None

    def remove_book(self, isbn):
        book = self._require_book(isbn)
        if not book.available:
            raise ValueError("Cannot remove a book that is on loan.")
        self._books.remove(isbn)
        if isbn in self._reservations:
            self._reservations.remove(isbn)
        self._sorted_books = None
        return book

    def find_by_isbn(self, isbn):
        return self._books.get(isbn)

    def books_sorted_by_title(self):
        if self._sorted_books is None:
            self._sorted_books = merge_sort(self._books.values(), key=_title_key)
        return self._sorted_books

    def find_by_title(self, title):
        """Return every book with this title (case is ignored)."""
        target = title.strip().lower()
        books = self.books_sorted_by_title()
        index = binary_search(books, target, key=_title_key)
        matches = []
        while index != -1 and index < len(books) and _title_key(books[index]) == target:
            matches.append(books[index])
            index += 1
        return matches

    def __len__(self):
        return len(self._books)

    # ----- loans -----

    def borrow_book(self, isbn, member_id, today):
        """Lend a book and return its due date."""
        book = self._require_book(isbn)
        if not book.available:
            raise ValueError("This book is already on loan.")
        waiting = self._reservations.get(isbn)
        if waiting is not None and not waiting.is_empty():
            if waiting.peek() != member_id:
                raise ValueError("This book is reserved for another member.")
            waiting.dequeue()
        due_date = today + timedelta(days=LOAN_PERIOD_DAYS)
        book.available = False
        self._active_loans.put(isbn, (member_id, due_date))
        self._due_dates.push(due_date, (isbn, member_id))
        return due_date

    def return_book(self, isbn):
        """Mark a book as returned. Return the next member waiting, if any."""
        book = self._require_book(isbn)
        if book.available:
            raise ValueError("This book is not on loan.")
        self._active_loans.remove(isbn)
        book.available = True
        waiting = self._reservations.get(isbn)
        if waiting is not None and not waiting.is_empty():
            return waiting.peek()
        return None

    def reserve_book(self, isbn, member_id):
        """Join the waiting list for a book that is on loan."""
        book = self._require_book(isbn)
        if book.available:
            raise ValueError("This book is available. Borrow it instead.")
        waiting = self._reservations.get(isbn)
        if waiting is None:
            waiting = Queue()
            self._reservations.put(isbn, waiting)
        if member_id in waiting:
            raise ValueError("This member has already reserved the book.")
        waiting.enqueue(member_id)
        return len(waiting)

    def overdue_loans(self, today):
        """Return (due_date, isbn, member_id) for loans due before today.

        Returned books leave old entries in the heap. They are dropped
        here when found (lazy deletion), so returning a book stays O(1).
        """
        overdue = []
        while not self._due_dates.is_empty():
            due_date, (isbn, member_id) = self._due_dates.peek()
            if due_date >= today:
                break
            self._due_dates.pop()
            if self._active_loans.get(isbn) == (member_id, due_date):
                overdue.append((due_date, isbn, member_id))
        for due_date, isbn, member_id in overdue:
            self._due_dates.push(due_date, (isbn, member_id))
        return overdue

    # ----- helpers -----

    def _require_book(self, isbn):
        book = self._books.get(isbn)
        if book is None:
            raise KeyError(f"No book with ISBN {isbn}.")
        return book