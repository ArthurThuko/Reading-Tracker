from book import Book
from library import Library
from audio_book import Audio_Book
from author import Author

author1 = Author("Robert C. Martin", "USA")
author2 = Author("David Thomas", "USA")
author3 = Author("Donald Knuth", "Canada")

book1 = Book("Clean Code", 464, author1)
book2 = Book("The Pragmatic Programmer", 632, author2)
audio_book1 = Audio_Book("The Art of Computer Programming", 1000, author3, 120)

book1.current_page = 100
book2.current_page = 200
audio_book1.current_page = 300

library = Library()
library.add_book(book1)
library.add_book(book2)
library.add_book(audio_book1)

for book in library.books:
    print(book)

print(f"Average progress of the library: {library.average_progress}%")