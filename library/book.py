"""Book record stored by the library system."""

from dataclasses import dataclass


@dataclass
class Book:
    """A single book held by the library."""

    isbn: str
    title: str
    author: str
    year: int
    available: bool = True

    def __post_init__(self):
        if not self.isbn or not str(self.isbn).strip():
            raise ValueError("A book must have an ISBN.")
        if not self.title or not self.title.strip():
            raise ValueError("A book must have a title.")
        self.isbn = str(self.isbn).strip()
        self.title = self.title.strip()