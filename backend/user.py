class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    @property
    def finished_count(self):
        return sum(1 for book in self.books if book.is_finished)